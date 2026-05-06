const aesthetics = {
  nightlife_flash: {
    description: "Raw direct-flash nightlife photography with dark rooms, reflective skin, crowded backgrounds, and real party movement instead of polished studio posing.",
    lighting: "hard on-camera flash mixed with low ambient club light, crisp face highlights, deep falloff behind the subject",
    details: ["club entrance", "wristband", "slight motion blur", "glossy skin", "crowded background"],
    realism_notes: ["flash shadow behind jawline", "slightly imperfect crop", "visible skin texture"]
  },
  quiet_luxury: {
    description: "Understated premium lifestyle photography with calm confidence, expensive natural textures, neutral colors, and restrained composition.",
    lighting: "soft side-window light with gentle shadow detail and no harsh beauty retouching",
    details: ["cashmere", "tailored basics", "brushed metal watch", "stone interior", "clean negative space"],
    realism_notes: ["natural fabric wrinkles", "subtle under-eye texture", "realistic room reflections"]
  },
  tokyo_streetwear: {
    description: "Dense urban street fashion with layered silhouettes, practical city light, real pavement texture, and a candid Tokyo-night feel.",
    lighting: "mixed neon signs, vending-machine glow, and streetlamp spill with realistic color contamination",
    details: ["crosswalks", "convenience store glow", "layered silhouettes", "rain-slick pavement", "background pedestrians"],
    realism_notes: ["uneven street light on face", "slight background blur", "natural clothing folds"]
  },
  gym_discipline: {
    description: "Focused training photography with physical effort, sweat, equipment wear, chalk, and disciplined body language.",
    lighting: "industrial overhead gym light with controlled contrast and practical highlights on sweat",
    details: ["chalk dust", "metal equipment", "sweat texture", "focused expression", "rubber floor"],
    realism_notes: ["redness in skin", "creased workout clothing", "realistic grip tension"]
  },
  soft_pinterest: {
    description: "Soft lifestyle imagery with calm domestic detail, muted colors, clean styling, and believable casual composition.",
    lighting: "diffused daylight with warm bounce from interior walls and soft background falloff",
    details: ["linen textures", "coffee tones", "soft background", "clean composition", "morning light"],
    realism_notes: ["stray hair", "natural hand placement", "soft but visible pores"]
  },
  cyber_grunge: {
    description: "Gritty future-street styling with techwear, scratched surfaces, neon spill, and grounded documentary realism.",
    lighting: "neon rim light, dirty practical light, and high-contrast shadows without fantasy glow",
    details: ["scratched surfaces", "underground setting", "techwear", "wet concrete", "visible cables"],
    realism_notes: ["dirty floor texture", "imperfect makeup", "realistic neon reflections"]
  },
  old_money: {
    description: "Classic heritage styling with tailored clothing, ivy architecture, vintage leisure cues, and timeless restraint.",
    lighting: "golden afternoon light with soft shadows and warm architectural bounce",
    details: ["tailored blazer", "vintage car", "ivy architecture", "leather shoes", "subtle confidence"],
    realism_notes: ["worn leather texture", "natural hair flyaways", "soft eye wrinkles"]
  },
  candid_digital_camera: {
    description: "Early digital-camera social photography with imperfect flash, casual framing, real friend-group energy, and snapshot authenticity.",
    lighting: "compact-camera flash with ambient spill and small hard catchlights",
    details: ["slight red-eye risk", "real snapshot framing", "casual pose", "date-night energy", "messy background"],
    realism_notes: ["minor blur", "uneven exposure", "authentic flash shine"]
  },
  cinematic_lonely: {
    description: "Moody solitary photography with quiet negative space, practical light sources, filmic color, and restrained emotion.",
    lighting: "single practical light with soft falloff, muted shadows, and natural darkness",
    details: ["empty street", "distant background", "reflective mood", "subtle grain", "wide negative space"],
    realism_notes: ["low-light noise", "soft background detail", "natural posture fatigue"]
  },
  fashion_editorial: {
    description: "Magazine-grade fashion photography with precise styling, controlled light, sharp wardrobe detail, and human realism intact.",
    lighting: "large softbox key with sculpted fill, controlled shadows, and realistic skin highlights",
    details: ["intentional pose", "premium wardrobe", "clean backdrop", "sharp styling", "editorial crop"],
    realism_notes: ["visible textile weave", "skin texture preserved", "natural asymmetry"]
  },
  desert_minimal: {
    description: "Sparse desert lifestyle photography with sun-washed tones, simple silhouettes, open space, and quiet confidence.",
    lighting: "low desert sun with warm rim light, pale sky bounce, and dry natural shadows",
    details: ["sand texture", "linen outfit", "distant mountains", "minimal styling", "wind movement"],
    realism_notes: ["squint from sunlight", "dust on shoes", "wind-touched hair"]
  },
  miami_flash: {
    description: "Glossy coastal nightlife photography with direct flash, humid skin, colorful interiors, and vacation-party realism.",
    lighting: "direct flash over warm bar lights, reflective surfaces, and saturated but believable color",
    details: ["palm shadows", "chrome bar detail", "humid skin glow", "white outfit", "bright wall color"],
    realism_notes: ["flash reflection on skin", "slight color cast", "realistic background clutter"]
  },
  clean_creator: {
    description: "Modern creator portrait with bright workspace detail, natural tech objects, polished but believable personal-brand styling.",
    lighting: "clean window light mixed with soft monitor glow and gentle shadow detail",
    details: ["desk setup", "laptop glow", "minimal outfit", "organized workspace", "natural posture"],
    realism_notes: ["screen reflections", "minor desk clutter", "realistic hand position"]
  },
  coastal_film: {
    description: "Relaxed coastal film photography with salt-air texture, soft color, wind movement, and nostalgic realism.",
    lighting: "soft beach haze with warm backlight and low-contrast filmic shadows",
    details: ["windy hair", "washed cotton", "shoreline", "film grain", "sun-faded colors"],
    realism_notes: ["sand on fabric", "skin redness from sun", "organic film grain"]
  },
  downtown_model_off_duty: {
    description: "Off-duty street style with realistic city errands, confident casual clothing, paparazzi-adjacent framing, and natural movement.",
    lighting: "open shade between buildings with street reflections and neutral daylight",
    details: ["coffee cup", "sunglasses", "oversized coat", "city sidewalk", "passing traffic"],
    realism_notes: ["walking motion", "natural jaw tension", "wrinkled outerwear"]
  }
};

