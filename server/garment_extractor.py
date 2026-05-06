import re
import json
import time
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

BROWSER_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Cache-Control': 'max-age=0',
}

GARMENT_TYPES = [
    ('t-shirt', ['t-shirt', 'tee shirt', ' tee ']),
    ('hoodie', ['hoodie', 'hooded sweatshirt']),
    ('sweatshirt', ['sweatshirt', 'crewneck']),
    ('bomber jacket', ['bomber jacket', 'bomber']),
    ('denim jacket', ['denim jacket']),
    ('jacket', ['track jacket', 'windbreaker', 'jacket']),
    ('coat', ['trench coat', 'overcoat', 'parka', 'coat']),
    ('shirt', ['button-up', 'button down', 'flannel shirt', 'dress shirt', 'shirt']),
    ('pants', ['pants', 'trousers']),
    ('jeans', ['jeans']),
    ('shorts', ['shorts']),
    ('joggers', ['joggers', 'sweatpants']),
    ('leggings', ['leggings']),
    ('dress', ['dress']),
    ('skirt', ['skirt']),
    ('sweater', ['sweater', 'knitwear', 'knit pullover']),
    ('cardigan', ['cardigan']),
    ('polo', ['polo shirt', 'polo']),
    ('tank top', ['tank top', 'singlet']),
    ('vest', ['vest', 'gilet']),
    ('jumpsuit', ['jumpsuit', 'romper']),
    ('tracksuit', ['tracksuit']),
    ('fleece', ['fleece jacket', 'fleece']),
    ('top', ['crop top', 'halter top']),
]

COLORS = [
    'black', 'white', 'grey', 'gray', 'red', 'blue', 'navy blue', 'navy',
    'green', 'beige', 'brown', 'tan', 'cream', 'ivory', 'off-white',
    'yellow', 'orange', 'purple', 'pink', 'burgundy', 'maroon', 'olive',
    'khaki', 'camel', 'stone', 'ecru', 'charcoal', 'natural', 'sand',
    'cobalt', 'teal', 'forest green', 'mint', 'coral', 'lavender', 'mauve',
    'rust', 'cognac', 'chocolate', 'bone', 'oatmeal', 'heather grey',
    'heather', 'slate', 'indigo',
]

FIT_KEYWORDS = [
    'oversized fit', 'slim fit', 'regular fit', 'relaxed fit', 'loose fit',
    'classic fit', 'athletic fit', 'comfort fit', 'straight fit',
    'oversized', 'slim', 'relaxed', 'loose', 'fitted', 'boxy', 'cropped',
    'baggy', 'wide-leg', 'tapered', 'skinny',
]

MATERIAL_KEYWORDS = [
    '100% cotton', 'organic cotton', 'french terry', 'waffle knit', 'rib knit',
    'terry cloth', 'cotton jersey', 'cotton fleece', 'cotton', 'polyester',
    'wool blend', 'wool', 'cashmere', 'silk', 'linen', 'denim', 'fleece',
    'nylon', 'spandex', 'elastane', 'rayon', 'jersey', 'velvet', 'corduroy',
    'tweed', 'canvas', 'leather', 'suede', 'modal', 'bamboo', 'hemp',
    'acrylic', 'mesh',
]


# ── HTTP fetch ───────────────────────────────────────────────────────────────

def validate_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https') and bool(parsed.netloc)
    except Exception:
        return False


def fetch_page(url: str, retries: int = 2):
    for attempt in range(retries):
        try:
            response = requests.get(
                url,
                headers=BROWSER_HEADERS,
                timeout=15,
                allow_redirects=True,
            )
            if response.status_code == 200:
                return response
            if response.status_code == 404:
                raise FileNotFoundError('Product page not found (404).')
            if response.status_code in (403, 429, 503):
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise PermissionError(
                    f'Site blocked scraping (HTTP {response.status_code}). '
                    'Try a different product page or brand.'
                )
            response.raise_for_status()
        except requests.exceptions.Timeout:
            if attempt < retries - 1:
                continue
            raise TimeoutError('Request timed out. The site may be slow or blocking requests.')
        except requests.exceptions.TooManyRedirects:
            raise ConnectionError('Too many redirects — page may require login.')
        except requests.exceptions.ConnectionError:
            raise ConnectionError('Could not connect to the URL. Check that it\'s a valid product page.')
        except (PermissionError, FileNotFoundError, TimeoutError, ConnectionError):
            raise
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f'Failed to fetch page: {e}')
    raise ConnectionError('Failed to fetch page after retries.')


