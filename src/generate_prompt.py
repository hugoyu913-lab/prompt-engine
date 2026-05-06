"""Prompt Engine CLI.

Generate hyper-realistic aesthetic social media image prompts.
Uses only the Python standard library.
"""

from __future__ import annotations

import json
import random
import sys
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRESETS_DIR = PROJECT_ROOT / "presets"
PROMPTS_DIR = PROJECT_ROOT / "prompts"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
LATEST_OUTPUT = OUTPUTS_DIR / "latest_prompt.md"
LIST_COMMANDS = {"list", "ls", "help", "?"}

PLATFORM_PROFILES = {
    "instagram_vertical_post": {
        "label": "Instagram vertical post",
        "format": "4:5 vertical crop, strong first-glance composition, feed-ready polish",
        "caption": "grid",
    },
    "tiktok_slideshow": {
        "label": "TikTok slideshow",
        "format": "9:16 vertical composition, bold subject read, clear story-frame energy",
        "caption": "slideshow",
    },
    "x_twitter_image": {
        "label": "X/Twitter image",
        "format": "wide 16:9 or 3:2 crop, readable thumbnail, sharp central subject",
        "caption": "timeline",
    },
    "pinterest_pin": {
        "label": "Pinterest pin",
        "format": "2:3 vertical crop, aspirational detail, save-worthy lifestyle framing",
        "caption": "pin",
    },
    "album_cover": {
        "label": "album cover",
        "format": "square 1:1 crop, iconic central image, negative space for title placement",
        "caption": "cover",
    },
}

MODEL_PROFILES = {
    "midjourney": {
        "label": "Midjourney",
        "instruction": "Use compact visual phrases, strong photographic tags, and clear aspect-ratio guidance.",
        "suffix": "--style raw --v 6",
    },
    "chatgpt_image": {
        "label": "ChatGPT image generation",
        "instruction": "Use natural-language direction with explicit realism, identity, camera, and composition constraints.",
        "suffix": "",
    },
    "stable_diffusion_flux": {
        "label": "Stable Diffusion / Flux",
        "instruction": "Use weighted detail-friendly phrasing, concrete camera terms, and keep negatives separate.",
        "suffix": "high detail, natural skin texture, realistic photography",
    },
}


def load_json(filename: str) -> dict:
    """Load a JSON preset file from the presets directory."""
    path = PRESETS_DIR / filename
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def load_negative_prompt() -> str:
    """Return the negative prompt text without Markdown headings."""
    path = PROMPTS_DIR / "negative_prompt.md"
    text = path.read_text(encoding="utf-8")
    return (
        text.replace("# Negative Prompt", "")
        .replace("Avoid:", "")
        .strip()
        .replace("\n\n", " ")
        .replace("\n", " ")
    )


def ask(prompt: str, default: str | None = None) -> str:
    """Ask for user input with an optional default."""
    label = prompt
    if default:
        label += f" [{default}]"
    answer = input(f"{label}: ").strip()

    if answer:
        return answer
    if default:
        return default
    return ask(prompt, default)


def print_preset_keys(title: str, presets: dict) -> None:
    """Print available preset keys."""
    print(f"\n{title}")
    for key, value in presets.items():
        label = value.get("label") if isinstance(value, dict) else None
        if label:
            print(f"  - {key} ({label})")
        else:
            print(f"  - {key}")


def choose_from_presets(title: str, presets: dict, default: str) -> str:
    """Ask for a preset and keep asking until the key exists."""
    print_preset_keys(f"Available {title.lower()}s", presets)
    print("Type a key, or type 'list' to show options again.")

    while True:
        choice = ask(title, default)

        if choice in LIST_COMMANDS:
            print_preset_keys(f"Available {title.lower()}s", presets)
            continue

        if choice in presets:
            return choice

        print(f"Unknown {title.lower()}: {choice}")
        print("No fallback used. Enter one of these keys exactly:")
        print("  " + ", ".join(presets.keys()))