const cameras = {
  iphone_portrait: { label: "iPhone portrait mode", look: "current smartphone realism, slight computational depth, crisp face detail, familiar vertical framing, natural social-media polish" },
  canon_r5_50mm: { label: "Canon R5 with 50mm lens", look: "sharp full-frame portrait, natural compression, detailed skin texture, creamy but believable background separation" },
  sony_a7siii_35mm: { label: "Sony A7S III with 35mm lens", look: "cinematic low-light realism, clean shadows, documentary perspective, strong night detail without looking rendered" },
  fuji_x100v: { label: "Fujifilm X100V", look: "compact street photography feel, film-like color, honest detail, natural highlight rolloff, candid framing" },
  contax_t2: { label: "Contax T2 film camera", look: "premium point-and-shoot film look, organic grain, soft highlight rolloff, realistic flash and imperfect focus" },
  ricoh_gr_iii: { label: "Ricoh GR III", look: "wide candid street-photo realism, compact-camera immediacy, textured detail, slightly raw everyday perspective" }
};

const lighting = {
  cinematic_window: "soft cinematic window light, natural falloff, realistic catchlights",
  direct_flash: "direct on-camera flash, crisp shadows, glossy highlights, nightlife realism",
  golden_hour: "low golden-hour sun, warm edge light, long natural shadows",
  neon_night: "neon practical lights, colored rim light, dark ambient contrast",
  overcast_soft: "large overcast sky light, soft shadows, even skin tones",
  studio_editorial: "large softbox key light, subtle fill, clean editorial contrast",
  gym_overhead: "industrial overhead lighting, realistic sweat highlights, controlled contrast",
  practical_lamp: "single practical lamp source, intimate shadows, cinematic warmth"
};

