"""Prompt Engine CLI.

Generate hyper-realistic aesthetic social media image prompts.
Uses only the Python standard library.
"""

from __future__ import annotations

import json
import random
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRESETS_DIR = PROJECT_ROOT / "presets"
PROMPTS_DIR = PROJECT_ROOT / "prompts"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
LATEST_OUTPUT = OUTPUTS_DIR / "latest_prompt.md"


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


def choose_from_presets(title: str, presets: dict, default: str) -> str:
    """Show preset keys and ask the user to choose one."""
    print(f"\n{title}")
    for key in presets:
        print(f"  - {key}")
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

    return (
        f"Hyper-realistic social media photograph of {subject} in {location}, "
        f"styled with the {aesthetic_key.replace('_', ' ')} aesthetic. "
        f"Mood: {mood}. {aesthetic['description']} "
        f"Use {aesthetic['lighting']} with {camera['label']} characteristics: {camera['look']}. "
        f"Pose direction: {pose}. "
        f"Include {details}, realistic skin texture, natural pores, believable facial asymmetry, "
        f"authentic human expression, realistic hands, natural shadows, cinematic lighting, "
        f"believable lens behavior, social-media-native composition for {platform}, "
        f"editorial taste, subtle imperfections, non-AI-looking photography."
    )


def build_variations(
    subject: str,
    location: str,
    platform: str,
    lighting: dict,
    poses: dict,
) -> list[str]:
    """Create three useful prompt variations."""
    lighting_values = list(lighting.values())
    pose_values = list(poses.values())

    return [
        (
            f"More candid: {subject} in {location}, {random.choice(pose_values)}, "
            f"{random.choice(lighting_values)}, looser framing for {platform}."
        ),
        (
            f"More editorial: {subject} in {location}, {random.choice(pose_values)}, "
            f"cleaner composition, stronger wardrobe focus, cinematic contrast."
        ),
        (
            f"More intimate: close realistic portrait of {subject}, natural skin texture, "
            f"{random.choice(lighting_values)}, quiet emotional detail."
        ),
    ]


def build_captions(mood: str, aesthetic_key: str) -> list[str]:
    """Create short social caption ideas."""
    aesthetic_name = aesthetic_key.replace("_", " ")
    return [
        f"{mood.capitalize()} in motion.",
        f"{aesthetic_name.title()} energy, no filter needed.",
        "Make it look effortless.",
        "Real light. Real texture. Real moment.",
        "A frame worth keeping.",
    ]


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
) -> str:
    """Render the full result as Markdown."""
    variation_lines = "\n".join(f"{index}. {text}" for index, text in enumerate(variations, 1))
    caption_lines = "\n".join(f"- {caption}" for caption in captions)
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
"""


def main() -> None:
    """Run the interactive CLI."""
    aesthetics = load_json("aesthetics.json")
    cameras = load_json("cameras.json")
    lighting = load_json("lighting.json")
    poses = load_json("poses.json")
    negative_prompt = load_negative_prompt()

    print("Prompt Engine")
    print("Generate hyper-realistic social media image prompts.\n")

    subject = ask("Subject", "a stylish person with realistic skin texture")
    aesthetic_key = choose_from_presets("Choose aesthetic", aesthetics, "quiet_luxury")
    location = ask("Location", "a cinematic city street")
    mood = ask("Mood", "confident and cinematic")
    camera_key = choose_from_presets("Choose camera", cameras, "canon_r5_50mm")
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
    variations = build_variations(subject, location, platform, lighting, poses)
    captions = build_captions(mood, aesthetic_key)

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
    )

    OUTPUTS_DIR.mkdir(exist_ok=True)
    LATEST_OUTPUT.write_text(markdown, encoding="utf-8")

    print("\n" + markdown)
    print(f"Saved to {LATEST_OUTPUT}")


if __name__ == "__main__":
    main()