# ── SSENSE extractor ─────────────────────────────────────────────────────────

def extract_ssense(soup, url: str) -> dict | None:
    next_data_tag = soup.find('script', {'id': '__NEXT_DATA__'})
    if not next_data_tag or not next_data_tag.string:
        return None

    try:
        next_data = json.loads(next_data_tag.string)
    except Exception:
        return None

    page_props = next_data.get('props', {}).get('pageProps', {})
    product = (
        page_props.get('product')
        or page_props.get('productProps', {}).get('product')
        or page_props.get('initialData', {}).get('product')
        or _find_product_in_dict(next_data)
    )

    if not product:
        return None

    result = {
        'brand': '',
        'product_name': '',
        'garment_type': '',
        'color': '',
        'fit': '',
        'material': '',
        'front_design': '',
        'back_design': '',
        'logo_text_placement': '',
        'image_urls': [],
        'description': '',
        'must_preserve': '',
        'must_avoid': '',
        'extraction_notes': ['Extracted via SSENSE __NEXT_DATA__.'],
    }

    # Brand
    brand_data = product.get('brand') or product.get('designerName') or {}
    if isinstance(brand_data, dict):
        result['brand'] = brand_data.get('name') or brand_data.get('brandName') or ''
    else:
        result['brand'] = str(brand_data)

    # Product name — strip brand prefix if present
    raw_name = product.get('name') or product.get('shortDescription') or ''
    brand_str = result['brand']
    if brand_str and raw_name.lower().startswith(brand_str.lower()):
        raw_name = raw_name[len(brand_str):].strip(' -–')
    result['product_name'] = raw_name

    # Description — strip HTML if present
    description = (
        product.get('description')
        or product.get('longDescription')
        or product.get('shortDescription')
        or ''
    )
    if '<' in description:
        desc_soup = BeautifulSoup(description, 'html.parser')
        description = desc_soup.get_text(separator=' ', strip=True)
    result['description'] = description

    # Color
    color = (
        product.get('color')
        or product.get('colourName')
        or product.get('selectedColor')
        or ''
    )
    if isinstance(color, dict):
        color = color.get('name') or color.get('label') or ''
    result['color'] = str(color)

    # Images
    images = product.get('images') or product.get('media') or []
    image_urls = []
    for img in images:
        if isinstance(img, dict):
            src = img.get('src') or img.get('url') or img.get('imageUrl') or ''
            if src:
                if src.startswith('//'):
                    src = 'https:' + src
                image_urls.append(src)
        elif isinstance(img, str) and img.startswith('http'):
            image_urls.append(img)
    result['image_urls'] = image_urls[:8]

    # Garment type from category
    category = (
        product.get('category')
        or product.get('categoryName')
        or product.get('productType')
        or ''
    )
    if isinstance(category, dict):
        category = category.get('name') or category.get('label') or ''
    result['garment_type'] = str(category)

    # Material
    material = (
        product.get('composition')
        or product.get('material')
        or product.get('fabric')
        or ''
    )
    if isinstance(material, list):
        material = ', '.join(material)
    result['material'] = str(material)

    # Fit
    result['fit'] = str(product.get('fit') or product.get('silhouette') or '')

    # Fill missing fields by inferring from description
    full_text = ' ' + (result['product_name'] + ' ' + description).lower() + ' '
    if not result['garment_type']:
        result['garment_type'] = _infer_garment_type(full_text)
    if not result['color']:
        result['color'] = _infer_color(full_text)
    if not result['fit']:
        result['fit'] = _infer_fit(full_text)
    if not result['material']:
        result['material'] = _infer_material(full_text)

    if description:
        _deep_parse_description(description, result)

    result['must_preserve'] = _build_must_preserve(result)
    result['must_avoid'] = _build_must_avoid(result)

    if not result['image_urls']:
        result['extraction_notes'].append('No product images found in __NEXT_DATA__.')

    missing = [f for f in ('brand', 'product_name', 'garment_type', 'color') if not result[f]]
    if missing:
        result['extraction_notes'].append(
            f'Could not auto-extract: {", ".join(missing)}. Fill in manually.'
        )

    return result