const poses = {
  candid_glance: "candid glance away from camera, relaxed shoulders, natural expression",
  walking_frame: "mid-step walking pose, slight motion in clothing, documentary realism",
  seated_composed: "seated composed posture, calm hands, confident eye line",
  mirror_check: "casual mirror-check pose, believable phone angle, natural body language",
  leaning_wall: "leaning against wall, one shoulder relaxed, subtle confidence",
  post_workout: "post-workout stance, controlled breathing, focused expression",
  editorial_profile: "three-quarter editorial profile, clean neck line, intentional gaze",
  laughing_candid: "mid-laugh candid moment, imperfect expression, authentic energy"
};

const platforms = {
  instagram_vertical_post: { label: "Instagram vertical post", format: "4:5 vertical crop, strong first-glance composition, feed-ready polish", caption: "grid" },
  tiktok_slideshow: { label: "TikTok slideshow", format: "9:16 vertical composition, bold subject read, clear story-frame energy", caption: "slideshow" },
  x_twitter_image: { label: "X/Twitter image", format: "wide 16:9 or 3:2 crop, readable thumbnail, sharp central subject", caption: "timeline" },
  pinterest_pin: { label: "Pinterest pin", format: "2:3 vertical crop, aspirational detail, save-worthy lifestyle framing", caption: "pin" },
  album_cover: { label: "album cover", format: "square 1:1 crop, iconic central image, negative space for title placement", caption: "cover" }
};

const models = {
  midjourney: { label: "Midjourney", instruction: "Use compact visual phrases, strong photographic tags, and clear aspect-ratio guidance.", suffix: "--style raw --v 6" },
  chatgpt_image: { label: "ChatGPT image generation", instruction: "Use natural-language direction with explicit realism, identity, camera, and composition constraints.", suffix: "" },
  stable_diffusion_flux: { label: "Stable Diffusion / Flux", instruction: "Use weighted detail-friendly phrasing, concrete camera terms, and keep negatives separate.", suffix: "high detail, natural skin texture, realistic photography" }
};

const quickPresets = {
  lonely_night_walk: {
    subject: "back-facing candid photo of a lone person in a dark oversized coat",
    aesthetic: "cinematic_lonely",
    camera: "sony_a7siii_35mm",
    lighting: "neon_night",
    pose: "walking_frame",
    location: "empty neon walkway after rain",
    mood: "distant, cinematic, and emotionally quiet",
    strengths: [9, 9, 9, 2, 10, 8]
  },
  underground_flash: {
    subject: "back-facing candid photo of a person leaving an underground club",
    aesthetic: "nightlife_flash",
    camera: "contax_t2",
    lighting: "direct_flash",
    pose: "candid_glance",
    location: "basement venue stairwell with stickers and concrete walls",
    mood: "raw, loud, and private",
    strengths: [8, 10, 8, 1, 8, 9]
  },
  chrome_hearts_fit: {
    subject: "back-facing candid photo of a person wearing a Chrome Hearts shirt",
    aesthetic: "nightlife_flash",
    camera: "ricoh_gr_iii",
    lighting: "neon_night",
    pose: "candid_glance",
    location: "neon night walkway outside a packed club",
    mood: "confident, anonymous, and cinematic",
    strengths: [8, 9, 8, 4, 8, 8]
  },
  detached_editorial: {
    subject: "detached fashion portrait of a person in black designer layers",
    aesthetic: "fashion_editorial",
    camera: "canon_r5_50mm",
    lighting: "studio_editorial",
    pose: "editorial_profile",
    location: "minimal concrete studio with one practical light",
    mood: "reserved, expensive, and emotionally distant",
    strengths: [9, 3, 7, 9, 9, 4]
  },
  candid_city_walk: {
    subject: "candid street photo of a person walking away in layered streetwear",
    aesthetic: "downtown_model_off_duty",
    camera: "fuji_x100v",
    lighting: "overcast_soft",
    pose: "walking_frame",
    location: "downtown sidewalk with traffic blur and storefront reflections",
    mood: "unbothered, fast, and cool",
    strengths: [8, 10, 5, 5, 6, 7]
  }
};

