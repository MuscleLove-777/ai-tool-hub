"""Fail the Pages build if brand images, local assets or persistent frame disappear."""
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
from brand_hub import IMAGE, PREFIX, check_assets

def check(root):
    check_assets(root)
    count = 0
    for path in root.rglob('*.html'):
        if any(x in path.relative_to(root).parts for x in ['.git','scripts','node_modules','templates','layouts','themes','references']):
            continue
        soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
        if not soup.h1 or soup.find('meta', attrs={'http-equiv':'refresh'}):
            continue
        assert len(soup.select('.ml-always img')) == 1, str(path)
        assert soup.select_one('.ml-always img')['src'] == IMAGE
        assert soup.select_one('#ml-brand-css')['href'] == PREFIX+'css/brand.css'
        for card in soup.select('a.card'):
            assert card.select_one('img')['src'] == IMAGE
        for tag in soup.select('img[src], link[href], script[src]'):
            url = tag.get('src', tag.get('href',''))
            if url.startswith(PREFIX):
                assert (root/'assets'/url.removeprefix(PREFIX)).is_file(), url
        count += 1
    assert count, 'No brand pages found'
    return count

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path('.'))
    args = parser.parse_args()
    print(f'PASS: {check(args.root)} brand pages; local assets and images verified')
