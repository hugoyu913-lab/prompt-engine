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
  iphone_portrait: {
    label: "iPhone portrait mode",
    look: "current smartphone realism, slight computational depth, crisp face detail, familiar vertical framing, natural social-media polish"
  },
  canon_r5_50mm: {
    label: "Canon R5 with 50mm lens",
    look: "sharp full-frame portrait, natural compression, detailed skin texture, creamy but believable background separation"
  },
  sony_a7siii_35mm: {
    label: "Sony A7S III with 35mm lens",
    look: "cinematic low-light realism, clean shadows, documentary perspective, strong night detail without looking rendered"
  },
  fuji_x100v: {
    label: "Fujifilm X100V",
    look: "compact street photography feel, film-like color, honest detail, natural highlight rolloff, candid framing"
  },
  contax_t2: {
    label: "Contax T2 film camera",
    look: "premium point-and-shoot film look, organic grain, soft highlight rolloff, realistic flash and imperfect focus"
  },
  ricoh_gr_iii: {
    label: "Ricoh GR III",
    look: "wide candid street-photo realism, compact-camera immediacy, textured detail, slightly raw everyday perspective"
  }
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
  instagram_vertical_post: {
    label: "Instagram vertical post",
    format: "4:5 vertical crop, strong first-glance composition, feed-ready polish",
    caption: "grid"
  },
  tiktok_slideshow: {
    label: "TikTok slideshow",
    format: "9:16 vertical composition, bold subject read, clear story-frame energy",
    caption: "slideshow"
  },
  x_twitter_image: {
    label: "X/Twitter image",
    format: "wide 16:9 or 3:2 crop, readable thumbnail, sharp central subject",
    caption: "timeline"
  },
  pinterest_pin: {
    label: "Pinterest pin",
    format: "2:3 vertical crop, aspirational detail, save-worthy lifestyle framing",
    caption: "pin"
  },
  album_cover: {
    label: "album cover",
    format: "square 1:1 crop, iconic central image, negative space for title placement",
    caption: "cover"
  }
};

const models = {
  midjourney: {
    label: "Midjourney",
    instruction: "Use compact visual phrases, strong photographic tags, and clear aspect-ratio guidance.",
    suffix: "--style raw --v 6"
  },
  chatgpt_image: {
    label: "ChatGPT image generation",
    instruction: "Use natural-language direction with explicit realism, identity, camera, and composition constraints.",
    suffix: ""
  },
  stable_diffusion_flux: {
    label: "Stable Diffusion / Flux",
    instruction: "Use weighted detail-friendly phrasing, concrete camera terms, and keep negatives separate.",
    suffix: "high detail, natural skin texture, realistic photography"
  }
};

const negativePrompt = "AI-looking image, plastic skin, waxy face, over-smoothed texture, fake pores, missing pores, airbrushed face, rubber skin, distorted hands, extra fingers, missing fingers, fused fingers, broken anatomy, uneven eyes, warped face, uncanny smile, glassy eyes, crossed eyes, duplicate person, identity drift, bad teeth, melted clothing, impossible fabric folds, broken jewelry, fake logo, unreadable text, misspelled text, warped background signs, impossible shadows, mismatched reflections, over-sharpened details, oversaturated colors, harsh HDR, fantasy render, cartoon, anime, 3D render, CGI, doll-like face, overly perfect symmetry, beauty-filter face, blurry subject, noisy face, low-resolution image, watermark, signature, frame, border.";

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
  universalPrompt: document.querySelector("#universalPrompt"),
  modelPrompt: document.querySelector("#modelPrompt"),
  negativePrompt: document.querySelector("#negativePrompt"),
  identityLock: document.querySelector("#identityLock"),
  promptDna: document.querySelector("#promptDna"),
  variations: document.querySelector("#variations"),
  captions: document.querySelector("#captions"),
  status: document.querySelector("#status")
};

let latestOutput = "";

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
    modelKey: elements.model.value
  };
}