const negativePrompt = "AI-looking image, plastic skin, waxy face, over-smoothed texture, fake pores, missing pores, airbrushed face, rubber skin, distorted hands, extra fingers, missing fingers, fused fingers, broken anatomy, uneven eyes, warped face, uncanny smile, glassy eyes, crossed eyes, duplicate person, identity drift, bad teeth, melted clothing, impossible fabric folds, broken jewelry, fake logo, unreadable text, misspelled text, warped background signs, impossible shadows, mismatched reflections, over-sharpened details, oversaturated colors, harsh HDR, fantasy render, cartoon, anime, 3D render, CGI, doll-like face, overly perfect symmetry, beauty-filter face, blurry subject, noisy face, low-resolution image, watermark, signature, frame, border.";
const storageKey = "prompt-engine-web-runs";
const favoritesKey = "prompt-engine-web-favorites";

const elements = {
  form: document.querySelector("#promptForm"),
  subject: document.querySelector("#subject"),
  aesthetic: document.querySelector("#aesthetic"),
  camera: document.querySelector("#camera"),
  lighting: document.querySelector("#lighting"),
  pose: document.querySelector("#pose"),
  location: document.querySelector("#location"),
  mood: document.querySelector("#mood"),
  platform: document.querySelector("#platform"),
  model: document.querySelector("#model"),
  strengths: {
    realism: document.querySelector("#realismStrength"),
    candidness: document.querySelector("#candidnessStrength"),
    darkness: document.querySelector("#darknessStrength"),
    luxury: document.querySelector("#luxuryStrength"),
    distance: document.querySelector("#distanceStrength"),
    imperfection: document.querySelector("#imperfectionStrength")
  },
  universalPrompt: document.querySelector("#universalPrompt"),
  modelPrompt: document.querySelector("#modelPrompt"),
  negativePrompt: document.querySelector("#negativePrompt"),
  identityLock: document.querySelector("#identityLock"),
  promptDna: document.querySelector("#promptDna"),
  variations: document.querySelector("#variations"),
  captions: document.querySelector("#captions"),
  status: document.querySelector("#status"),
  toast: document.querySelector("#toast"),
  recentRuns: document.querySelector("#recentRuns"),
  previewAesthetic: document.querySelector("#previewAesthetic"),
  previewSubject: document.querySelector("#previewSubject"),
  previewMeta: document.querySelector("#previewMeta"),
  previewMood: document.querySelector("#previewMood"),
  previewPlatform: document.querySelector("#previewPlatform"),
  generateButton: document.querySelector("#generateButton")
};

let latestOutput = "";
let latestParts = null;

function labelFor(key) {
  return key.replaceAll("_", " ");
}

function fillSelect(select, data, selected) {
  select.innerHTML = "";
  Object.entries(data).forEach(([key, value]) => {
    const option = document.createElement("option");
    option.value = key;
    option.textContent = value.label ? `${value.label} (${key})` : labelFor(key);
    select.appendChild(option);
  });
  select.value = selected;
}

function readInput() {
  return {
    subject: elements.subject.value.trim() || "back-facing candid photo of a person wearing a Chrome Hearts shirt",
    aestheticKey: elements.aesthetic.value,
    cameraKey: elements.camera.value,
    lightingKey: elements.lighting.value,
    poseKey: elements.pose.value,
    location: elements.location.value.trim() || "neon night walkway outside a packed club",
    mood: elements.mood.value.trim() || "confident, anonymous, and cinematic",
    platformKey: elements.platform.value,
    modelKey: elements.model.value,
    strengths: Object.fromEntries(Object.entries(elements.strengths).map(([key, input]) => [key, Number(input.value)]))
  };
}

function strengthWording(strengths) {
  const words = [];
  if (strengths.realism >= 7) words.push("documentary-grade realism, preserved pores, natural facial asymmetry, real lens behavior");
  if (strengths.candidness >= 7) words.push("snapshot realism, unposed timing, casual body language, reduced editorial stiffness");
  if (strengths.darkness >= 7) words.push("underexposed edges, deep shadows, night contrast, practical light falloff");
  if (strengths.luxury >= 7) words.push("quiet luxury restraint, premium fabric texture, expensive simplicity");
  if (strengths.distance >= 7) words.push("emotionally distant posture, anonymous presence, face partially withheld");
  if (strengths.imperfection >= 7) words.push("motion blur, analog noise, imperfect framing, slight underexposure, real-world messiness");
  if (!words.length) words.push("balanced realism with clean social-media composition");
  return words.join("; ");
}

