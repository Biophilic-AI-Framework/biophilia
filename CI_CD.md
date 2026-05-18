# CI/CD Pipeline

The Biophilic AI Framework uses GitHub Actions for continuous integration and delivery.

## Workflows

### 1. Tests & Quality Checks (`.github/workflows/tests.yml`)

**Trigger:** Every push to `main`/`develop` and all pull requests

**Jobs:**

#### Test Suite
- Runs on: macOS, Ubuntu
- Python versions: 3.11, 3.12, 3.13
- Executes: `pytest tests/ -v --tb=short`
- Coverage report: Uploads to Codecov

Expected: **73 tests pass in ~0.22s**

#### Type Checking
- Tool: `mypy` (strict mode)
- Command: `mypy src/biophilia --ignore-missing-imports`
- Expected: No errors on public API

#### Linting & Formatting
- Tool: `ruff`
- Commands:
  - `ruff check src/biophilia tests/`
  - `ruff format --check src/biophilia tests/`

### 2. Security & Dependency Check (`.github/workflows/security.yml`)

**Trigger:** 
- Every Monday at 09:00 UTC
- Any push to `pyproject.toml` or `uv.lock`
- Pull requests modifying dependencies

**Jobs:**

- **Bandit** – Security scanning for common Python vulnerabilities
- **Safety** – Checks for known vulnerable package versions

**Note:** These jobs are non-blocking (continue-on-error) to allow for discussion before breaking builds.

## Badge Status

Add this to your README to show CI status:

```markdown
[![Tests](https://github.com/Biophilic-AI-Framework/biophilia/actions/workflows/tests.yml/badge.svg)](https://github.com/Biophilic-AI-Framework/biophilia/actions/workflows/tests.yml)
[![Security](https://github.com/Biophilic-AI-Framework/biophilia/actions/workflows/security.yml/badge.svg)](https://github.com/Biophilic-AI-Framework/biophilia/actions/workflows/security.yml)
```

## Local Pre-flight Checks

Before pushing, run these locally to catch issues early:

```bash
# Run all checks in sequence
uv run pytest tests/ -v && \
uv run mypy src/biophilia && \
uv run ruff check src/biophilia tests/
```

Or individually:

```bash
# Unit tests
uv run pytest tests/ -v --cov=src/biophilia

# Type checks
uv run mypy src/biophilia

# Linting
uv run ruff check src/biophilia tests/
uv run ruff format src/biophilia tests/  # Auto-fix formatting
```

## Troubleshooting CI Failures

### Test Failures

**Common cause:** Python version mismatch or missing dependencies

```bash
# Ensure you have the same env as CI
uv sync --all-extras
uv run pytest tests/ -v
```

**If a specific test fails:**
- Check the GitHub Actions log for detailed output
- Run the test locally: `uv run pytest tests/test_module.py::TestClass::test_name -v`
- Add `-vv` flag for extra verbosity

### Type Checking Failures

**Cause:** Missing type hints or `# type: ignore` comments

```bash
uv run mypy src/biophilia --show-error-codes  # Shows error codes
```

Forward refs with `from __future__ import annotations`:
```python
from __future__ import annotations
```

Ignore unavoidable JSON typing issues:
```python
data: dict[str, object]  # type: ignore[type-arg]
```

### Linting Failures

**Format issues:**
```bash
uv run ruff format src/biophilia tests/  # Auto-fix
```

**Naming or import issues:**
```bash
uv run ruff check --fix src/biophilia tests/  # Auto-fix where possible
```

Then review and commit the changes.

## Secrets & Credentials

No secrets are needed for the basic test pipeline. The `.env` file with `BIF_SECRET_KEY` is **only** required when *running* the application locally—not for tests.

Tests use a fixture to inject `BIF_SECRET_KEY=test-secret-key-do-not-use-in-prod`.

See `tests/conftest.py`:
```python
@pytest.fixture(autouse=True)
def bif_secret_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """Inject a dummy secret key so tests avoid RuntimeError."""
    monkeypatch.setenv("BIF_SECRET_KEY", "test-secret-key...")
```

## Future Enhancements

Planned additions to the CI/CD pipeline:

- [ ] Code coverage thresholds and regression detection
- [ ] Performance benchmarking (regression warnings)
- [ ] Automated releases to PyPI
- [ ] Docker image builds and pushes
- [ ] Integration tests against live consensus network
- [ ] Documentation build & deployment

## Matrix Testing

The workflow tests against:

| OS | Python 3.11 | Python 3.12 | Python 3.13 |
|---|---|---|---|
| **Ubuntu** | ✅ | ✅ | ✅ |
| **macOS** | ✅ | ✅ | ✅ |

This ensures broad compatibility across platforms and Python versions.

## Performance

Typical CI run times:

- **Test suite:** ~30–45 seconds (3 Python versions × 2 OSs in parallel)
- **Type checking:** ~10 seconds
- **Linting:** ~5 seconds
- **Total per PR:** ~1 minute

Codecov integration adds minimal overhead (~10 seconds).

## Debugging CI Issues

**View full logs:**
1. Go to your PR → "Checks" tab
2. Click "Tests & Quality Checks"
3. Expand the job (e.g., "test (ubuntu-latest, 3.13)")
4. See detailed step-by-step output

**Re-run a failed workflow:**
1. Click "Re-run all jobs" button
2. Or "Re-run failed jobs" to save time

**Check dependency compatibility:**
```bash
# Create a fresh venv to test a clean install
python3.11 -m venv test_venv
source test_venv/bin/activate
uv sync  # Should work without errors
python -c "import biophilia; print(biophilia.__version__)"
```

---

**Last updated:** May 2026  
**Framework status:** CI/CD configured and tested  
**Platform support:** Ubuntu (Linux), macOS

