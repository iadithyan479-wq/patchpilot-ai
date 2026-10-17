#!/usr/bin/env python3
"""Create a GitHub release with generated notes (draft by default)."""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys


def run(command: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, check=True, text=True, capture_output=capture)
    except FileNotFoundError as exc:
        raise RuntimeError(f"Required command not found: {command[0]}") from exc
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or exc.stdout or "").strip()
        raise RuntimeError(detail or f"Command failed: {' '.join(command)}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate GitHub release notes and create a draft release by default."
    )
    parser.add_argument("tag", help="Release tag, e.g. v0.2.0 (must already exist locally or remotely)")
    parser.add_argument("--target", help="Branch or commit to target; defaults to the repository default branch")
    parser.add_argument("--title", help="Release title; defaults to the tag")
    parser.add_argument("--publish", action="store_true", help="Publish immediately instead of creating a draft")
    parser.add_argument("--dry-run", action="store_true", help="Show the planned command without creating a release")
    args = parser.parse_args()

    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", args.tag):
        parser.error("tag contains unsupported characters")
    if not shutil.which("gh"):
        print("Error: install GitHub CLI (gh) and authenticate with `gh auth login`.", file=sys.stderr)
        return 2

    try:
        repo = run(["gh", "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"], capture=True).stdout.strip()
        if not repo:
            raise RuntimeError("Could not determine the GitHub repository. Run this from a cloned repository.")
        exists = subprocess.run(["gh", "release", "view", args.tag], text=True, capture_output=True)
        if exists.returncode == 0:
            raise RuntimeError(f"A release for {args.tag} already exists.")

        command = ["gh", "release", "create", args.tag, "--generate-notes", "--title", args.title or args.tag]
        if args.target:
            command.extend(["--target", args.target])
        if not args.publish:
            command.append("--draft")
        if args.dry_run:
            print(f"Repository: {repo}")
            print(f"Mode: {'publish' if args.publish else 'draft'}")
            print("Command: " + " ".join(command))
            return 0
        result = run(command, capture=True)
        print(result.stdout.strip() or f"Created {'published' if args.publish else 'draft'} release {args.tag} in {repo}.")
        return 0
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