function buildUniversalPrompt(input) {
  const aesthetic = aesthetics[input.aestheticKey];
  const camera = cameras[input.cameraKey];
  const platform = platforms[input.platformKey];
  return `Hyper-realistic photograph of ${input.subject} in ${input.location}. Platform: ${platform.label}; compose as ${platform.format}. Aesthetic: ${labelFor(input.aestheticKey)}. Mood: ${input.mood}. ${aesthetic.description} Scene details: ${aesthetic.details.join(", ")}. Lighting: ${lighting[input.lightingKey]}; also preserve ${aesthetic.lighting}. Camera: ${camera.label}; ${camera.look}. Pose and expression: ${poses[input.poseKey]}, lived-in body language, no stiff model posing. Creative direction strength: ${strengthWording(input.strengths)}. Realism requirements: ${aesthetic.realism_notes.join(", ")}, natural pores, tiny skin imperfections, realistic facial asymmetry, grounded wardrobe texture, accurate hands, believable lens distortion, subtle background messiness, authentic social-media framing, not over-edited, not AI-looking.`;
}

function buildModelPrompt(universalPrompt, input) {
  const model = models[input.modelKey];
  const platform = platforms[input.platformKey];
  const suffix = model.suffix ? ` ${model.suffix}` : "";
  return `${model.instruction} ${universalPrompt} Prioritize believable photography, identity consistency, and ${platform.format}.${suffix}`;
}

function buildIdentityLock(subject) {
  return [
    `Keep the same core subject: ${subject}.`,
    "Preserve face shape, apparent age range, body type, skin tone, hair length, and hair color.",
    "Preserve the back-facing candid angle unless deliberately changed.",
    "Preserve the Chrome Hearts shirt as the wardrobe anchor when present.",
    "Do not add extra people unless requested.",
    "Do not glamorize so much that the person becomes a different identity."
  ];
}

function buildPromptDna(input) {
  const aesthetic = aesthetics[input.aestheticKey];
  const camera = cameras[input.cameraKey];
  return [
    `Realism style: ${aesthetic.realism_notes.join(", ")}; strength ${input.strengths.realism}/10`,
    `Camera language: ${camera.label}: ${camera.look}`,
    `Composition language: ${platforms[input.platformKey].format}`,
    `Aesthetic intensity: ${input.strengths.luxury >= 7 ? "luxury-forward" : "grounded"} ${labelFor(input.aestheticKey)}`,
    `Lighting behavior: ${lighting[input.lightingKey]}; darkness ${input.strengths.darkness}/10`,
    `Emotional tone: ${input.mood}; distance ${input.strengths.distance}/10`,
    `Imperfection layer: ${input.strengths.imperfection}/10`
  ];
}

function buildVariations(input) {
  const aesthetic = aesthetics[input.aestheticKey];
  const platform = platforms[input.platformKey];
  const candid = input.strengths.candidness >= 7 ? "more accidental timing, less posed energy" : "controlled but natural timing";
  const imperfect = input.strengths.imperfection >= 7 ? "motion blur, analog noise, underexposed edges, imperfect crop" : "clean detail with subtle imperfections";
  return [
    `Candid variant: ${input.subject} in ${input.location}, ${input.mood}, ${poses[input.poseKey]}, ${lighting[input.lightingKey]}, ${candid}, ${imperfect}, ${platform.format}.`,
    `Atmosphere variant: ${input.subject} in ${input.location}, ${aesthetic.lighting}, environmental reflections, background texture, practical shadows, visible wardrobe detail, ${platform.format}.`,
    `Detached variant: ${input.subject}, emotionally distant posture, face partially withheld, ${lighting[input.lightingKey]}, realistic fabric detail, identity locked, non-AI-looking.`
  ];
}

function buildCaptions(input) {
  return [
    `${input.mood.charAt(0).toUpperCase() + input.mood.slice(1)}, but keep it effortless.`,
    `${labelFor(input.aestheticKey)} frame with real-life texture.`,
    "Back-facing, but still unmistakable.",
    `Saved this one for the ${platforms[input.platformKey].caption}.`,
    "Chrome, flash, motion.",
    "Looks unplanned. Was not."
  ];
}