def _find_product_in_dict(data, depth: int = 0) -> dict | None:
    if depth > 6:
        return None
    if isinstance(data, dict):
        if data.get('name') and (
            data.get('brand') or data.get('description') or data.get('designerName')
        ):
            return data
        for value in data.values():
            found = _find_product_in_dict(value, depth + 1)
            if found:
                return found
    elif isinstance(data, list):
        for item in data:
            found = _find_product_in_dict(item, depth + 1)
            if found:
                return found
    return None


# ── Main entry point ─────────────────────────────────────────────────────────

def extract_garment(url: str) -> dict:
    if not validate_url(url):
        raise ValueError('Invalid URL — must start with http:// or https://')

    domain = urlparse(url).netloc.lower()
    response = fetch_page(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Domain-specific extractors
    if 'ssense.com' in domain:
        result = extract_ssense(soup, url)
        if result:
            return result
        # Fall through to generic if __NEXT_DATA__ had no product

    # ── Generic extraction pipeline ──────────────────────────────────────────

    result = {
        'brand': '',
        'product_name': '',
        'garment_type': '',
        'color': '',
        'fit': '',
        'material': '',
        'front_design': '',
        'back_design': '',
        'logo_text_placement': '',
        'image_urls': [],
        'description': '',
        'must_preserve': '',
        'must_avoid': '',
        'extraction_notes': [],
    }

    # 1. JSON-LD product schema
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            ld = json.loads(script.string or '')
            items = ld if isinstance(ld, list) else [ld]
            for item in items:
                if isinstance(item, dict) and item.get('@type') in (
                    'Product', 'https://schema.org/Product'
                ):
                    _apply_json_ld(result, item)
                    result['extraction_notes'].append('JSON-LD product schema found.')
                    break
        except (json.JSONDecodeError, AttributeError, TypeError):
            continue

    # 2. Open Graph / meta tags
    if not result['product_name']:
        result['product_name'] = _og(soup, 'og:title') or _page_title(soup)
    if not result['description']:
        result['description'] = (
            _og(soup, 'og:description') or _meta(soup, 'description') or ''
        )
    if not result['brand']:
        result['brand'] = _og(soup, 'og:brand') or _meta(soup, 'brand') or ''
    if not result['image_urls']:
        og_img = _og(soup, 'og:image')
        if og_img:
            result['image_urls'] = [og_img]

    # 3. Infer brand from domain if still missing
    if not result['brand']:
        result['brand'] = _brand_from_domain(url)

    # 4. Collect more product images
    if len(result['image_urls']) < 4:
        more = _scrape_images(soup, url, set(result['image_urls']))
        result['image_urls'] = (result['image_urls'] + more)[:8]

    # 5. Infer structured fields from combined text
    full_text = ' ' + (result['product_name'] + ' ' + result['description']).lower() + ' '

    if not result['garment_type']:
        result['garment_type'] = _infer_garment_type(full_text)
    if not result['color']:
        result['color'] = _infer_color(full_text)
    if not result['fit']:
        result['fit'] = _infer_fit(full_text)
    if not result['material']:
        result['material'] = _infer_material(full_text)

    # 6. Infer design details from description
    desc_lower = result['description'].lower()
    if desc_lower:
        if not result['front_design']:
            result['front_design'] = _infer_front_design(desc_lower)
        if not result['back_design']:
            result['back_design'] = _infer_back_design(desc_lower)
        if not result['logo_text_placement']:
            result['logo_text_placement'] = _infer_logo_placement(desc_lower)

    # 7. Build must_preserve / must_avoid
    result['must_preserve'] = _build_must_preserve(result)
    result['must_avoid'] = _build_must_avoid(result)

    # 8. Report gaps
    missing = [
        f for f in ('brand', 'product_name', 'garment_type', 'color')
        if not result[f]
    ]
    if missing:
        result['extraction_notes'].append(
            f'Could not auto-extract: {", ".join(missing)}. Fill in manually.'
        )
    if not result['image_urls']:
        result['extraction_notes'].append('No product images found.')

    return result


# ── JSON-LD ──────────────────────────────────────────────────────────────────

def _apply_json_ld(result: dict, item: dict) -> None:
    if not result['product_name']:
        result['product_name'] = item.get('name', '')
    if not result['description']:
        result['description'] = item.get('description', '')
    if not result['color']:
        result['color'] = item.get('color', '')
    if not result['material']:
        result['material'] = item.get('material', '')

    brand = item.get('brand', {})
    if not result['brand']:
        if isinstance(brand, dict):
            result['brand'] = brand.get('name', '')
        elif isinstance(brand, str):
            result['brand'] = brand

    if not result['image_urls']:
        images = item.get('image', [])
        if isinstance(images, str):
            result['image_urls'] = [images]
        elif isinstance(images, list):
            result['image_urls'] = [
                (i if isinstance(i, str) else i.get('url', ''))
                for i in images
                if i
            ][:8]


# ── HTML meta helpers ────────────────────────────────────────────────────────

def _og(soup, prop: str) -> str:
    tag = soup.find('meta', property=prop)
    return (tag.get('content') or '').strip() if tag else ''


def _meta(soup, name: str) -> str:
    tag = soup.find('meta', attrs={'name': name})
    return (tag.get('content') or '').strip() if tag else ''


def _page_title(soup) -> str:
    if soup.title and soup.title.string:
        return soup.title.string.strip()
    h1 = soup.find('h1')
    return h1.get_text(strip=True) if h1 else ''


def _brand_from_domain(url: str) -> str:
    try:
        netloc = urlparse(url).netloc.replace('www.', '')
        domain = netloc.split('.')[0]
        return domain.replace('-', ' ').title()
    except Exception:
        return ''


# ── Image scraping ───────────────────────────────────────────────────────────

def _scrape_images(soup, base_url: str, seen: set) -> list:
    imgs = []

    for script in soup.find_all('script'):
        text = script.string or ''
        for url in re.findall(
            r'https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp)[^\s"\'<>]*', text
        ):
            if url not in seen and _is_product_image(url):
                imgs.append(url)
                seen.add(url)
            if len(imgs) >= 6:
                return imgs

    for img in soup.find_all('img'):
        src = (
            img.get('data-src')
            or img.get('data-lazy-src')
            or img.get('src')
            or ''
        )
        if not src or src.startswith('data:'):
            continue
        full = urljoin(base_url, src)
        if full not in seen and _is_product_image(full):
            imgs.append(full)
            seen.add(full)
        if len(imgs) >= 6:
            break

    return imgs


def _is_product_image(url: str) -> bool:
    low = url.lower()
    skip = (
        'logo', 'icon', 'sprite', 'placeholder', 'blank', 'pixel',
        'tracking', 'badge', 'avatar', 'banner', 'social', 'favicon',
    )
    if any(s in low for s in skip):
        return False
    return bool(re.search(r'\.(jpg|jpeg|png|webp)(\?|$|&)', low))


# ── Text inference ───────────────────────────────────────────────────────────

def _infer_garment_type(text: str) -> str:
    for canonical, keywords in GARMENT_TYPES:
        for kw in keywords:
            if kw in text:
                return canonical
    return ''


def _infer_color(text: str) -> str:
    for color in COLORS:
        if re.search(r'\b' + re.escape(color) + r'\b', text):
            return color
    return ''


def _infer_fit(text: str) -> str:
    for fit in FIT_KEYWORDS:
        if fit in text:
            return fit
    return ''


def _infer_material(text: str) -> str:
    for mat in MATERIAL_KEYWORDS:
        if mat in text:
            return mat
    return ''


def _infer_front_design(text: str) -> str:
    m = re.search(r'(?:front|chest)[^.]{0,100}', text)
    if m:
        snippet = m.group(0).strip()
        design_words = (
            'graphic', 'logo', 'print', 'text', 'embroid', 'patch',
            'minimal', 'clean', 'blank', 'cross', 'design', 'detail',
        )
        if any(k in snippet for k in design_words):
            return snippet[:120]
    return ''


def _infer_back_design(text: str) -> str:
    m = re.search(r'back[^.]{0,120}', text)
    if m:
        snippet = m.group(0).strip()
        design_words = (
            'graphic', 'logo', 'print', 'text', 'embroid', 'patch',
            'cross', 'design', 'detail',
        )
        if any(k in snippet for k in design_words):
            return snippet[:120]
    return ''


def _infer_logo_placement(text: str) -> str:
    parts = []
    for pattern in (r'logo[^.]{0,80}', r'branding[^.]{0,80}', r'embroidered[^.]{0,80}'):
        m = re.search(pattern, text)
        if m:
            parts.append(m.group(0).strip()[:80])
    return '; '.join(parts[:2])


# ── Aggressive description parse ────────────────────────────────────────────

_DESIGN_WORDS = (
    'graphic', 'print', 'logo', 'embroid', 'patch', 'motif',
    'artwork', 'appliqué', 'applique', 'screenprint', 'illustration',
    'lettering', 'inscription', 'cross', 'text', 'design',
)

_FIT_WORDS = (
    ('oversized fit', 'oversized fit'),
    ('relaxed fit', 'relaxed fit'),
    ('slim fit', 'slim fit'),
    ('regular fit', 'regular fit'),
    ('oversized', 'oversized'),
    ('relaxed', 'relaxed'),
    ('boxy', 'boxy'),
    ('slim', 'slim'),
    ('regular', 'regular'),
    ('loose', 'loose'),
    ('fitted', 'fitted'),
    ('straight', 'straight'),
)


def _deep_parse_description(description: str, result: dict) -> None:
    """Sentence-level parse of the full description. Mutates result in-place."""
    desc_lower = description.lower()
    sentences = re.split(r'[.;!\n]+', description)
    sentences_lower = [s.lower().strip() for s in sentences]

    # Fit — scan full description for any fit keyword, return the keyword itself
    if not result.get('fit'):
        for kw, label in _FIT_WORDS:
            if kw in desc_lower:
                result['fit'] = label
                break

    # Is any design word present anywhere in the description?
    has_design = any(w in desc_lower for w in _DESIGN_WORDS)

    # Front design — collect sentences mentioning front/chest
    if not result.get('front_design'):
        front_sents = [
            s.strip() for s, sl in zip(sentences, sentences_lower)
            if ('front' in sl or 'chest' in sl) and s.strip()
        ]
        if front_sents and has_design:
            result['front_design'] = '; '.join(front_sents)[:240]
        elif front_sents:
            result['front_design'] = front_sents[0][:120]

    # Back design — collect sentences mentioning back
    if not result.get('back_design'):
        back_sents = [
            s.strip() for s, sl in zip(sentences, sentences_lower)
            if 'back' in sl and s.strip()
        ]
        if back_sents and has_design:
            result['back_design'] = '; '.join(back_sents)[:240]
        elif back_sents:
            result['back_design'] = back_sents[0][:120]

    # Logo/graphic placement — collect every sentence with a design word
    if not result.get('logo_text_placement'):
        logo_sents = [
            s.strip() for s, sl in zip(sentences, sentences_lower)
            if any(w in sl for w in ('logo', 'graphic', 'branding',
                                     'embroid', 'print', 'motif', 'appliqué'))
            and s.strip()
        ]
        if logo_sents:
            result['logo_text_placement'] = '; '.join(logo_sents)[:240]


# ── Must preserve / avoid builders ──────────────────────────────────────────

def _build_must_preserve(result: dict) -> str:
    parts = []
    if result.get('garment_type'):
        parts.append(f'exact {result["garment_type"]} structure')
    if result.get('color'):
        parts.append(f'{result["color"]} color')
    if result.get('fit'):
        parts.append(f'{result["fit"]} fit')
    if result.get('material'):
        parts.append(f'natural {result["material"]} texture and drape')
    if result.get('back_design'):
        parts.append('back design as photographed')
    if result.get('front_design'):
        parts.append('front design as photographed')
    return ', '.join(parts) or 'garment structure, color, and all design details'


def _build_must_avoid(result: dict) -> str:
    parts = ['invented graphics', 'wrong color', 'wrong garment silhouette']
    if result.get('logo_text_placement'):
        parts.append('altered logo or text placement')
    if result.get('brand'):
        parts.append('incorrect branding or invented labels')
    return ', '.join(parts)
