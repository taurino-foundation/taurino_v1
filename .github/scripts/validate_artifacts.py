#!/usr/bin/env python3
"""Basic PyPI artifact checks, including names, version and accidental duplicates."""
from pathlib import Path
import argparse
from collections import Counter

p=argparse.ArgumentParser()
p.add_argument('dist')
p.add_argument('--version', required=True)
a=p.parse_args()
files=list(Path(a.dist).iterdir())
wheels=[f for f in files if f.name.endswith('.whl')]
sdist=[f for f in files if f.name.endswith('.tar.gz')]
assert wheels, 'No wheels found'
assert len(sdist) == 1, f'Expected exactly one source distribution, got {len(sdist)}'
assert all(f.name.startswith('taurino-') and a.version in f.name for f in wheels+sdist), 'Wrong package name/version'
counts=Counter(f.name for f in files)
assert all(count == 1 for count in counts.values()), 'Duplicate artifact names'
print(f'Validated {len(wheels)} wheels and one sdist for taurino {a.version}')