def choose_random_key(presets: dict) -> str:
    """Return a random key from a preset dictionary."""
    return random.choice(list(presets.keys()))


def build_universal_prompt(
    subject: str,
    aesthetic_key: str,
    location: str,
    mood: str,
    camera_key: str,
    platform_key: str,
    lighting_key: str,
    pose_key: str,
    aesthetics: dict,
    cameras: dict,
    lighting: dict,
    poses: dict,
) -> str:
    """Build a platform-aware universal prompt."""
    aesthetic = aesthetics[aesthetic_key]
    camera = cameras[camera_key]
    platform = PLATFORM_PROFILES[platform_key]
    details = ", ".join(aesthetic["details"])
    realism_notes = ", ".join(aesthetic["realism_notes"])

    return (
        f"Hyper-realistic photograph of {subject} in {location}. "
        f"Platform: {platform['label']}; compose as {platform['format']}. "
        f"Aesthetic: {aesthetic_key.replace('_', ' ')}. Mood: {mood}. "
        f"{aesthetic['description']} "
        f"Scene details: {details}. "
        f"Lighting: {lighting[lighting_key]}; also preserve {aesthetic['lighting']}. "
        f"Camera: {camera['label']}; {camera['look']}. "
        f"Pose and expression: {poses[pose_key]}, lived-in body language, no stiff model posing. "
        f"Realism requirements: {realism_notes}, natural pores, tiny skin imperfections, "
        f"realistic facial asymmetry, grounded wardrobe texture, accurate hands, believable lens distortion, "
        f"subtle background messiness, authentic social-media framing, not over-edited, not AI-looking."
    )


def build_model_specific_prompt(universal_prompt: str, model_key: str, platform_key: str) -> str:
    """Adapt the universal prompt to a selected image model."""
    model = MODEL_PROFILES[model_key]
    platform = PLATFORM_PROFILES[platform_key]

    prompt = (
        f"{model['instruction']} "
        f"{universal_prompt} "
        f"Prioritize believable photography, identity consistency, and {platform['format']}."
    )
    if model["suffix"]:
        prompt += f" {model['suffix']}"
    return prompt


def build_identity_lock(subject: str) -> dict:
    """Create an identity consistency section."""
    return {
        "immutable_traits": [
            f"Keep the same core subject: {subject}.",
            "Preserve face shape, apparent age range, body type, skin tone, hair length, and hair color.",
            "Preserve key wardrobe anchors and recognizable styling details from the subject description.",
        ],
        "must_not_change": [
            "Do not change ethnicity, age range, body build, hairstyle, facial structure, or signature outfit elements.",
            "Do not add extra people unless the subject explicitly asks for them.",
            "Do not glamorize so much that the person becomes a different identity.",
        ],
        "consistency_reminders": [
            "Repeat stable identity traits in every variation.",
            "Keep facial features realistic and asymmetric, not beauty-filtered.",
            "If regenerating, compare eyes, jawline, hair, hands, and wardrobe anchor first.",
        ],
    }


def build_variations(
    subject: str,
    aesthetic_key: str,
    location: str,
    mood: str,
    platform_key: str,
    lighting_key: str,
    pose_key: str,
    aesthetics: dict,
    lighting: dict,
    poses: dict,
) -> list[str]:
    """Create three useful prompt variations."""
    aesthetic = aesthetics[aesthetic_key]
    platform = PLATFORM_PROFILES[platform_key]
    selected_lighting = lighting[lighting_key]
    selected_pose = poses[pose_key]

    return [
        (
            f"Candid variation: {subject} in {location}, {mood} mood, {selected_pose}, "
            f"{selected_lighting}, imperfect crop, slight environmental motion, "
            f"real skin texture, believable snapshot timing, {platform['format']}."
        ),
        (
            f"Editorial variation: {subject} in {location}, {aesthetic['lighting']}, "
            f"{selected_pose}, stronger wardrobe shape, intentional negative space, "
            f"premium but realistic color grade, visible fabric texture, cinematic contrast, {platform['format']}."
        ),
        (
            f"Close portrait variation: {subject}, tighter frame, {selected_lighting}, "
            f"honest facial detail, natural pores, subtle under-eye texture, realistic catchlights, "
            f"background from {location} still readable, identity locked, non-AI-looking."
        ),
    ]


