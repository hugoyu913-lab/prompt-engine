"""Prompt Engine CLI.

Generate hyper-realistic aesthetic social media image prompts.
Uses only the Python standard library.
"""

from __future__ import annotations

import json
import random
import sys
import uuid
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRESETS_DIR = PROJECT_ROOT / "presets"
PROMPTS_DIR = PROJECT_ROOT / "prompts"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
DATA_DIR = PROJECT_ROOT / "data"
LATEST_OUTPUT = OUTPUTS_DIR / "latest_prompt.md"
PROMPT_RUNS_FILE = DATA_DIR / "prompt_runs.jsonl"
IMAGE_REVIEWS_FILE = DATA_DIR / "image_reviews.jsonl"
LEARNED_PATTERNS_FILE = DATA_DIR / "learned_patterns.json"
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


def append_jsonl(path: Path, record: dict) -> None:
    """Append one JSON object to a JSONL file."""
    path.parent.mkdir(exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=True) + "\n")


def read_jsonl(path: Path) -> list[dict]:
    """Read JSONL records, skipping blank or broken lines."""
    if not path.exists():
        return []

    records = []
    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return records


def save_json(path: Path, data: dict) -> None:
    """Save a dictionary as pretty JSON."""
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def load_learned_patterns() -> dict:
    """Load learned prompt patterns if analysis has been run."""
    if not LEARNED_PATTERNS_FILE.exists():
        return {}
    try:
        return json.loads(LEARNED_PATTERNS_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


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


def ask_optional(prompt: str) -> str:
    """Ask for optional text."""
    return input(f"{prompt}: ").strip()


def ask_score(prompt: str) -> int:
    """Ask for a 1-10 review score."""
    while True:
        answer = ask(prompt)
        try:
            score = int(answer)
        except ValueError:
            print("Enter a whole number from 1 to 10.")
            continue

        if 1 <= score <= 10:
            return score

        print("Score must be from 1 to 10.")


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


def build_prompt_dna(
    aesthetic_key: str,
    camera_key: str,
    platform_key: str,
    lighting_key: str,
    mood: str,
    aesthetics: dict,
    cameras: dict,
    lighting: dict,
) -> dict:
    """Describe the prompt's reusable creative pattern."""
    aesthetic = aesthetics[aesthetic_key]
    camera = cameras[camera_key]
    return {
        "realism_style": ", ".join(aesthetic["realism_notes"]),
        "camera_language": f"{camera['label']}: {camera['look']}",
        "composition_language": PLATFORM_PROFILES[platform_key]["format"],
        "aesthetic_intensity": f"Medium-strong {aesthetic_key.replace('_', ' ')} with grounded detail.",
        "lighting_behavior": lighting[lighting_key],
        "emotional_tone": mood,
    }


def build_mutation_notes(reason: str, changes: list[str]) -> dict:
    """Describe how and why a prompt changed."""
    return {
        "what_changed": changes,
        "why_it_changed": reason,
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
    run_id: str,
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
    prompt_dna: dict,
    mutation_notes: dict,
    variations: list[str],
    captions: list[str],
    scorecard: dict,
) -> str:
    """Render the full result as Markdown."""
    variation_lines = "\n".join(f"{index}. {text}" for index, text in enumerate(variations, 1))
    caption_lines = "\n".join(f"- {caption}" for caption in captions)
    dna_lines = "\n".join(f"- {key.replace('_', ' ').title()}: {value}" for key, value in prompt_dna.items())
    changed_lines = render_list("What changed", mutation_notes["what_changed"])
    problem_lines = render_list("Problems noticed", scorecard["problems_noticed"])
    improvement_lines = render_list("Prompt improvement notes", scorecard["prompt_improvement_notes"])
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"""# Prompt Engine Output

Run ID: {run_id}

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

## Prompt DNA

{dna_lines}

## Mutation Notes

### What changed from the original prompt

{changed_lines}

### Why it changed

{mutation_notes["why_it_changed"]}

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


def show_history(limit: int = 10) -> None:
    """Show recent prompt runs."""
    runs = read_jsonl(PROMPT_RUNS_FILE)
    if not runs:
        print("No prompt runs found.")
        return

    print(f"Recent prompt runs (last {min(limit, len(runs))})")
    for run in runs[-limit:]:
        print(
            f"{run['run_id']} | {run['created_at']} | {run['aesthetic']} | "
            f"{run['camera']} | {run['pose']} | {run['platform']} | {run['subject']}"
        )


def review_prompt_run() -> None:
    """Collect and save an image review for a generated prompt."""
    runs = {run["run_id"]: run for run in read_jsonl(PROMPT_RUNS_FILE)}
    if not runs:
        print("No prompt runs found. Generate a prompt first.")
        return

    run_id = ask("Run ID")
    if run_id not in runs:
        print(f"Unknown run_id: {run_id}")
        print("Use --history to see recent run IDs.")
        return

    realism = ask_score("Realism score /10")
    aesthetic = ask_score("Aesthetic score /10")
    identity = ask_score("Identity score /10")
    postability = ask_score("Postability score /10")
    notes = ask_optional("Notes")
    what_failed = ask_optional("What failed")
    what_to_improve = ask_optional("What to improve")
    average_score = round((realism + aesthetic + identity + postability) / 4, 2)

    review = {
        "review_id": uuid.uuid4().hex[:12],
        "run_id": run_id,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "realism": realism,
        "aesthetic": aesthetic,
        "identity": identity,
        "postability": postability,
        "average_score": average_score,
        "notes": notes,
        "what_failed": what_failed,
        "what_to_improve": what_to_improve,
    }
    append_jsonl(IMAGE_REVIEWS_FILE, review)

    run = runs[run_id]
    print(f"Saved review for {run_id}. Average: {average_score}/10")
    print(f"{run['aesthetic']} | {run['camera']} | {run['pose']} | {run['platform']}")


def show_best(limit: int = 5) -> None:
    """Show highest scoring reviewed prompt runs."""
    runs = {run["run_id"]: run for run in read_jsonl(PROMPT_RUNS_FILE)}
    reviews = read_jsonl(IMAGE_REVIEWS_FILE)
    if not reviews:
        print("No image reviews found. Use --review after testing generated images.")
        return

    best_by_run = {}
    for review in reviews:
        run_id = review["run_id"]
        if run_id not in runs:
            continue
        if run_id not in best_by_run or review["average_score"] > best_by_run[run_id]["average_score"]:
            best_by_run[run_id] = review

    ranked = sorted(best_by_run.values(), key=lambda item: item["average_score"], reverse=True)
    if not ranked:
        print("No reviewed prompt runs matched saved history.")
        return

    print(f"Best prompt runs (top {min(limit, len(ranked))})")
    for review in ranked[:limit]:
        run = runs[review["run_id"]]
        print(
            f"{review['average_score']}/10 | {review['run_id']} | {run['aesthetic']} | "
            f"{run['camera']} | {run['lighting']} | {run['pose']} | {run['platform']}"
        )
        if review.get("what_to_improve"):
            print(f"  improve: {review['what_to_improve']}")


def average_by_field(reviewed_runs: list[dict], field: str) -> list[dict]:
    """Average review scores by a run field."""
    buckets = {}
    for item in reviewed_runs:
        key = item["run"].get(field, "unknown")
        buckets.setdefault(key, []).append(item["review"]["average_score"])

    results = []
    for key, scores in buckets.items():
        results.append({"name": key, "average_score": round(sum(scores) / len(scores), 2), "count": len(scores)})
    return sorted(results, key=lambda item: (item["average_score"], item["count"]), reverse=True)


def detect_common_traits(high_scoring_runs: list[dict]) -> list[str]:
    """Find simple repeated prompt traits in strong runs."""
    trait_checks = {
        "natural pores and skin texture": ["natural pores", "skin texture"],
        "direct flash or hard practical light": ["direct flash", "on-camera flash", "hard"],
        "cinematic low-light realism": ["low-light", "cinematic", "night"],
        "imperfect candid framing": ["imperfect crop", "candid", "snapshot"],
        "visible wardrobe and fabric texture": ["fabric texture", "wardrobe", "clothing folds"],
        "clear platform crop language": ["crop", "composition", "framing"],
        "identity consistency reminders": ["identity", "same core subject", "preserve"],
    }
    text = " ".join(item["run"].get("universal_prompt", "").lower() for item in high_scoring_runs)
    found = []
    for trait, needles in trait_checks.items():
        if any(needle in text for needle in needles):
            found.append(trait)
    return found or ["No repeated traits detected yet. Add more reviewed runs."]


def analyze_reviewed_runs() -> dict:
    """Analyze reviewed runs and save learned pattern data."""
    runs = {run["run_id"]: run for run in read_jsonl(PROMPT_RUNS_FILE)}
    reviews = read_jsonl(IMAGE_REVIEWS_FILE)
    reviewed_runs = [{"run": runs[review["run_id"]], "review": review} for review in reviews if review["run_id"] in runs]

    if not reviewed_runs:
        findings = {
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "reviewed_run_count": 0,
            "message": "No reviewed prompt runs yet. Generate prompts, review images, then run --analyze.",
        }
        save_json(LEARNED_PATTERNS_FILE, findings)
        print(findings["message"])
        return findings

    high_scoring = [item for item in reviewed_runs if item["review"]["average_score"] >= 8]
    if not high_scoring:
        high_scoring = sorted(reviewed_runs, key=lambda item: item["review"]["average_score"], reverse=True)[:3]

    findings = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "reviewed_run_count": len(reviewed_runs),
        "high_scoring_run_count": len(high_scoring),
        "highest_scoring_aesthetics": average_by_field(reviewed_runs, "aesthetic"),
        "best_cameras": average_by_field(reviewed_runs, "camera"),
        "best_lighting_setups": average_by_field(reviewed_runs, "lighting"),
        "best_platforms": average_by_field(reviewed_runs, "platform"),
        "common_traits_high_scoring": detect_common_traits(high_scoring),
        "top_run_ids": [item["run"]["run_id"] for item in sorted(high_scoring, key=lambda item: item["review"]["average_score"], reverse=True)[:5]],
    }
    save_json(LEARNED_PATTERNS_FILE, findings)

    print(f"Saved learned patterns to {LEARNED_PATTERNS_FILE}")
    print("Top aesthetics: " + ", ".join(item["name"] for item in findings["highest_scoring_aesthetics"][:3]))
    print("Top cameras: " + ", ".join(item["name"] for item in findings["best_cameras"][:3]))
    print("Top lighting: " + ", ".join(item["name"] for item in findings["best_lighting_setups"][:3]))
    return findings


def best_key_from_patterns(patterns: dict, section: str, fallback: str) -> str:
    """Pick a learned best key if available."""
    items = patterns.get(section, [])
    if items:
        return items[0]["name"]
    return fallback


def build_evolved_selection(patterns: dict, aesthetics: dict, cameras: dict, lighting: dict, poses: dict) -> dict:
    """Choose presets biased toward learned high-scoring patterns."""
    aesthetic_key = best_key_from_patterns(patterns, "highest_scoring_aesthetics", choose_random_key(aesthetics))
    camera_key = best_key_from_patterns(patterns, "best_cameras", choose_random_key(cameras))
    lighting_key = best_key_from_patterns(patterns, "best_lighting_setups", choose_random_key(lighting))
    if aesthetic_key not in aesthetics:
        aesthetic_key = choose_random_key(aesthetics)
    if camera_key not in cameras:
        camera_key = choose_random_key(cameras)
    if lighting_key not in lighting:
        lighting_key = choose_random_key(lighting)
    return {
        "aesthetic": aesthetic_key,
        "camera": camera_key,
        "lighting": lighting_key,
        "pose": choose_random_key(poses),
    }


def mutate_text(base_prompt: str, variant_number: int) -> tuple[str, list[str]]:
    """Create one evolved prompt mutation."""
    changes_by_variant = [
        (
            "Increase camera specificity and preserve practical imperfections.",
            "Add lens behavior, imperfect focus, visible pores, and grounded color.",
        ),
        (
            "Tighten composition language for stronger social-media readability.",
            "Add crop, negative space, subject hierarchy, and thumbnail clarity.",
        ),
        (
            "Raise aesthetic intensity while keeping photography believable.",
            "Add stronger wardrobe, environment, and lighting cues without fantasy styling.",
        ),
        (
            "Add environmental detail so the scene feels lived-in.",
            "Add background texture, clutter, reflections, weather, or room-specific objects.",
        ),
        (
            "Make realism wording more defensive against AI-looking output.",
            "Add asymmetry, fabric flaws, natural hands, imperfect skin, and real lens distortion.",
        ),
    ]
    change, addition = changes_by_variant[variant_number % len(changes_by_variant)]
    return f"{base_prompt} Evolved direction: {addition}", [change]


def mutate_prompt_run() -> None:
    """Create evolved variants from an existing run."""
    runs = {run["run_id"]: run for run in read_jsonl(PROMPT_RUNS_FILE)}
    if not runs:
        print("No prompt runs found. Generate a prompt first.")
        return

    run_id = ask("Run ID to mutate")
    if run_id not in runs:
        print(f"Unknown run_id: {run_id}")
        print("Use --history to see recent run IDs.")
        return

    original = runs[run_id]
    variant_count = 5
    evolved_variants = []
    all_changes = []
    for index in range(variant_count):
        prompt, changes = mutate_text(original["universal_prompt"], index)
        evolved_variants.append(prompt)
        all_changes.extend(changes)

    mutation_run_id = uuid.uuid4().hex[:12]
    identity_lock = build_identity_lock(original["subject"])
    prompt_dna = {
        "realism_style": "Preserve original identity while increasing realism safeguards.",
        "camera_language": "Mutated camera wording across variants.",
        "composition_language": "Mutated crop and social readability wording.",
        "aesthetic_intensity": "Slightly varied across variants.",
        "lighting_behavior": "Preserve original lighting behavior and add practical detail.",
        "emotional_tone": original["mood"],
    }
    mutation_notes = build_mutation_notes(
        f"Mutated from run {run_id} to test which wording improves postability without changing identity.",
        all_changes,
    )
    variant_lines = "\n\n".join(f"### Variant {index}\n\n{prompt}" for index, prompt in enumerate(evolved_variants, 1))
    markdown = f"""# Prompt Mutation Output

Run ID: {mutation_run_id}
Parent Run ID: {run_id}

## Identity Lock

### Immutable face/body traits

{render_list("Immutable traits", identity_lock["immutable_traits"])}

### What must not change

{render_list("Must not change", identity_lock["must_not_change"])}

### Consistency reminders

{render_list("Consistency reminders", identity_lock["consistency_reminders"])}

## Prompt DNA

{render_list("Prompt DNA", [f"{key.replace('_', ' ').title()}: {value}" for key, value in prompt_dna.items()])}

## Mutation Notes

### What changed from the original prompt

{render_list("What changed", mutation_notes["what_changed"])}

### Why it changed

{mutation_notes["why_it_changed"]}

## Evolved Variants

{variant_lines}
"""
    OUTPUTS_DIR.mkdir(exist_ok=True)
    LATEST_OUTPUT.write_text(markdown, encoding="utf-8")
    append_jsonl(
        PROMPT_RUNS_FILE,
        {
            **original,
            "run_id": mutation_run_id,
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "parent_run_id": run_id,
            "mode": "mutate",
            "universal_prompt": evolved_variants[0],
            "model_specific_prompt": evolved_variants[0],
            "mutation_variants": evolved_variants,
            "latest_output": str(LATEST_OUTPUT),
        },
    )
    print(markdown)
    print(f"Saved mutation output to {LATEST_OUTPUT}")


def build_prompt_run_record(
    run_id: str,
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
    prompt_dna: dict,
    mutation_notes: dict,
) -> dict:
    """Build the saved generation record."""
    return {
        "run_id": run_id,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "subject": subject,
        "aesthetic": aesthetic_key,
        "location": location,
        "mood": mood,
        "camera": camera_key,
        "platform": platform_key,
        "model_profile": model_key,
        "lighting": lighting_key,
        "pose": pose_key,
        "universal_prompt": universal_prompt,
        "model_specific_prompt": model_specific_prompt,
        "prompt_dna": prompt_dna,
        "mutation_notes": mutation_notes,
        "latest_output": str(LATEST_OUTPUT),
    }


def main() -> None:
    """Run the interactive CLI."""
    aesthetics = load_json("aesthetics.json")
    cameras = load_json("cameras.json")
    lighting = load_json("lighting.json")
    poses = load_json("poses.json")
    negative_prompt = load_negative_prompt()
    random_mode = has_command("--random", "random")
    evolve_mode = has_command("--evolve", "evolve")

    maybe_print_list_and_exit(aesthetics, cameras)
    if has_command("--history", "history"):
        show_history()
        return
    if has_command("--review", "review"):
        review_prompt_run()
        return
    if has_command("--best", "best"):
        show_best()
        return
    if has_command("--analyze", "analyze"):
        analyze_reviewed_runs()
        return
    if has_command("--mutate", "mutate"):
        mutate_prompt_run()
        return

    print("Prompt Engine")
    print("Generate hyper-realistic social media image prompts.\n")
    print("Tip: run `python src/generate_prompt.py --list` to view options.")
    print("Tip: run `python src/generate_prompt.py --random` to randomize aesthetic, camera, lighting, and pose.\n")
    print("Tip: run `python src/generate_prompt.py --evolve` to bias prompts toward learned winners.\n")

    subject = ask("Subject", "a stylish person with realistic skin texture")
    if evolve_mode:
        learned_patterns = load_learned_patterns()
        selections = build_evolved_selection(learned_patterns, aesthetics, cameras, lighting, poses)
        aesthetic_key = selections["aesthetic"]
        camera_key = selections["camera"]
        lighting_key = selections["lighting"]
        pose_key = selections["pose"]
        print("\nEvolved selections")
        print(f"  Aesthetic: {aesthetic_key}")
        print(f"  Camera: {camera_key}")
        print(f"  Lighting: {lighting_key}")
        print(f"  Pose: {pose_key}")
        if not learned_patterns:
            print("  No learned patterns found yet; using random fallback.")
    elif random_mode:
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
    run_id = uuid.uuid4().hex[:12]
    prompt_dna = build_prompt_dna(
        aesthetic_key,
        camera_key,
        platform_key,
        lighting_key,
        mood,
        aesthetics,
        cameras,
        lighting,
    )
    if evolve_mode:
        mutation_notes = build_mutation_notes(
            "This prompt uses learned pattern bias from reviewed high-scoring runs.",
            [
                "Selected historically stronger aesthetic, camera, or lighting when available.",
                "Kept identity and platform requirements unchanged.",
                "Used learned direction while preserving beginner-friendly prompt structure.",
            ],
        )
    else:
        mutation_notes = build_mutation_notes(
            "Fresh generation; no parent prompt was mutated.",
            ["Created baseline prompt DNA for future testing and evolution."],
        )

    markdown = render_markdown(
        run_id,
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
        prompt_dna,
        mutation_notes,
        variations,
        captions,
        scorecard,
    )

    OUTPUTS_DIR.mkdir(exist_ok=True)
    LATEST_OUTPUT.write_text(markdown, encoding="utf-8")
    append_jsonl(
        PROMPT_RUNS_FILE,
        build_prompt_run_record(
            run_id,
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
            prompt_dna,
            mutation_notes,
        ),
    )

    print("\n" + markdown)
    print(f"Saved to {LATEST_OUTPUT}")
    print(f"Tracked run in {PROMPT_RUNS_FILE}")


if __name__ == "__main__":
    main()
