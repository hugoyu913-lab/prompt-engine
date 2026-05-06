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
    label = f"{prompt}"
    if default:
        label += f" [{default}]"
    label += ": "

    answer = input(label).strip()
    if answer:
        return answer
    if default:
        return default
    return ask(prompt, default)


def print_preset_keys(title: str, presets: dict) -> None:
    """Print available preset keys."""
    print(f"\n{title}")
    for key in presets:
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
        print("Use one of the listed keys exactly, such as:")
        print("  " + ", ".join(list(presets.keys())[:5]))
    choice = ask(title.rstrip("?"), default)

    if choice in presets:
        return choice

    print(f"Unknown preset: {choice}. Using default: {default}")
    return default


def build_prompt(
    subject: str,
    aesthetic_key: str,
    location: str,
    mood: str,
    camera_key: str,
    platform: str,
    aesthetics: dict,
    cameras: dict,
    poses: dict,
) -> str:
    """Build the final prompt from user input and preset data."""
    aesthetic = aesthetics[aesthetic_key]
    camera = cameras[camera_key]
    pose_key, pose = random.choice(list(poses.items()))
    details = ", ".join(aesthetic["details"])
    realism_notes = ", ".join(aesthetic["realism_notes"])

    return (
        f"Hyper-realistic {platform} photograph of {subject} in {location}. "
        f"Aesthetic: {aesthetic_key.replace('_', ' ')}. Mood: {mood}. "
        f"{aesthetic['description']} "
        f"Scene details: {details}. "
        f"Lighting: {aesthetic['lighting']}, natural falloff, practical shadows, believable highlights. "
        f"Camera: {camera['label']}; {camera['look']}. "
        f"Pose and expression: {pose}, lived-in body language, no model stiffness. "
        f"Realism requirements: {realism_notes}, natural pores, tiny skin imperfections, "
        f"realistic facial asymmetry, grounded wardrobe texture, accurate hands, believable lens distortion, "
        f"subtle background messiness, authentic social-media framing, not over-edited, not AI-looking."
    )


def build_variations(
    subject: str,
    aesthetic_key: str,
    location: str,
    mood: str,
    platform: str,
    aesthetics: dict,
    lighting: dict,
    poses: dict,
) -> list[str]:
    """Create three useful prompt variations."""
    aesthetic = aesthetics[aesthetic_key]
    lighting_values = list(lighting.values())
    pose_values = list(poses.values())

    return [
        (
            f"Candid variation: {subject} in {location}, {mood} mood, {random.choice(pose_values)}, "
            f"{random.choice(lighting_values)}, imperfect crop, slight environmental motion, "
            f"real skin texture, believable snapshot timing, composed for {platform}."
        ),
        (
            f"Editorial variation: {subject} in {location}, {aesthetic['lighting']}, "
            f"{random.choice(pose_values)}, stronger wardrobe shape, intentional negative space, "
            f"premium but realistic color grade, visible fabric texture, cinematic contrast."
        ),
        (
            f"Close portrait variation: {subject}, tighter frame, {random.choice(lighting_values)}, "
            f"honest facial detail, natural pores, subtle under-eye texture, realistic catchlights, "
            f"background from {location} still readable, non-AI-looking."
        ),
    ]


def build_captions(subject: str, mood: str, aesthetic_key: str, platform: str) -> list[str]:
    """Create stronger social caption ideas."""
    aesthetic_name = aesthetic_key.replace("_", " ")
    short_subject = subject.split(" wearing ")[0].strip()
    return [
        f"{mood.capitalize()}, but keep it effortless.",
        f"{aesthetic_name.title()} frame with real-life texture.",
        f"{short_subject.capitalize()} energy, caught between moments.",
        f"Saved this one for the {platform} grid.",
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


def render_markdown(
    subject: str,
    aesthetic_key: str,
    location: str,
    mood: str,
    camera_key: str,
    platform: str,
    final_prompt: str,
    negative_prompt: str,
    variations: list[str],
    captions: list[str],
    scorecard: dict,
) -> str:
    """Render the full result as Markdown."""
    variation_lines = "\n".join(f"{index}. {text}" for index, text in enumerate(variations, 1))
    caption_lines = "\n".join(f"- {caption}" for caption in captions)
    problem_lines = "\n".join(f"- {item}" for item in scorecard["problems_noticed"])
    improvement_lines = "\n".join(f"- {item}" for item in scorecard["prompt_improvement_notes"])
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""# Prompt Engine Output

Generated: {created_at}

## Input

- Subject: {subject}
- Aesthetic: `{aesthetic_key}`
- Location: {location}
- Mood: {mood}
- Camera: `{camera_key}`
- Platform: {platform}

## Final Prompt

{final_prompt}

## Negative Prompt

{negative_prompt}

## 3 Variations

{variation_lines}

## Social Media Caption Ideas

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


def maybe_print_list_and_exit(aesthetics: dict, cameras: dict) -> None:
    """Support a simple list command before interactive generation."""
    if len(sys.argv) < 2:
        return

    command = sys.argv[1].lower()
    if command not in {"list", "--list", "-l"}:
        return

    print_preset_keys("Available aesthetics", aesthetics)
    print_preset_keys("Available cameras", cameras)
    raise SystemExit(0)


def main() -> None:
    """Run the interactive CLI."""
    aesthetics = load_json("aesthetics.json")
    cameras = load_json("cameras.json")
    lighting = load_json("lighting.json")
    poses = load_json("poses.json")
    negative_prompt = load_negative_prompt()

    maybe_print_list_and_exit(aesthetics, cameras)

    print("Prompt Engine")
    print("Generate hyper-realistic social media image prompts.\n")
    print("Tip: run `python src/generate_prompt.py --list` to view aesthetics and cameras.\n")

    subject = ask("Subject", "a stylish person with realistic skin texture")
    aesthetic_key = choose_from_presets("Aesthetic", aesthetics, "quiet_luxury")
    location = ask("Location", "a cinematic city street")
    mood = ask("Mood", "confident and cinematic")
    camera_key = choose_from_presets("Camera", cameras, "canon_r5_50mm")
    platform = ask("Platform", "Instagram")

    final_prompt = build_prompt(
        subject,
        aesthetic_key,
        location,
        mood,
        camera_key,
        platform,
        aesthetics,
        cameras,
        poses,
    )
    variations = build_variations(
        subject,
        aesthetic_key,
        location,
        mood,
        platform,
        aesthetics,
        lighting,
        poses,
    )
    captions = build_captions(subject, mood, aesthetic_key, platform)
    scorecard = build_scorecard()

    markdown = render_markdown(
        subject,
        aesthetic_key,
        location,
        mood,
        camera_key,
        platform,
        final_prompt,
        negative_prompt,
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
