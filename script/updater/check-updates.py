#!/usr/bin/env python3
import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(".")
POLICY = ROOT / 'script' / 'updater' / 'update-policy.csv'
WORKSPACE = ROOT / 'workspace'
README = ROOT / 'README.md'


def run(cmd, cwd=None):
    return subprocess.check_output(cmd, cwd=cwd or ROOT, text=True).strip()


def parse_policies():
    policies = []
    with POLICY.open() as f:
        for name, policy, *rest in csv.reader(f):
            name = name.strip()
            if not name or name.startswith('#'):
                continue
            policy = policy.strip()
            param = rest[0].strip() if rest else ''
            policies.append((name, policy, param))
    return policies


def get_latest_tag(path: Path):
    # fetch all tags so that we have the latest metadata
    run(['git', 'fetch', '--tags'], cwd=path)

    # list tags sorted by version (newest first)
    tags = run([
        'git', 'for-each-ref',
        '--sort=-version:refname',
        '--format=%(refname:short)',
        'refs/tags'
    ], cwd=path).splitlines()

    return tags[0] if tags else None


def get_latest_commit(path: Path, branch: str):
    run(['git', 'fetch', 'origin', branch], cwd=path)
    return run(['git', 'rev-parse', f'origin/{branch}'], cwd=path)


def update_submodule(path: Path, new_ref: str):
    # checkout the new ref (tag or commit) inside the submodule
    run(['git', '-C', str(path), 'checkout', new_ref])
    # stage the submodule change in the superproject
    run(['git', 'add', str(path)])


def update_readme(updates: dict[str, tuple[str,str]]):
    lines = README.read_text().splitlines()
    touched = []
    for i, line in enumerate(lines):
        if not line.startswith('|'):
            continue
        parts = [p.strip() for p in line.split('|')[1:-1]]
        if len(parts) < 2:
            continue
        comp = parts[0].lower()
        if comp in updates:
            _, new_ver = updates[comp]
            parts[1] = new_ver
            lines[i] = '| ' + ' | '.join(parts) + ' |'
            touched.append(comp)
    if touched:
        README.write_text('\n'.join(lines) + '\n')
    return touched


def main():
    policies = parse_policies()
    updates = {}

    for name, policy, param in policies:
        comp_dir = WORKSPACE / name
        if not comp_dir.exists():
            continue

        if policy == 'tag':
            new_ref = get_latest_tag(comp_dir)
        elif policy == 'branch':
            new_ref = get_latest_commit(comp_dir, param)
        else:
            continue

        if not new_ref:
            continue

        # extract current version from README table (case-insensitive match)
        m = re.search(
            rf'\|\s*{re.escape(name)}\s*\|\s*([^|\s]+)\s*\|',
            README.read_text(),
            re.IGNORECASE
        )
        current = m.group(1).strip() if m else ''

        if new_ref != current:
            updates[name.lower()] = (current, new_ref)
            update_submodule(comp_dir, new_ref)

    if not updates:
        print("No updates found.", file=sys.stderr)
        sys.exit(0)

    touched = update_readme(updates)

    # emit a markdown summary for the PR body
    print("## Updated Components\n")
    for comp in touched:
        old, new = updates[comp]
        print(f"- **{comp}**: `{old}` → `{new}`")
    print("\n*This PR was generated automatically by GitHub Actions.*")


if __name__ == '__main__':
    main()
