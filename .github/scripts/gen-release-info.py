import json
import re
import sys
import os
import datetime as dt
import urllib.request

REPO = 'Aasdqwe1/agent-toolbox'
PAGES_BASE = 'https://aasdqwe1.github.io/agent-toolbox-site'
CDN_BASE = 'https://cdn.jsdelivr.net/gh/Aasdqwe1/agent-toolbox-site@main'
INPUT = '/tmp/releases.json'
OUTPUT = 'assets/release-info.json'
APK_DIR = 'apk'


def download(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers={'User-Agent': 'agent-toolbox-site'})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, 'wb') as f:
        f.write(r.read())
    print('downloaded', dest)


try:
    with open(INPUT, encoding='utf-8') as f:
        releases = json.load(f)
except Exception as e:
    print('parse error:', e)
    sys.exit(1)

ci = next((r for r in releases if r.get('tag_name') == 'latest' and not r.get('draft')), None)
stable_candidates = [r for r in releases if not r.get('draft') and not r.get('prerelease')]
stable = sorted(stable_candidates, key=lambda x: x['published_at'], reverse=True)[0] if stable_candidates else None


def asset_info(release, apk_name):
    assets = release.get('assets') or []
    if not assets:
        return None
    a = assets[0]
    info = {
        'tag': release['tag_name'],
        'asset_name': a['name'],
        'size': a['size'],
        'size_mb': round(a['size'] / 1048576, 1),
        'published_at': release['published_at'],
        'download_url': a['browser_download_url'],
        'pages_url': f'{PAGES_BASE}/apk/{apk_name}',
        'cdn_url': f'{CDN_BASE}/apk/{apk_name}',
    }
    return info


ci_info = asset_info(ci, 'agent-toolbox-latest.apk') if ci else None
stable_info = asset_info(stable, 'agent-toolbox-stable.apk') if stable else None

if ci_info:
    m = re.search(r'latest-([a-f0-9]{7,})', ci_info['asset_name'])
    ci_info['commit'] = m.group(1) if m else ''
    download(ci_info['download_url'], os.path.join(APK_DIR, 'agent-toolbox-latest.apk'))

if stable_info:
    download(stable_info['download_url'], os.path.join(APK_DIR, 'agent-toolbox-stable.apk'))

out = {
    'updated_at': dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
    'ci': ci_info,
    'stable': stable_info,
}

with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print('updated_at:', out['updated_at'])
if ci_info:
    print('ci:', ci_info['tag'], ci_info['size_mb'], 'MB')
if stable_info:
    print('stable:', stable_info['tag'], stable_info['size_mb'], 'MB')
