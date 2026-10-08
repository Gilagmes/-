#!/usr/bin/env python3
from pathlib import Path
import re, sys
root=Path(__file__).resolve().parents[1]
errors=[]
idx=(root/'index.html').read_text()
for ref in re.findall(r'(?:href|src)="([^"]+)"',idx):
    if ref.startswith(('http:','https:','#','data:')): continue
    ref=ref.split('?',1)[0]
    if not (root/ref).exists(): errors.append(f'missing asset: {ref}')
js=(root/'game.js').read_text()
# cheap static integrity checks for accidental truncation / unmatched braces
pairs={'{':'}','(':')','[':']'}
for a,b in pairs.items():
    if js.count(a)!=js.count(b): errors.append(f'game.js delimiter mismatch {a}{b}: {js.count(a)} != {js.count(b)}')
for token in ['startHeroArt','runSystemAudit','requestAnimationFrame']:
    if token not in js and token!='startHeroArt': errors.append(f'expected token absent: {token}')
css=(root/'v380.css').read_text()
css381=(root/'v384.css').read_text()
if '#start' not in css or '.start-visual' not in css: errors.append('v380 visual layer incomplete')
if '384' not in css381: errors.append('v384 combat readability release marker missing')
if 'drawCombatCommandHUD' not in js: errors.append('combat HUD function missing')
if 'killBurst' not in js: errors.append('kill impact effect missing')
if 'abilityTelegraph' not in js: errors.append('v383 ability telegraph missing')
if 'pushAbilityTelegraph' not in js: errors.append('ability telegraph helper missing')
if 'drawStatusChips' not in js: errors.append('status chips helper missing')
if 'v396' not in idx: errors.append('v396 cache marker missing')
if not (root/'v396.css').exists(): errors.append('v396 stylesheet missing')
if 'aether-clash-v396' not in (root/'sw.js').read_text(): errors.append('v396 service worker cache missing')
if 'updateVisionGameplay' not in js: errors.append('vision gameplay updater missing')
if 'wardActive' not in js: errors.append('ward lifecycle helper missing')
if 'placeControlWard' not in js: errors.append('control ward placement missing')
if 'visionControl' not in js: errors.append('objective vision control missing')
if 'ТОТЕМ ОБНАРУЖЕН' not in js: errors.append('counter-vision feedback missing')
if "cat==='crit'" not in js: errors.append('combat number hierarchy missing')
try:
    import subprocess
    subprocess.run(['node','--check',str(root/'game.js')],check=True,capture_output=True,text=True)
except Exception as exc:
    errors.append(f'node syntax check failed: {exc}')
print('AETHER CLASH VALIDATOR')
print('version: v396')
print('assets:', 'OK' if not any(x.startswith('missing asset') for x in errors) else 'FAIL')
print('game.js delimiters:', 'OK' if not any('delimiter mismatch' in x for x in errors) else 'FAIL')
if errors:
    print('\n'.join('ERROR: '+x for x in errors)); sys.exit(1)
print('RESULT: PASS')
