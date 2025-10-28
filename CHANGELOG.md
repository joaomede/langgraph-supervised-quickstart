# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-10-28

### Added
- Initial public release of LangGraph Supervised Quickstart
- Multi-agent supervisor system with LangGraph v1
- Interactive chat CLI with Rich terminal UI (panels, markdown, status indicators)
- Single-query mode for one-shot inference
- Text Analysis Agent with entity extraction and keyword counting tools
- Data Analysis Agent with statistics and table formatting tools
- Conversation memory supporting context-aware multi-turn dialogues
- Language-agnostic text processing (no hardcoded stopwords)
- Docker support with multi-stage Dockerfile
- Docker Compose orchestration with resource limits
- Comprehensive documentation:
  - `README.md` - Streamlined project overview (316 lines)
  - `docs/FINAL_SUMMARY.md` - Detailed architecture and implementation
  - `docs/CLI_UX_SHOWCASE.md` - Terminal interface showcase
  - `docs/QUICK_START_EXAMPLES.md` - Practical usage examples
  - `docs/DOCKER_GUIDE.md` - Complete Docker documentation
  - `docs/PRE_COMMIT_REVIEW.md` - Technical quality audit
  - `docs/RELEASE_CORRECTIONS_SUMMARY.md` - Pre-release corrections log
- Repository governance files:
  - `LICENSE` - MIT License
  - `CODE_OF_CONDUCT.md` - Contributor Covenant v2.1
  - `CONTRIBUTING.md` - Contribution guidelines
  - `SECURITY.md` - Security policy
  - `SUPPORT.md` - Support resources
  - `.github/PULL_REQUEST_TEMPLATE.md` - PR template
  - `.github/CODEOWNERS` - Code ownership assignment
  - `.github/ISSUE_TEMPLATE/` - Bug report and feature request templates
- `CITATION.cff` - Citation metadata for scholarly use
- `.env.example` - Environment configuration template (fully in English)
- `pyproject.toml` - Project metadata and build configuration
- `requirements.txt` - Python dependencies (LangGraph v1, LangChain, Rich)

### Changed
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Security
- Environment variables properly managed via `.env` (not committed)
- `.gitignore` configured to exclude sensitive files
- Docker `.dockerignore` optimized for secure builds

---

## [Unreleased]

### Planned
- Automated testing suite (unit and integration tests)
- GitHub Actions CI/CD pipeline
- Code quality tools (ruff, mypy)
- Example Jupyter notebooks
- Performance benchmarks
- Video walkthrough/demo
- PyPI package distribution

---

**Links:**
- [0.1.0]: https://github.com/joaomede/langgraph-supervised-quickstart/releases/tag/v0.1.0

---

**Tips for maintainers:**
- Group changes under: Added, Changed, Deprecated, Removed, Fixed, Security
- Include links to issues/PRs when helpful
- Keep one version per release
- Follow Semantic Versioning (MAJOR.MINOR.PATCH)