function renderList(target, items) {
  target.innerHTML = "";
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    target.appendChild(li);
  });
}

function buildFullOutput(parts) {
  return [
    "# Prompt Engine Web Output",
    "",
    "## Universal Prompt",
    parts.universalPrompt,
    "",
    "## Model-Specific Prompt",
    parts.modelPrompt,
    "",
    "## Negative Prompt",
    parts.negativePrompt,
    "",
    "## Identity Lock",
    parts.identityLock.map((item) => `- ${item}`).join("\n"),
    "",
    "## Prompt DNA",
    parts.promptDna.map((item) => `- ${item}`).join("\n"),
    "",
    "## Variations",
    parts.variations.map((item, index) => `${index + 1}. ${item}`).join("\n"),
    "",
    "## Captions",
    parts.captions.map((item) => `- ${item}`).join("\n")
  ].join("\n");
}

function updatePreview(input) {
  elements.previewAesthetic.textContent = input.aestheticKey;
  elements.previewSubject.textContent = input.subject;
  elements.previewMeta.textContent = `${cameras[input.cameraKey].label} / ${input.location}`;
  elements.previewMood.textContent = input.mood;
  elements.previewPlatform.textContent = platforms[input.platformKey].label;
}

function setGenerating(isGenerating) {
  elements.generateButton.classList.toggle("generating", isGenerating);
  elements.generateButton.textContent = isGenerating ? "Generating" : "Generate Prompt";
}

function generatePrompt(saveRun = false) {
  const input = readInput();
  updatePreview(input);
  setGenerating(true);
  setStatus("Generating");

  window.setTimeout(() => {
    const universalPrompt = buildUniversalPrompt(input);
    const modelPrompt = buildModelPrompt(universalPrompt, input);
    const identityLock = buildIdentityLock(input.subject);
    const promptDna = buildPromptDna(input);
    const variations = buildVariations(input);
    const captions = buildCaptions(input);

    elements.universalPrompt.textContent = universalPrompt;
    elements.modelPrompt.textContent = modelPrompt;
    elements.negativePrompt.textContent = negativePrompt;
    renderList(elements.identityLock, identityLock);
    renderList(elements.promptDna, promptDna);
    renderList(elements.variations, variations);
    renderList(elements.captions, captions);

    latestParts = { input, universalPrompt, modelPrompt, negativePrompt, identityLock, promptDna, variations, captions };
    latestOutput = buildFullOutput(latestParts);
    setGenerating(false);
    setStatus("Generated");
    if (saveRun) saveCurrentPrompt(false);
  }, 260);
}

function setStatus(text) {
  elements.status.textContent = text;
}

function showToast(message) {
  elements.toast.textContent = message;
  elements.toast.classList.add("show");
  window.setTimeout(() => elements.toast.classList.remove("show"), 1600);
}

async function copyText(text, label) {
  if (!text) {
    showToast("Nothing to copy");
    return;
  }
  try {
    if (navigator.clipboard) {
      await navigator.clipboard.writeText(text);
    } else {
      const helper = document.createElement("textarea");
      helper.value = text;
      helper.style.position = "fixed";
      helper.style.opacity = "0";
      document.body.appendChild(helper);
      helper.select();
      document.execCommand("copy");
      helper.remove();
    }
    showToast(`${label} copied`);
  } catch (error) {
    showToast("Copy blocked by browser");
  }
}

function randomKey(data) {
  const keys = Object.keys(data);
  return keys[Math.floor(Math.random() * keys.length)];
}

function setStrengths(values) {
  const keys = ["realism", "candidness", "darkness", "luxury", "distance", "imperfection"];
  keys.forEach((key, index) => {
    elements.strengths[key].value = values[index];
  });
}

function applyPreset(name) {
  const preset = quickPresets[name];
  elements.subject.value = preset.subject;
  elements.aesthetic.value = preset.aesthetic;
  elements.camera.value = preset.camera;
  elements.lighting.value = preset.lighting;
  elements.pose.value = preset.pose;
  elements.location.value = preset.location;
  elements.mood.value = preset.mood;
  setStrengths(preset.strengths);
  generatePrompt();
}

