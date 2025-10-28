# Contributing Guide

Thanks for your interest in contributing to langgraph-supervised-quickstart! This guide explains how to propose changes and contribute effectively.

## Table of Contents
- Code of Conduct
- Ways to contribute
- Development setup
- Branching & workflow
- Commit style
- Pull request checklist
- Issue triage

## Code of Conduct

Please review and follow our [Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project, you agree to abide by it.

## Ways to Contribute

- Report bugs and issues
- Suggest features and improvements
- Improve documentation and examples
- Fix typos and broken links
- Add small, focused enhancements

## Development Setup

1. Fork the repository and clone your fork.
2. Create a virtual environment and install dependencies:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3. Configure your `.env` (see `README.md`).
4. Run the CLI locally:

```bash
PYTHONPATH=src python -m cli --help
```

## Branching & Workflow

- Create a feature branch from `main`:

```bash
git checkout -b feat/short-description
```

- Keep changes small and focused.
- Write clear commit messages.
- Open a Pull Request early (drafts welcome).

## Commit Style

Use clear, conventional commit messages. Examples:

- `feat(cli): add rich status spinner`
- `fix(tools): handle empty input for keyword_counts`
- `docs(readme): add mermaid architecture diagrams`
- `chore: update requirements`

## Pull Request Checklist

- [ ] Tests (if applicable) pass locally
- [ ] Lint/type-check (if applicable) is clean
- [ ] Docs updated (README or docs/*)
- [ ] Linked to related issue(s)
- [ ] Clear description of changes and rationale

## Issue Triage

When opening an issue, please include:

- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Environment details (OS, Python version)
- Screenshots or logs if helpful

Use labels appropriately: `bug`, `enhancement`, `docs`, `help wanted`, etc.

## Questions?

See [SUPPORT.md](SUPPORT.md) for help options. Thank you for contributing!