def build_captions(subject: str, mood: str, aesthetic_key: str, platform_key: str) -> list[str]:
    """Create platform-aware social caption ideas."""
    aesthetic_name = aesthetic_key.replace("_", " ")
    platform = PLATFORM_PROFILES[platform_key]
    short_subject = subject.split(" wearing ")[0].strip()
    return [
        f"{mood.capitalize()}, but keep it effortless.",
        f"{aesthetic_name.title()} frame with real-life texture.",
        f"{short_subject.capitalize()} energy, caught between moments.",
        f"Saved this one for the {platform['caption']}.",
        "Soft flaws, sharp timing.",
        "Looks unplanned. Was not.",
    ]


def build_scorecard() -> dict:
    """Create a review scorecard template for judging generated images."""
    return {
        "realism": "__/10",
        "aesthetic": "__/10",
        "identity_consistency": "__/10",
        "social_media_postability": "__/10",
        "problems_noticed": [
            "Check hands, teeth, eyes, hairline, skin texture, clothing seams, and background text.",
            "Look for over-smoothed skin, warped accessories, fake logos, or impossible shadows.",
        ],
        "prompt_improvement_notes": [
            "If image looks too artificial, add more camera-specific detail and reduce beauty language.",
            "If aesthetic is weak, add 2-3 concrete wardrobe, lighting, or location details.",
            "If identity drifts, repeat stable traits: age range, hair, face shape, wardrobe anchor.",
        ],
    }


def render_list(title: str, items: list[str]) -> str:
    """Render Markdown bullet list."""
    return "\n".join(f"- {item}" for item in items)


def render_markdown(
    subject: str,
    aesthetic_key: str,
    location: str,
    mood: str,
    camera_key: str,
    platform_key: str,
    model_key: str,
    lighting_key: str,
    pose_key: str,
    universal_prompt: str,
    model_specific_prompt: str,
    negative_prompt: str,
    identity_lock: dict,
    variations: list[str],
    captions: list[str],
    scorecard: dict,
) -> str:
    """Render the full result as Markdown."""
    variation_lines = "\n".join(f"{index}. {text}" for index, text in enumerate(variations, 1))
    caption_lines = "\n".join(f"- {caption}" for caption in captions)
    problem_lines = render_list("Problems noticed", scorecard["problems_noticed"])
    improvement_lines = render_list("Prompt improvement notes", scorecard["prompt_improvement_notes"])
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""# Prompt Engine Output

Generated: {created_at}

## Input

- Subject: {subject}
- Aesthetic: `{aesthetic_key}`
- Location: {location}
- Mood: {mood}
- Camera: `{camera_key}`
- Platform: `{platform_key}` ({PLATFORM_PROFILES[platform_key]["label"]})
- Model profile: `{model_key}` ({MODEL_PROFILES[model_key]["label"]})
- Lighting: `{lighting_key}`
- Pose: `{pose_key}`

## Universal Prompt

{universal_prompt}

## Model-Specific Prompt

{model_specific_prompt}

## Negative Prompt

{negative_prompt}

## Identity Lock

### Immutable face/body traits

{render_list("Immutable traits", identity_lock["immutable_traits"])}

### What must not change

{render_list("Must not change", identity_lock["must_not_change"])}

### Consistency reminders

{render_list("Consistency reminders", identity_lock["consistency_reminders"])}

## 3 Variations

{variation_lines}

## Captions

{caption_lines}

## Image Review Scorecard

- Realism: {scorecard["realism"]}
- Aesthetic: {scorecard["aesthetic"]}
- Identity consistency: {scorecard["identity_consistency"]}
- Social media postability: {scorecard["social_media_postability"]}

