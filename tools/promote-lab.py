#!/usr/bin/env python3
"""Promote lab.html to index.html — the exact inverse of tools/make-lab.py.

The lab is prod with five things taken out. Shipping it means putting those five
back and changing nothing else:

  1. the product title
  2. no robots noindex (the product is meant to be found)
  3. the Open Graph / Twitter block, lifted verbatim from the current index.html
  4. the Cloudflare Web Analytics snippet, lifted verbatim from the current index.html
  5. the real localStorage keys, so existing sprites are still there after the deploy

Nothing is authored here: the two restored blocks are copied out of the index.html
being replaced, so a promotion cannot invent or drop a tag. The script refuses to
write if any step fails to match, and prints the diff summary it is about to apply.

    python3 tools/promote-lab.py            # check only, writes nothing
    python3 tools/promote-lab.py --write    # actually replace index.html
"""
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROD = os.path.join(ROOT, 'index.html')
LAB = os.path.join(ROOT, 'lab.html')

lab = io.open(LAB, encoding='utf-8').read()
prod = io.open(PROD, encoding='utf-8').read()

OG_RE = r'<!-- Open Graph / social preview -->.*?<meta name="twitter:image"[^>]*>\n'
ANALYTICS_RE = r'<!-- Cloudflare Web Analytics.*?</script>\n'
NOINDEX_RE = r'<meta name="robots" content="noindex,nofollow">\n'

failures = []


def grab(pattern, label):
    m = re.search(pattern, prod, re.S)
    if not m:
        failures.append('current index.html has no ' + label)
        return ''
    return m.group(0)


og = grab(OG_RE, 'Open Graph block')
analytics = grab(ANALYTICS_RE, 'analytics snippet')

s = lab
steps = []


def sub_once(pattern, repl, label, flags=0):
    global s
    s, n = re.subn(pattern, repl, s, count=1, flags=flags)
    steps.append((label, n))
    if n != 1:
        failures.append(label + ' matched ' + str(n) + ' times, expected 1')


sub_once(r'<title>[^<]*</title>', '<title>Blockmode — ASCII Sprite Editor</title>', 'title')
sub_once(NOINDEX_RE, '', 'drop noindex')
# the OG block sat immediately before the description meta in prod; put it back there
sub_once(r'(?=<meta name="description")', og.replace('\\', '\\\\'), 'restore Open Graph')
sub_once(r'(?=</body>)', analytics.replace('\\', '\\\\'), 'restore analytics')

for key in ('blockmode:v1', 'blockmode:onboarded', 'blockmode:theme', 'blockmode:hints'):
    ns = key.replace('blockmode:', 'blockmode:lab:')
    s, n = re.subn(re.escape("'" + ns + "'"), "'" + key + "'", s)
    steps.append(('un-namespace ' + key, n))
    if n < 1:
        failures.append('no occurrences of ' + ns)

leftovers = re.findall(r'blockmode:lab:[A-Za-z0-9_:-]*', s)
if leftovers:
    failures.append('lab storage keys survived: ' + ', '.join(sorted(set(leftovers))))
if 'noindex' in s:
    failures.append('noindex survived')

for label, n in steps:
    print('  %-28s %d' % (label, n))

if failures:
    sys.stderr.write('promote-lab: REFUSING to write\n')
    for f in failures:
        sys.stderr.write('  - ' + f + '\n')
    sys.exit(1)

if '--write' in sys.argv:
    io.open(PROD, 'w', encoding='utf-8').write(s)
    print('index.html replaced (%d lines)' % len(s.splitlines()))
else:
    out = os.path.join(ROOT, '.promote-preview.html')
    io.open(out, 'w', encoding='utf-8').write(s)
    print('check only — preview written to %s (pass --write to replace index.html)' % out)
