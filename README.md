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
├── data/
│   ├── prompt_runs.jsonl
│   ├── image_reviews.jsonl
│   └── learned_patterns.json
├── examples/
│   └── example_outputs.md
├── server/
│   ├── app.py
│   └── garment_extractor.py
├── web/
│   ├── index.html
│   ├── styles.css
│   └── app.js
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

## Web Interface

Prompt Engine includes a local static website. Open this file in your browser:

```text
web/index.html
```

The web app uses the same presets as the Python project, with defaults tuned for a back-facing candid Chrome Hearts nightlife prompt.

## URL Garment Extraction

Paste any clothing product URL into the **Product URL** field and click **Extract from URL**. The backend fetches the page and auto-fills all garment fields (brand, name, type, color, fit, material, front/back design, logo placement, must preserve, must avoid). Extracted product images appear as clickable thumbnails.

### Run the backend

Install dependencies once:

```bash
pip install -r requirements.txt
```

Start the backend server (keep this terminal open):

```bash
python server/app.py
```

The backend runs at `http://localhost:5050`. The web UI connects to it automatically.

### Open the website

Open `web/index.html` in your browser. No additional server is needed for the UI itself.

### Use URL extraction

1. Paste a product URL into the **Product URL** field in the Garment Reference panel.
2. Click **Extract from URL**.
3. Wait a moment — all garment fields auto-fill from the product page.
4. Edit any field manually after extraction.
5. Extracted product images appear as thumbnails below the URL field.

**Reference Image Reminder:** For exact logos, prints, or graphics, upload one of the extracted product images directly to your image model as a visual reference. Text prompts alone cannot guarantee exact reproduction of specific logos or graphics.

### Supported extraction sources

- JSON-LD product schema (`@type: Product`)
- Open Graph tags (`og:title`, `og:description`, `og:image`)
- Meta tags (`name`, `description`, `brand`)
- Page title and `<h1>`
- Product description text (color, fit, material, design details inferred)
- Inline script JSON blobs and `<img>` tags (for product images)

### Error handling

| Error | Cause | Fix |
|-------|-------|-----|
| Cannot reach backend | Server not running | Run `python server/app.py` |
| 403 Forbidden | Site blocks scrapers | Try a different product page or brand |
| 404 Not Found | Bad URL | Check the URL in your browser |
| Timeout | Slow or blocking site | Try again or use a different URL |
| Could not auto-extract | No structured data | Fill missing fields manually |

The CLI asks for:

- subject
- aesthetic
- location
- mood
- camera
- platform
- model profile

Press Enter to use the suggested default when one is shown. The final result includes clean copy-paste prompts, universal prompt, model-specific prompt, negative prompt, identity lock, three variations, captions, and an image review scorecard.

To list available aesthetics and cameras without generating a prompt:

```bash
python src/generate_prompt.py --list
```

During aesthetic or camera selection, type `list` to show available options again. If an option does not exist, the CLI asks again instead of silently using the wrong preset.

To randomize aesthetic, camera, lighting, and pose while still entering subject, location, mood, platform, and model profile:

```bash
python src/generate_prompt.py --random
```

## Prompt Testing Lab

Every generated prompt gets a unique `run_id`, writes the Markdown output to `outputs/latest_prompt.md`, and appends a tracking record to `data/prompt_runs.jsonl`.

Show recent prompt runs:

```bash
python src/generate_prompt.py --history
```

Review a generated image by `run_id`:

```bash
python src/generate_prompt.py --review
```

The review flow saves realism, aesthetic, identity, postability, notes, failure points, and improvement ideas to `data/image_reviews.jsonl`.

Show the highest scoring reviewed runs:

```bash
python src/generate_prompt.py --best
```

Scores use the average of realism, aesthetic, identity, and postability.

## Prompt Evolution System

Analyze reviewed runs and save learned winners:

```bash
python src/generate_prompt.py --analyze
```

The analysis writes `data/learned_patterns.json` with highest scoring aesthetics, cameras, lighting setups, platforms, and common traits among strong runs.

Generate a future prompt biased toward learned successful styles:

```bash
python src/generate_prompt.py --evolve
```

Create evolved variants from an existing run while preserving identity:

```bash
python src/generate_prompt.py --mutate
```

Every normal, evolved, and mutated prompt keeps a `run_id`, saves `outputs/latest_prompt.md`, and can be reviewed later.

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

## Quality Modes

- `pfp_mode`
- `candid_realism`
- `outfit_focus`
- `atmosphere_focus`
- `editorial_realism`

## Available Aesthetics

- `nightlife_flash`
- `rarely_online_flash`
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
