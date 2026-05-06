# Prompt Engine

Prompt Engine is a small Python CLI that generates hyper-realistic aesthetic social media image prompts. It combines a subject, aesthetic, location, mood, camera style, and platform into a polished prompt designed for believable photography, cinematic lighting, realistic skin texture, and non-AI-looking results.

The MVP uses only the Python standard library. Generated prompts are saved automatically to `outputs/latest_prompt.md`.

## Folder Structure

```text
prompt-engine/
├── prompts/
│   ├── base_template.md
│   └── negative_prompt.md
├── presets/
│   ├── aesthetics.json
│   ├── cameras.json
│   ├── lighting.json
│   └── poses.json
├── outputs/
│   └── .gitkeep
├── examples/
│   └── example_outputs.md
├── src/
│   └── generate_prompt.py
├── README.md
└── requirements.txt
```

## How To Run

From the project root:

```bash
python src/generate_prompt.py
```

The CLI asks for:

- subject
- aesthetic
- location
- mood
- camera
- platform
- model profile

Press Enter to use the suggested default when one is shown. The final result includes a universal prompt, model-specific prompt, negative prompt, identity lock, three variations, captions, and an image review scorecard.

To list available aesthetics and cameras without generating a prompt:

```bash
python src/generate_prompt.py --list
```

During aesthetic or camera selection, type `list` to show available options again. If an option does not exist, the CLI asks again instead of silently using the wrong preset.

To randomize aesthetic, camera, lighting, and pose while still entering subject, location, mood, platform, and model profile:

```bash
python src/generate_prompt.py --random
```

## Platform Modes

- `instagram_vertical_post`
- `tiktok_slideshow`
- `x_twitter_image`
- `pinterest_pin`
- `album_cover`

## Model Profiles

- `midjourney`
- `chatgpt_image`
- `stable_diffusion_flux`

## Available Aesthetics

- `nightlife_flash`
- `quiet_luxury`
- `tokyo_streetwear`
- `gym_discipline`
- `soft_pinterest`
- `cyber_grunge`
- `old_money`
- `candid_digital_camera`
- `cinematic_lonely`
- `fashion_editorial`
- `desert_minimal`
- `miami_flash`
- `clean_creator`
- `coastal_film`
- `downtown_model_off_duty`

## Roadmap Ideas

- Add command-line flags for non-interactive generation.
- Add more platform-specific prompt formatting.
- Add saved prompt history with timestamps.
- Add preset scoring for stronger aesthetic matching.
- Add batch generation from CSV or JSON input.
- Add optional web UI.
- Add prompt export formats for Midjourney, DALL-E, Flux, and Stable Diffusion.
