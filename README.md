

## GitHub release automation

`scripts/create_release.py` asks GitHub CLI to generate release notes from merged pull requests and commits. It creates a **draft** release by default, so you can review the notes before publishing:

```bash
python3 scripts/create_release.py v0.2.0
```

Preview the planned action without creating a release:

```bash
python3 scripts/create_release.py v0.2.0 --dry-run
```

To publish immediately instead of creating a draft, opt in explicitly:

```bash
python3 scripts/create_release.py v0.2.0 --publish
```

You need GitHub CLI (`gh`) installed and authenticated, and must run the script from a clone of the target repository. `--target BRANCH_OR_COMMIT` and `--title "Release title"` are optional. The script does not post to social media.
