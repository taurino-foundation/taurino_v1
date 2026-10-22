#!/usr/bin/env python3
"""Verify that a requested release tag matches the checked-out commit and crate version."""
from pathlib import Path
import argparse, re, subprocess, tomllib

p = argparse.ArgumentParser()
p.add_argument('--tag', required=True)
p.add_argument('--github-output')
a = p.parse_args()
root = Path(__file__).resolve().parents[2]
crate = tomllib.loads((root/'crates/taurino/Cargo.toml').read_text(encoding='utf-8'))
version = crate['package']['version']
assert re.fullmatch(r'v?\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?', a.tag), f'Invalid tag: {a.tag}'
assert a.tag == f'v{version}', f'Tag {a.tag} does not match crate version v{version}'
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
tag_commit = subprocess.check_output(['git', 'rev-list', '-n', '1', a.tag], cwd=root, text=True).strip()
assert commit == tag_commit, f'Checkout {commit} differs from tag commit {tag_commit}'
if a.github_output:
    with open(a.github_output, 'a', encoding='utf8') as f:
        f.write(f'version={version}\n')
print(f'Release tag validated: {a.tag} at {commit}')