function randomize() {
  elements.aesthetic.value = randomKey(aesthetics);
  elements.camera.value = randomKey(cameras);
  elements.lighting.value = randomKey(lighting);
  elements.pose.value = randomKey(poses);
  Object.values(elements.strengths).forEach((input) => {
    input.value = Math.floor(Math.random() * 5) + 5;
  });
  generatePrompt();
}

function clearForm() {
  elements.subject.value = "";
  elements.location.value = "";
  elements.mood.value = "";
  generatePrompt();
  setStatus("Cleared");
}

function loadJson(key) {
  try {
    return JSON.parse(localStorage.getItem(key)) || [];
  } catch (error) {
    return [];
  }
}

function saveJson(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function saveCurrentPrompt(favorite) {
  if (!latestParts) return;
  const run = {
    id: Date.now().toString(36),
    favorite,
    createdAt: new Date().toLocaleString(),
    title: latestParts.input.subject,
    aesthetic: latestParts.input.aestheticKey,
    camera: latestParts.input.cameraKey,
    output: latestOutput
  };
  const runs = [run, ...loadJson(storageKey)].slice(0, 12);
  saveJson(storageKey, runs);
  if (favorite) saveJson(favoritesKey, [run, ...loadJson(favoritesKey)].slice(0, 12));
  renderRecentRuns();
  showToast(favorite ? "Favorited" : "Saved");
}

function renderRecentRuns() {
  const runs = loadJson(storageKey);
  elements.recentRuns.innerHTML = "";
  if (!runs.length) {
    const empty = document.createElement("p");
    empty.className = "recent-empty";
    empty.textContent = "Saved prompts appear here.";
    elements.recentRuns.appendChild(empty);
    return;
  }
  runs.forEach((run) => {
    const item = document.createElement("article");
    item.className = "recent-item";
    item.innerHTML = `<strong>${run.aesthetic}</strong><small>${run.camera}</small><small>${run.createdAt}</small>`;
    item.addEventListener("click", () => copyText(run.output, "Saved prompt"));
    elements.recentRuns.appendChild(item);
  });
}

function init() {
  fillSelect(elements.aesthetic, aesthetics, "nightlife_flash");
  fillSelect(elements.camera, cameras, "ricoh_gr_iii");
  fillSelect(elements.lighting, lighting, "neon_night");
  fillSelect(elements.pose, poses, "candid_glance");
  fillSelect(elements.platform, platforms, "instagram_vertical_post");
  fillSelect(elements.model, models, "chatgpt_image");

  elements.form.addEventListener("submit", (event) => {
    event.preventDefault();
    generatePrompt(true);
  });
  document.querySelector("#randomize").addEventListener("click", randomize);
  document.querySelector("#clear").addEventListener("click", clearForm);
  document.querySelector("#savePrompt").addEventListener("click", () => saveCurrentPrompt(false));
  document.querySelector("#favoritePrompt").addEventListener("click", () => saveCurrentPrompt(true));
  document.querySelector("#clearRuns").addEventListener("click", () => {
    saveJson(storageKey, []);
    renderRecentRuns();
    showToast("Recent runs cleared");
  });
  document.querySelectorAll("[data-preset]").forEach((button) => {
    button.addEventListener("click", () => applyPreset(button.dataset.preset));
  });
  Object.values(elements.strengths).forEach((input) => {
    input.addEventListener("input", () => generatePrompt());
  });
  [
    elements.subject,
    elements.location,
    elements.mood,
    elements.aesthetic,
    elements.camera,
    elements.lighting,
    elements.pose,
    elements.platform,
    elements.model
  ].forEach((input) => {
    input.addEventListener("change", () => generatePrompt());
  });
  document.querySelectorAll("[data-copy]").forEach((button) => {
    button.addEventListener("click", () => {
      const target = button.dataset.copy;
      const map = {
        modelPrompt: elements.modelPrompt.textContent,
        negativePrompt: elements.negativePrompt.textContent,
        fullOutput: latestOutput
      };
      copyText(map[target], button.textContent.replace("Copy ", ""));
    });
  });

  renderRecentRuns();
  generatePrompt();
}

init();