function buildUniversalPrompt(input) {
  const aesthetic = aesthetics[input.aestheticKey];
  const camera = cameras[input.cameraKey];
  const platform = platforms[input.platformKey];

  return `Hyper-realistic photograph of ${input.subject} in ${input.location}. Platform: ${platform.label}; compose as ${platform.format}. Aesthetic: ${labelFor(input.aestheticKey)}. Mood: ${input.mood}. ${aesthetic.description} Scene details: ${aesthetic.details.join(", ")}. Lighting: ${lighting[input.lightingKey]}; also preserve ${aesthetic.lighting}. Camera: ${camera.label}; ${camera.look}. Pose and expression: ${poses[input.poseKey]}, lived-in body language, no stiff model posing. Realism requirements: ${aesthetic.realism_notes.join(", ")}, natural pores, tiny skin imperfections, realistic facial asymmetry, grounded wardrobe texture, accurate hands, believable lens distortion, subtle background messiness, authentic social-media framing, not over-edited, not AI-looking.`;
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
    "Preserve the Chrome Hearts shirt as the wardrobe anchor.",
    "Do not add extra people unless requested.",
    "Do not glamorize so much that the person becomes a different identity."
  ];
}

function buildPromptDna(input) {
  const aesthetic = aesthetics[input.aestheticKey];
  const camera = cameras[input.cameraKey];
  return [
    `Realism style: ${aesthetic.realism_notes.join(", ")}`,
    `Camera language: ${camera.label}: ${camera.look}`,
    `Composition language: ${platforms[input.platformKey].format}`,
    `Aesthetic intensity: medium-strong ${labelFor(input.aestheticKey)} with grounded detail`,
    `Lighting behavior: ${lighting[input.lightingKey]}`,
    `Emotional tone: ${input.mood}`
  ];
}

function buildVariations(input) {
  const aesthetic = aesthetics[input.aestheticKey];
  const platform = platforms[input.platformKey];
  return [
    `Candid variant: ${input.subject} in ${input.location}, ${input.mood}, ${poses[input.poseKey]}, ${lighting[input.lightingKey]}, imperfect crop, slight motion, real skin texture, ${platform.format}.`,
    `Editorial variant: ${input.subject} in ${input.location}, ${aesthetic.lighting}, stronger wardrobe shape, visible shirt texture, intentional negative space, premium but realistic color grade, ${platform.format}.`,
    `Close atmosphere variant: ${input.subject}, tighter environmental frame, ${lighting[input.lightingKey]}, realistic fabric detail, readable neon walkway background, identity locked, non-AI-looking.`
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

function renderList(target, items, ordered = false) {
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

function generatePrompt() {
  const input = readInput();
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
  renderList(elements.variations, variations, true);
  renderList(elements.captions, captions);

  latestOutput = buildFullOutput({
    universalPrompt,
    modelPrompt,
    negativePrompt,
    identityLock,
    promptDna,
    variations,
    captions
  });
  setStatus("Generated");
}

function setStatus(text) {
  elements.status.textContent = text;
}

async function copyText(text, label) {
  if (!text) {
    setStatus("Nothing to copy");
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
    setStatus(`${label} copied`);
  } catch (error) {
    setStatus("Copy blocked");
  }
}

function randomKey(data) {
  const keys = Object.keys(data);
  return keys[Math.floor(Math.random() * keys.length)];
}

function randomize() {
  elements.aesthetic.value = randomKey(aesthetics);
  elements.camera.value = randomKey(cameras);
  elements.lighting.value = randomKey(lighting);
  elements.pose.value = randomKey(poses);
  generatePrompt();
}

function clearForm() {
  elements.subject.value = "";
  elements.location.value = "";
  elements.mood.value = "";
  generatePrompt();
  setStatus("Cleared");
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
    generatePrompt();
  });
  document.querySelector("#randomize").addEventListener("click", randomize);
  document.querySelector("#clear").addEventListener("click", clearForm);
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

  generatePrompt();
}

init();
