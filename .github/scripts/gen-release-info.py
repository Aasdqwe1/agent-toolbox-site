import json
import re
import sys
import os
import datetime as dt
import subprocess

REPO = 'Aasdqwe1/agent-toolbox'
KOTLIN_REPO = 'Aasdqwe1/agent-toolbox-kotlin'
PAGES_BASE = 'https://aasdqwe1.github.io/agent-toolbox-site'
INPUT = '/tmp/releases.json'
KOTLIN_INPUT = '/tmp/kotlin-releases.json'
OUTPUT = 'assets/release-info.json'
APK_DIR = 'apk'
TOKEN = os.environ.get('GITHUB_TOKEN', '')


def download(url, dest):
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    cmd = ['curl', '-sL', '--fail', '-o', dest, url]
    if TOKEN:
        cmd += ['-H', f'Authorization: Bearer {TOKEN}']
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        # 失败时清理半成品，避免提交损坏文件
        if os.path.exists(dest):
            os.remove(dest)
        raise RuntimeError(f'download failed: {url} ({r.returncode})')
    print('downloaded', dest, f'{os.path.getsize(dest)} bytes')


try:
    with open(INPUT, encoding='utf-8') as f:
        releases = json.load(f)
except Exception as e:
    print('parse error:', e)
    sys.exit(1)

ci = next((r for r in releases if r.get('tag_name') == 'latest' and not r.get('draft')), None)
stable_candidates = [r for r in releases if not r.get('draft') and not r.get('prerelease')]
stable = sorted(stable_candidates, key=lambda x: x['published_at'], reverse=True)[0] if stable_candidates else None

# Kotlin CI build (from agent-toolbox-kotlin repo)
kotlin = None
try:
    with open(KOTLIN_INPUT, encoding='utf-8') as f:
        kotlin_releases = json.load(f)
    krel = next((r for r in kotlin_releases if r.get('tag_name') == 'kotlin-latest-build' and not r.get('draft')), None)
    if krel:
        kotlin = asset_info(krel, 'agent-toolbox-kotlin-latest.apk')
        m = re.search(r'latest-([a-f0-9]{7,})', kotlin.get('asset_name', ''))
        if m:
            kotlin['commit'] = m.group(1)
except Exception as e:
    print('kotlin release (kotlin-repo) parse error:', e)

# Fallback: kotlin-latest-build might be on the main repo (agent-toolbox)
if not kotlin:
    try:
        krel = next((r for r in releases if r.get('tag_name') == 'kotlin-latest-build' and not r.get('draft')), None)
        if krel:
            kotlin = asset_info(krel, 'agent-toolbox-kotlin-latest.apk')
            m = re.search(r'latest-([a-f0-9]{7,})', kotlin.get('asset_name', ''))
            if m:
                kotlin['commit'] = m.group(1)
    except Exception as e:
        print('kotlin release (main-repo fallback) error:', e)


def asset_info(release, apk_name):
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
        'pages_url': f'{PAGES_BASE}/apk/{apk_name}',
    }


ci_info = asset_info(ci, 'agent-toolbox-latest.apk') if ci else None
stable_info = asset_info(stable, 'agent-toolbox-stable.apk') if stable else None

# 先写 release-info.json，确保即使 APK 下载失败元数据也更新
out = {
    'updated_at': dt.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
    'ci': ci_info,
    'stable': stable_info,
    'kotlin': kotlin,
}
with open(OUTPUT, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

# 再尝试下载 APK 镜像（失败不影响上面已写入的元数据）
if ci_info:
    m = re.search(r'latest-([a-f0-9]{7,})', ci_info['asset_name'])
    ci_info['commit'] = m.group(1) if m else ''
    try:
        download(ci_info['download_url'], os.path.join(APK_DIR, 'agent-toolbox-latest.apk'))
    except Exception as e:
        print('APK(latest) 下载失败，跳过:', e)

if stable_info:
    try:
        download(stable_info['download_url'], os.path.join(APK_DIR, 'agent-toolbox-stable.apk'))
    except Exception as e:
        print('APK(stable) 下载失败，跳过:', e)

print('updated_at:', out['updated_at'])
if ci_info:
    print('ci:', ci_info['tag'], ci_info['size_mb'], 'MB')
if kotlin:
    print('kotlin:', kotlin['tag'], kotlin['size_mb'], 'MB')
if stable_info:
    print('stable:', stable_info['tag'], stable_info['size_mb'], 'MB')
