import re
import json
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
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


def validate_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https') and bool(parsed.netloc)
    except Exception:
        return False


def extract_garment(url: str) -> dict:
    if not validate_url(url):
        raise ValueError('Invalid URL — must start with http:// or https://')

    try:
        response = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        if response.status_code == 403:
            raise PermissionError(
                'Website blocked access (403 Forbidden). '
                'Try copying the product URL from the browser address bar.'
            )
        if response.status_code == 404:
            raise FileNotFoundError('Product page not found (404).')
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise TimeoutError('Request timed out. The website may be slow or blocking scrapers.')
    except requests.exceptions.TooManyRedirects:
        raise ConnectionError('Too many redirects — the page may require login.')
    except requests.exceptions.ConnectionError:
        raise ConnectionError('Could not connect to the website. Check the URL.')
    except (PermissionError, FileNotFoundError, TimeoutError, ConnectionError):
        raise
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f'Failed to fetch page: {e}')

    soup = BeautifulSoup(response.text, 'html.parser')

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
            'cross', 'design', 'detail', 'graphic',
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


# ── Must preserve / avoid builders ──────────────────────────────────────────

def _build_must_preserve(result: dict) -> str:
    parts = []
    if result['garment_type']:
        parts.append(f'exact {result["garment_type"]} structure')
    if result['color']:
        parts.append(f'{result["color"]} color')
    if result['fit']:
        parts.append(f'{result["fit"]} fit')
    if result['material']:
        parts.append(f'natural {result["material"]} texture and drape')
    if result['back_design']:
        parts.append('back design as photographed')
    if result['front_design']:
        parts.append('front design as photographed')
    return ', '.join(parts) or 'garment structure, color, and all design details'


def _build_must_avoid(result: dict) -> str:
    parts = ['invented graphics', 'wrong color', 'wrong garment silhouette']
    if result['logo_text_placement']:
        parts.append('altered logo or text placement')
    if result['brand']:
        parts.append('incorrect branding or invented labels')
    return ', '.join(parts)
