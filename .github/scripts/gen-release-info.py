import json
import re
import sys
import datetime as dt

REPO = 'Aasdqwe1/agent-toolbox'
INPUT = '/tmp/releases.json'
OUTPUT = 'assets/release-info.json'

try:
    with open(INPUT, encoding='utf-8') as f:
        releases = json.load(f)
except Exception as e:
    print('parse error:', e)
    sys.exit(1)

# 最新 CI 构建：tag == latest 且非 draft
ci = next((r for r in releases if r.get('tag_name') == 'latest' and not r.get('draft')), None)
# 最新正式版：非 draft 且非 prerelease，按 published_at 排序
stable_candidates = [r for r in releases if not r.get('draft') and not r.get('prerelease')]
stable = sorted(stable_candidates, key=lambda x: x['published_at'], reverse=True)[0] if stable_candidates else None


def asset_info(release):
    assets = release.get('assets') or []
    if not assets:
        return None
    a = assets[0]
    return {
        'tag': release['tag_name'],
        'asset_name': a['name'],
        'size': a['size'],
        'size_mb': round(a['size'] / 1048576, 1),
        'published_at': release['published_at'],
        'download_url': a['browser_download_url'],
    }


ci_info = asset_info(ci) if ci else None
stable_info = asset_info(stable) if stable else None

if ci_info:
    m = re.search(r'latest-([a-f0-9]{7,})', ci_info['asset_name'])
    ci_info['commit'] = m.group(1) if m else ''

out = {
    'updated_at': dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
    'ci': ci_info,
    'stable': stable_info,
}

with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print('updated_at:', out['updated_at'])
if ci_info:
    print('ci:', ci_info['tag'], ci_info['asset_name'], ci_info['size_mb'], 'MB')
else:
    print('ci: none')
if stable_info:
    print('stable:', stable_info['tag'], stable_info['asset_name'], stable_info['size_mb'], 'MB')
else:
    print('stable: none')
