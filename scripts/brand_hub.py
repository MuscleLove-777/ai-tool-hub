"""Persistent MuscleLove presentation, applied by the existing Pages build."""
import json
from pathlib import Path
from bs4 import BeautifulSoup

PREFIX = '/ai-tool-hub/assets/'
IMAGE = PREFIX + 'images/musclelove-stretch.png'
ALT = '明るいジムで両腕を上げる、筋肉質な架空の日本人成人女性のアニメイラスト'


def fragment(html):
    return BeautifulSoup(html, 'html.parser')


def apply_brand(soup, home=False):
    for tag in soup.select('link[href="/assets/css/visual.css"], script[src="/assets/js/visual.js"]'):
        tag.decompose()
    if not soup.select_one('#ml-brand-css'):
        soup.head.append(soup.new_tag('link', id='ml-brand-css', rel='stylesheet', href=PREFIX+'css/brand.css'))
    if not soup.select_one('#ml-brand-js'):
        soup.head.append(soup.new_tag('script', id='ml-brand-js', src=PREFIX+'js/brand.js', defer=''))
    if not soup.select_one('.ml-nav'):
        soup.body.insert(0, fragment('''<nav class="ml-nav" aria-label="メインナビゲーション"><a class="ml-wordmark" href="/ai-tool-hub/">Muscle<span>Love</span><small>AI TOOL HUB</small></a><a href="/ai-tool-hub/#discover">ツールを探す <span aria-hidden="true">↗</span></a></nav>'''))
    if home:
        header = soup.select_one('header.header')
        if header and not header.select_one('.ml-hero-copy'):
            header.clear()
            header.append(fragment(f'''<div class="ml-hero-copy"><p class="ml-eyebrow">STRONG BODY. CREATIVE MIND.</p><h1>Muscle<span>Love</span><small>AI TOOL HUB</small></h1><p class="ml-tagline">強く、美しく。<br/>つくる力も、鍛えよう。</p><p class="subtitle">筋肉美とクリエイティブを愛するあなたへ。<br/>AI・創作・フィットネスのヒントを、ここから。</p><div class="ml-actions"><a class="ml-primary" href="#discover">ツール・ブログを探す <span aria-hidden="true">↗</span></a><a class="ml-secondary" href="https://x.com/MuscleGirlLove7" target="_blank" rel="noopener">公式Xを見る</a></div><p class="ml-note">MUSCLE &amp; CREATIVITY / BY MUSCLELOVE</p></div><figure class="ml-cover ml-project-cover"><img src="{IMAGE}" alt="{ALT}" width="1024" height="1536" loading="eager" fetchpriority="high" decoding="async"/><figcaption>架空の成人女性のAIイラスト</figcaption><span class="ml-image-label" aria-hidden="true">STRENGTH<br/><b>IS BEAUTIFUL.</b></span></figure>'''))
        first = soup.select_one('.category')
        if first:
            first['id'] = 'discover'
        title = 'MuscleLove AI Tool Hub | 強く、美しく。つくる力も、鍛えよう。'
        desc = '筋肉美とクリエイティブを愛する人のためのMuscleLoveポータル。AI・創作・フィットネスのブログを探せます。'
        soup.title.string = title
        for key, value in [('description', desc), ('og:title', title), ('twitter:title', title), ('og:description', desc), ('twitter:description', desc)]:
            tag = soup.find('meta', attrs={'property' if key.startswith('og:') else 'name': key})
            if tag:
                tag['content'] = value
        for tag in soup.find_all('script', type='application/ld+json'):
            data = json.loads(tag.string or tag.get_text())
            if data.get('@type') == 'WebSite':
                data.update(name=title, description=desc)
                tag.string = json.dumps(data, ensure_ascii=False)
    for img in soup.select('.ml-project-cover img, .ml-card-image, .ml-always img'):
        img['src'] = IMAGE
        img['width'], img['height'] = '1024', '1536'
        img['data-ml-fallback'] = IMAGE
        if 'ml-card-image' not in img.get('class', []):
            img['alt'] = ALT
    for caption in soup.select('.ml-project-cover figcaption'):
        caption.string = '架空の成人女性のAIイラスト'
    if not soup.select_one('.ml-always'):
        soup.body.append(fragment(f'''<aside class="ml-always" aria-label="MuscleLove ブランド"><img src="{IMAGE}" alt="{ALT}" width="1024" height="1536" decoding="async"/><div><strong>Muscle<span>Love</span></strong><p>強く、美しく。</p><a href="https://x.com/MuscleGirlLove7" target="_blank" rel="noopener">公式X <span aria-hidden="true">↗</span></a></div></aside>'''))
    for attr, key, value in [('property','og:image', 'https://musclelove-777.github.io'+IMAGE),('name','twitter:image','https://musclelove-777.github.io'+IMAGE),('property','og:image:width','1024'),('property','og:image:height','1536'),('property','og:image:type','image/png')]:
        tag = soup.find('meta', attrs={attr:key})
        if tag is None:
            tag = soup.new_tag('meta', attrs={attr:key})
            soup.head.append(tag)
        tag['content'] = value


def check_assets(root):
    for name in ['images/musclelove-stretch.png', 'css/brand.css', 'js/brand.js']:
        if not (Path(root)/'assets'/name).is_file():
            raise ValueError('Required brand asset missing: '+name)
