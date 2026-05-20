# GitHub Actions CI/CD Setup

## Overview

The Biophilic AI Framework now features a comprehensive CI/CD pipeline via GitHub Actions for automated testing, type checking, linting, and security scanning.

## Files Added

### Workflow Definitions

**`.github/workflows/tests.yml`** (80 lines)
- Runs on every push to `main`/`develop` and all PRs
- Tests against: Python 3.11, 3.12, 3.13 on Ubuntu & macOS
- Jobs:
  - `test`: Unit tests + coverage (pytest)
  - `type-check`: Static type validation (mypy)
  - `lint`: Code style & formatting (ruff)

**`.github/workflows/security.yml`** (45 lines)
- Scheduled: Every Monday 09:00 UTC
- Triggered: When dependencies change
- Jobs:
  - Bandit: Security vulnerability scanning
  - Safety: Known vulnerable package detection

### Issue & PR Templates

**`.github/ISSUE_TEMPLATE/bug_report.md`** (38 lines)
- Guided template for bug reports
- Includes: Steps, environment, pillar classification

**`.github/ISSUE_TEMPLATE/feature_request.md`** (31 lines)
- Guided template for feature proposals
- Links to philosophical pillars

**`.github/pull_request_template.md`** (62 lines)
- Pre-filled PR description template
- Checklist for quality assurance
- Pillar categorization

### Documentation

**`CI_CD.md`** (220 lines)
- Complete CI/CD documentation
- Workflow descriptions & triggers
- Troubleshooting guide
- Badge snippets for README

**`CONTRIBUTING.md`** (280 lines)
- Contributor code of conduct
- Pull request guidelines
- Testing & quality standards
- Commit message conventions

## How It Works

### On Every Push (`main` or `develop`)

```
┌─ Tests & Quality Checks
│  ├─ test (3 Python versions × 2 OS) → 6 parallel jobs
│  ├─ type-check (mypy strict) → 1 job
│  └─ lint (ruff) → 1 job
└─ Total runtime: ~60 seconds
```

### On Every Pull Request

Same checks automatically run. GitHub blocks merge if any job fails.

### Security Scan (Weekly)

Runs every Monday + on dependency changes.
- Identifies CVEs and vulnerable packages
- Non-blocking but visible in PR

## GitHub Status Check Integration

When you push or create a PR, you'll see these checks:

```
✅ Tests & Quality Checks
├─ ✅ test (ubuntu-latest, 3.11)
├─ ✅ test (ubuntu-latest, 3.12)
├─ ✅ test (ubuntu-latest, 3.13)
├─ ✅ test (macos-latest, 3.11)
├─ ✅ test (macos-latest, 3.12)
├─ ✅ test (macos-latest, 3.13)
├─ ✅ type-check
└─ ✅ lint

✅ Security & Dependency Check
├─ ℹ️  bandit (may have findings)
└─ ℹ️  safety (may have findings)
```

Green checkmarks = can merge
Red X = must fix before merge

## Adding to README

Add these badges to your README.md for status visibility:

```markdown
## Status

[![Tests](https://github.com/Biophilic-AI-Framework/biophilia/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/Biophilic-AI-Framework/biophilia/actions/workflows/tests.yml)
[![Security](https://github.com/Biophilic-AI-Framework/biophilia/actions/workflows/security.yml/badge.svg)](https://github.com/Biophilic-AI-Framework/biophilia/actions/workflows/security.yml)

**[Test Results](https://github.com/Biophilic-AI-Framework/biophilia/actions)** | **[CI/CD Documentation](CI_CD.md)**
```

## Configuration Notes

### Python Versions

Matrix tests:
- **3.11** – Oldest supported (PEP 585 compatibility)
- **3.12** – Stable LTS candidate
- **3.13** – Latest (current at project time)

### Dependency Management

- **Runtime:** Zero external deps (pure stdlib)
- **Dev:** pytest, mypy, ruff, coverage (all in `pyproject.toml`)
- **CI:** Auto-installed via `uv sync --all-extras`

### OS Support

- **Ubuntu** (latest) – Linux/Docker base
- **macOS** (latest) – Apple Silicon & Intel

*Windows support coming later (actions available but not currently tested)*

## Local Development vs. CI

### Local (Before Push)

```bash
uv run pytest tests/ -v
uv run mypy src/biophilia
uv run ruff check src/biophilia tests/
```

### CI (After Push)

GitHub Actions runs the same checks automatically in parallel across all Python versions and OS combinations.

## Secrets Management

**No secrets required** for tests! The pipeline uses:

```python
# conftest.py auto-injects for tests only
@pytest.fixture(autouse=True)
def bif_secret_key(monkeypatch):
    monkeypatch.setenv("BIF_SECRET_KEY", "test-secret-key...")
```

Real `BIF_SECRET_KEY` is only needed when *running* the framework, not for CI tests.

## Cost & Performance

- **GitHub Actions free tier:** ~2000 minutes/month
- **Expected usage:** ~100 minutes/month (plenty of headroom)
- **Per PR:** ~1 minute runtime (parallelized)

## What's Next

Possible enhancements:

- [ ] Coverage thresholds (e.g., fail if <90%)
- [ ] Automated releases to PyPI
- [ ] Docker image builds
- [ ] Performance benchmarking
- [ ] Windows OS matrix
- [ ] Integration tests against live network

---

**Last updated:** May 18, 2026  
**Status:** ✅ Fully configured and tested  
**Templates:** 2 issue templates + 1 PR template  
**Workflows:** 2 (tests + security)

