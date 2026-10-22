#!/usr/bin/env python3
"""Check Taurino's PyPI metadata, Rust crate and optional workspace version."""
from pathlib import Path
import re
import sys
import tomllib

root = Path(__file__).resolve().parents[2]

def toml(path):
    return tomllib.loads((root / path).read_text(encoding='utf-8'))

project = toml('pyproject.toml')['project']
crate = toml('crates/taurino/Cargo.toml')['package']
version = crate['version']
if not re.fullmatch(r'\d+\.\d+\.\d+(?:[-+][\w.-]+)?', version):
    sys.exit(f'Invalid Rust version: {version}')
if project.get('name', '').lower() != 'taurino':
    sys.exit(f"Expected PyPI package 'taurino', got {project.get('name')!r}")
if 'version' in project and project['version'] != version:
    sys.exit('pyproject project.version differs from Rust crate version')
if 'version' not in project and 'version' not in project.get('dynamic', []):
    sys.exit('pyproject must declare project.version or dynamic=["version"]')
workspace = toml('Cargo.toml')
dep = workspace.get('workspace', {}).get('dependencies', {}).get('taurino')
if isinstance(dep, dict) and dep.get('version') and dep['version'] != version:
    sys.exit('workspace.dependencies.taurino.version differs from crate version')
print(f'Metadata OK: taurino {version}')