### Problems noticed

{problem_lines}

### Prompt improvement notes

{improvement_lines}
"""


def has_command(*commands: str) -> bool:
    """Return True when any command appears in argv."""
    entered = {arg.lower() for arg in sys.argv[1:]}
    return any(command in entered for command in commands)


def maybe_print_list_and_exit(aesthetics: dict, cameras: dict) -> None:
    """Support a simple list command before interactive generation."""
    if not has_command("list", "--list", "-l"):
        return

    print_preset_keys("Available aesthetics", aesthetics)
    print_preset_keys("Available cameras", cameras)
    print_preset_keys("Available platforms", PLATFORM_PROFILES)
    print_preset_keys("Available model profiles", MODEL_PROFILES)
    raise SystemExit(0)


def main() -> None:
    """Run the interactive CLI."""
    aesthetics = load_json("aesthetics.json")
    cameras = load_json("cameras.json")
    lighting = load_json("lighting.json")
    poses = load_json("poses.json")
    negative_prompt = load_negative_prompt()
    random_mode = has_command("--random", "random")

    maybe_print_list_and_exit(aesthetics, cameras)

    print("Prompt Engine")
    print("Generate hyper-realistic social media image prompts.\n")
    print("Tip: run `python src/generate_prompt.py --list` to view options.")
    print("Tip: run `python src/generate_prompt.py --random` to randomize aesthetic, camera, lighting, and pose.\n")

    subject = ask("Subject", "a stylish person with realistic skin texture")
    if random_mode:
        aesthetic_key = choose_random_key(aesthetics)
        camera_key = choose_random_key(cameras)
        lighting_key = choose_random_key(lighting)
        pose_key = choose_random_key(poses)
        print("\nRandom selections")
        print(f"  Aesthetic: {aesthetic_key}")
        print(f"  Camera: {camera_key}")
        print(f"  Lighting: {lighting_key}")
        print(f"  Pose: {pose_key}")
    else:
        aesthetic_key = choose_from_presets("Aesthetic", aesthetics, "quiet_luxury")
        camera_key = choose_from_presets("Camera", cameras, "canon_r5_50mm")
        lighting_key = choose_from_presets("Lighting", lighting, "cinematic_window")
        pose_key = choose_from_presets("Pose", poses, "candid_glance")

    location = ask("Location", "a cinematic city street")
    mood = ask("Mood", "confident and cinematic")
    platform_key = choose_from_presets("Platform", PLATFORM_PROFILES, "instagram_vertical_post")
    model_key = choose_from_presets("Model profile", MODEL_PROFILES, "chatgpt_image")

    universal_prompt = build_universal_prompt(
        subject,
        aesthetic_key,
        location,
        mood,
        camera_key,
        platform_key,
        lighting_key,
        pose_key,
        aesthetics,
        cameras,
        lighting,
        poses,
    )
    model_specific_prompt = build_model_specific_prompt(universal_prompt, model_key, platform_key)
    identity_lock = build_identity_lock(subject)
    variations = build_variations(
        subject,
        aesthetic_key,
        location,
        mood,
        platform_key,
        lighting_key,
        pose_key,
        aesthetics,
        lighting,
        poses,
    )
    captions = build_captions(subject, mood, aesthetic_key, platform_key)
    scorecard = build_scorecard()

    markdown = render_markdown(
        subject,
        aesthetic_key,
        location,
        mood,
        camera_key,
        platform_key,
        model_key,
        lighting_key,
        pose_key,
        universal_prompt,
        model_specific_prompt,
        negative_prompt,
        identity_lock,
        variations,
        captions,
        scorecard,
    )

    OUTPUTS_DIR.mkdir(exist_ok=True)
    LATEST_OUTPUT.write_text(markdown, encoding="utf-8")

    print("\n" + markdown)
    print(f"Saved to {LATEST_OUTPUT}")


if __name__ == "__main__":
    main()
