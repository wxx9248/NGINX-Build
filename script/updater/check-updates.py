#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(".")
VERSIONS = ROOT / 'versions.json'
WORKSPACE = ROOT / 'workspace'
README = ROOT / 'README.md'

TABLE_HEADER = ['| Components | Commit Tag |', '|--|--|']


def run(cmd, cwd=None):
    return subprocess.check_output(cmd, cwd=cwd or ROOT, text=True).strip()


def load_versions() -> dict:
    with VERSIONS.open() as f:
        return json.load(f)


def save_versions(versions: dict):
    with VERSIONS.open('w') as f:
        json.dump(versions, f, indent=2)
        f.write('\n')


def get_latest_tag(path: Path):
    run(['git', 'fetch', '--tags'], cwd=path)
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
    run(['git', '-C', str(path), 'checkout', new_ref])
    run(['git', 'add', str(path)])


def rewrite_readme(versions: dict):
    lines = README.read_text().splitlines()
    start = end = None
    for i, line in enumerate(lines):
        if start is None and line.strip() == TABLE_HEADER[0]:
            start = i
            continue
        if start is not None and not line.startswith('|'):
            end = i
            break
    if start is None:
        return
    if end is None:
        end = len(lines)

    body = [f'| {name} | {entry["version"]} |' for name, entry in versions.items()]
    new_block = [TABLE_HEADER[0], TABLE_HEADER[1], *body]
    lines[start:end] = new_block
    README.write_text('\n'.join(lines) + '\n')


def main():
    versions = load_versions()
    updates = {}

    for name, entry in versions.items():
        comp_dir = WORKSPACE / name
        if not comp_dir.exists():
            continue

        policy = entry.get('policy')
        if policy == 'tag':
            new_ref = get_latest_tag(comp_dir)
        elif policy == 'branch':
            new_ref = get_latest_commit(comp_dir, entry['branch'])
        else:
            continue

        if not new_ref:
            continue

        current = entry['version']
        if new_ref != current:
            updates[name] = (current, new_ref)
            update_submodule(comp_dir, new_ref)
            entry['version'] = new_ref

    if not updates:
        print("No updates found.", file=sys.stderr)
        sys.exit(0)

    save_versions(versions)
    rewrite_readme(versions)
    run(['git', 'add', str(VERSIONS)])
    run(['git', 'add', str(README)])

    print("## Updated Components\n")
    for name, (old, new) in updates.items():
        print(f"- **{name}**: `{old}` → `{new}`")
    print("\n*This PR was generated automatically by GitHub Actions.*")


if __name__ == '__main__':
    main()
