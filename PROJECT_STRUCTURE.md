# Project Structure – Clean & Organized

## Directory Overview

```
biophilia/                          Repository Root
│
├─ src/biophilia/                   ✅ PRODUCTION CODE (v0.2)
│  ├─ __init__.py
│  ├─ audit/                        Pillar I & III: audit gates
│  ├─ biosemiotics/                 Signal interpretation
│  ├─ governance/                   Decision logic (3 pillars)
│  ├─ actions/                      Actuator interface
│  ├─ cloud/                        Resource management
│  ├─ infrastructure/               Logging & utilities
│  ├─ orchestration/                Main application
│  └─ _data/                        Bundled JSON baselines
│
├─ tests/                           ✅ UNIT TESTS (73 tests)
│  ├─ conftest.py
│  ├─ test_chronicle.py
│  ├─ test_governance.py
│  └─ ... (7 test modules total)
│
├─ scripts/                         ✅ CLI TOOLS
│  ├─ run_simulation.py
│  └─ analyze_integrity.py
│
├─ core/                            📖 PHILOSOPHY & CONCEPTS
│  ├─ PRINCIPLES.md
│  ├─ pillar-I.md
│  ├─ pillar-II.md
│  ├─ pillar-III.md
│  └─ ... (conceptual foundations)
│
├─ process/                         📊 RESEARCH & VALIDATION
│  ├─ analysis/                     Experiments (EXP_01, EXP_02)
│  ├─ evaluations/                  Case studies & benchmarks
│  ├─ dialogue/                     AI model testing logs
│  └─ benchmarks/
│
├─ prompts/                         💬 PROMPT LIBRARY
│  ├─ bif-claude4-CAI-de.md
│  ├─ bif-gemini-de.md
│  ├─ gpt-bif-de.md
│  └─ ...
│
├─ .github/                         ✅ CI/CD & TEMPLATES
│  ├─ workflows/
│  │  ├─ tests.yml                 Unit tests, type check, lint
│  │  └─ security.yml              CVE scanning, security audit
│  └─ ISSUE_TEMPLATE/
│     ├─ bug_report.md
│     └─ feature_request.md
│
├─ pyproject.toml                   ✅ PACKAGE CONFIG
├─ .env.example                     ✅ ENVIRONMENT TEMPLATE
├─ .gitignore                       ✅ VCS RULES
│
└─ Documentation Files
   ├─ README.md                     Project overview
   ├─ INSTALLATION.md               Setup & quick start
   ├─ DEVELOPMENT.md                Architecture & developer guide
   ├─ CONTRIBUTING.md               Contributor guidelines
   ├─ CI_CD.md                      CI/CD pipeline details
   ├─ CI_CD_SETUP.md                Setup overview
   ├─ CHANGELOG.md                  Version history (v0.1 → v0.2)
   ├─ QUICKSTART.md
   ├─ VISION.md                     Project vision
   └─ ...
```

## What Goes Where

### ✅ Active Development: `src/biophilia/`

**Contains:** All production Python code
- 23 modules
- Full type hints (PEP 484)
- Zero external runtime dependencies
- Used by: `uv run`, `pytest`, deployed apps

**To import:**
```python
from biophilia.governance.layer import GovernanceLayer
from biophilia.audit.chronicle import IntegrityChronicle
from biophilia.orchestration.application import BIFApplication
```

### ✅ Testing: `tests/`

**Contains:** Unit test suite
- 73 tests (100% pass rate)
- Coverage across all modules
- Test fixtures & mocking
- No external test data needed

**To run:**
```bash
uv run pytest tests/ -v
```

### ✅ CI/CD: `.github/`

**Contains:** GitHub Actions workflows
- Automated testing (Python 3.11–3.13 × Ubuntu + macOS)
- Type checking (mypy)
- Linting (ruff)
- Security scanning (Bandit, Safety)

**To view:**
1. Push code to GitHub
2. Check "Actions" tab
3. See live test results

### 📖 Reference Material: `core/`, `process/`, `prompts/`

**Contains:** Philosophical & research documentation
- Pillar definitions
- Test cases & experiments
- AI model testing results
- Prompt templates

**Usage:** Read for understanding the framework's intellectual foundation

### 📦 Legacy Archive: `_legacy/`

**Contains:** v0.1 prototype code (read-only)
- Old implementation for reference
- Historical record of evolution
- Migration guide (in `_legacy/README.md`)

**Usage:** Only for learning how code evolved

---

## File Organization Principles

### ✨ Clean Rules Applied

1. **Old Python code** → `_legacy/v0.1-prototype/`
   - Prototype scripts no longer in root
   - Historical reference preserved
   - No longer imported or used

2. **New Python code** → `src/biophilia/`
   - Single source of truth
   - Consistent imports
   - All tests passing

3. **Tests** → `tests/`
   - 1:1 mapping to modules
   - Isolated & reproducible
   - Run via pytest

4. **Documentation** → Root level
   - Readable from GitHub UI
   - Linked in pyproject.toml
   - Organized by audience

5. **CI/CD** → `.github/`
   - GitHub Actions native
   - Automatic on push/PR
   - Status visible in web UI

---

## Quick Navigation

**I want to...** | **Go to...**
---|---
...understand the project | [README.md](README.md)
...install & run it | [INSTALLATION.md](INSTALLATION.md)
...develop & contribute | [CONTRIBUTING.md](CONTRIBUTING.md) + [DEVELOPMENT.md](DEVELOPMENT.md)
...see what changed | [CHANGELOG.md](CHANGELOG.md)
...check CI/CD status | [.github/workflows/](github/workflows/) + [CI_CD.md](CI_CD.md)
...understand the philosophy | [core/PRINCIPLES.md](core/PRINCIPLES.md) + [core/pillar-*.md](core/)
...view old prototype code | [_legacy/README.md](_legacy/README.md)
...run tests locally | `uv run pytest tests/ -v`
...see code architecture | [DEVELOPMENT.md](DEVELOPMENT.md#project-structure)

---

## Statistics

| Category | Count | Status |
|----------|-------|--------|
| **Production Modules** | 23 Python files | ✅ Typed, tested |
| **Unit Tests** | 73 tests | ✅ 100% pass |
| **Test Modules** | 7 files | ✅ Full coverage |
| **Documentation** | 10+ markdown files | ✅ Complete |
| **CI/CD Workflows** | 2 | ✅ Active |
| **Legacy Files** | 16 Python files | 📦 Archived |
| **Total Lines of Code** | ~3,000 (src) | ✅ Well-typed |

---

**Project Status:** Clean, organized, production-ready. 🌿✨

No stray files. No confusion. Just working code.

