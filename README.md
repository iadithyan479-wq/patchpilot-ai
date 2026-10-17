# PatchPilot

PatchPilot is a small, AI-assisted code review CLI. It reads a Git diff and asks an OpenAI-compatible chat-completions endpoint to identify concrete bugs, security risks, and missing tests. Findings are returned as Markdown and include file/line references when available.

## Features

- Reviews the working-tree diff, a commit range, or a diff piped through stdin.
- Uses an OpenAI-compatible endpoint and configurable model.
- Reads credentials only from environment variables; never writes them to disk.
- Limits diff size, supports timeout configuration, and handles API errors clearly.
- Can save the Markdown review to a file.

## Requirements

- Python 3.10+
- Git (for repository diff mode)
- An API key for an OpenAI-compatible chat-completions service

## Install

```bash
git clone https://github.com/OWNER/patchpilot.git
cd patchpilot
python -m pip install .
```

## Configure

```bash
export OPENAI_API_KEY="your-key"
# Optional: defaults shown
export OPENAI_BASE_URL="https://api.openai.com/v1"
export PATCHPILOT_MODEL="gpt-4o-mini"
```

`OPENAI_BASE_URL` is the API base URL (not the full `/chat/completions` URL). For compatible providers, set it to their documented base URL.

## Usage

Review unstaged and staged changes:

```bash
patchpilot
```

Review a commit range:

```bash
patchpilot --base main
```

Review a specific range:

```bash
patchpilot --range HEAD~2..HEAD
```

Review a diff from stdin and save the report:

```bash
git diff main...HEAD | patchpilot --stdin --output review.md
```

Additional options:

```text
patchpilot --help
```

PatchPilot asks the model to report only actionable findings, ordered by severity, and to explicitly say when it finds none. AI output is advisory; verify each finding before acting on it. Do not send secrets or sensitive code to a third-party model unless you are authorized to do so.

## Development

```bash
python -m unittest discover -s tests -v
```

## License

MIT
