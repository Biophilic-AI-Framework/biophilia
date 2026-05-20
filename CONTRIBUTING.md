# Contributing to Biophilic AI Framework

Thank you for your interest in contributing to BIF! We welcome all forms of contribution, from code improvements to philosophical discussions and documentation enhancements.

## Code of Conduct

We are committed to providing a welcoming and inspiring community for all. Please read and abide by our [Code of Conduct](CODE_OF_CONDUCT.md) (coming soon).

## How to Contribute

### 1. Report Issues

Found a bug? Have a feature idea? Please open an issue:

1. Go to [Issues](https://github.com/Biophilic-AI-Framework/biophilia/issues)
2. Check if a similar issue already exists
3. Create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs. actual behavior
   - Python version, OS, and environment details

### 2. Submit a Pull Request

#### Setup

```bash
# Clone and enter your fork
git clone https://github.com/YOUR-USERNAME/biophilia.git
cd biophilia

# Create a feature branch
git checkout -b feature/my-feature
# or bugfix/issue-number

# Sync dependencies
uv sync --all-extras
```

#### Guidelines

**Code Quality:**
- Type hints on all functions (PEP 484)
- Google-style docstrings for public APIs
- 100+ character line length is OK (we use Ruff with line-length=100)
- Use `from __future__ import annotations` for forward compatibility

**Testing:**
- Add tests for new features
- Ensure all tests pass: `uv run pytest tests/ -v`
- Aim for >95% coverage on changed code

**Commits:**
- Clear, descriptive commit messages
- Reference issue numbers: `Fixes #123` or `Relates to #456`
- Group related changes logically
- Include the pillar(s) affected in the message

Example:
```
Pillar I (Non-Maleficence): increase dead-zone tolerance

- Raise dissonance dead-zone from 3% to 5% to reduce false positives
- Add test case: test_dead_zone_tolerates_sensor_noise
- Update baseline threshold documentation

Fixes #42
```

#### Before Submitting

```bash
# 1. Run tests
uv run pytest tests/ -v

# 2. Type check
uv run mypy src/biophilia

# 3. Lint and format
uv run ruff check src/biophilia tests/
uv run ruff format src/biophilia tests/

# 4. Coverage report
uv run pytest tests/ --cov=src/biophilia --cov-report=term-missing
```

Pull request will auto-run these checks via GitHub Actions, so these steps are mainly for local speed.

### 3. Improve Documentation

Documentation improvements are always welcome!

- Fix typos or clarify explanations
- Add usage examples or tutorials
- Improve docstrings
- Add or update README sections

No need for special approval for documentation PRs—just ensure clarity and accuracy.

### 4. Philosophical Contributions

BIF is as much about values as it is about code. You can contribute by:

- Discussing the three pillars and their applications
- Proposing new ethical frameworks or extensions
- Sharing real-world use cases
- Writing essays or case studies (in `/docs/essays/`, coming soon)

## Development Workflow

### Project Structure

```
src/biophilia/                 # Production code (fully typed)
├── audit/                     # Pillar I & III: audit & impact gates
├── biosemiotics/              # Signal interpretation & entropy
├── governance/                # Decision logic (three pillars)
├── actions/                   # Actuator interface
├── cloud/                     # Resource management
├── infrastructure/            # Logging & helpers
├── orchestration/             # Application layer
└── _data/                     # Bundled JSON configurations

tests/                         # Unit tests (one-to-one mapping to src)
├── test_chronicle.py
├── test_governance.py
├── test_*.py
└── conftest.py                # Shared fixtures

scripts/                       # Utility CLI tools
docs/                          # Documentation (future)
```

### Naming Conventions

- **Classes:** `PascalCase`, philosophy-aware names
  - `BiophilicEntropyDetector` (not `EntropyDetector`)
  - `IntegrityChronicle` (not `AuditLog`)
- **Functions:** `snake_case`, verb-first
  - `record_action()`, `verify_integrity()`, `analyze_trend()`
- **Constants:** `SCREAMING_SNAKE_CASE`
  - `_SPIKE_MULTIPLIER`, `_GOLDEN_ZONES`
- **Private:** Leading underscore `_private_method()`
- **Tests:** `test_<feature>_<scenario>.py`
  - `test_governance_veto_below_threshold`

### Type Hints & Docstrings

Example:

```python
def calculate_dissonance(
    self, 
    node_name: str, 
    current_sensors: dict[str, float]
) -> float:
    """
    Compute weighted dissonance for a network node.
    
    The dissonance score measures how far sensor readings deviate
    from their biological ideals (baseline). A dead-zone of 5% is
    applied to suppress noise within healthy variance.
    
    Parameters
    ----------
    node_name:
        Identifier of the network node (e.g. 'Forest_Node_01').
    current_sensors:
        Dict mapping sensor names to current readings.
        
    Returns
    -------
    Dissonance score in [0, ∞), rounded to 4 decimals.
    Low values indicate harmony; high values indicate systemic stress.
        
    Raises
    ------
    KeyError
        If node_name is unknown and no fallback exists.
    """
```

### Testing Patterns

Use pytest fixtures for reusable test data:

```python
# In conftest.py
@pytest.fixture()
def sensor_data_harmony() -> dict[str, float]:
    return {
        "audio_harmony": 0.85,
        "soil_moisture": 45.0,
        "ambient_light": 600.0,
        "mycelium_activity": 0.5,
    }

# In your test
def test_perfect_harmony(detector, sensor_data_harmony):
    d = detector.calculate_dissonance("Forest_Node_01", sensor_data_harmony)
    assert d == 0.0
```

### Git Workflow (Recommended)

```bash
# 1. Create feature branch from main
git checkout -b feature/descriptive-feature-name

# 2. Make changes & commit with clear messages
git add src/biophilia/module/file.py tests/test_module.py
git commit -m "Pillar II: force emergency stabilization on critical state

- Add is_mandatory flag to governance context
- Implement absolute override in GovernanceLayer.validate()
- Add test: test_mandatory_forces_emergency
- Update docstring to reflect override logic

Fixes #88"

# 3. Push to your fork
git push origin feature/descriptive-feature-name

# 4. Open a Pull Request on GitHub
#    - Link the issue it fixes
#    - Describe what changed and why
#    - Reference any related PRs or discussions
```

## Review Process

Pull requests will be reviewed for:

1. **Correctness** – Does it work? Are edge cases handled?
2. **Consistency** – Does it follow project patterns and style?
3. **Performance** – Any obvious inefficiencies?
4. **Documentation** – Are docstrings and comments clear?
5. **Philosophy** – Does it align with the three pillars?

Expect feedback and discussion—this is a collaborative process. We're not perfect, and neither are our first drafts!

## Release Process

Releases follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (0→1): Breaking changes or new pillars
- **MINOR** (0.1→0.2): New features, non-breaking additions
- **PATCH** (0.2.0→0.2.1): Bug fixes, documentation

Releases are tagged and published to PyPI (coming soon).

## Community

- **Discussions:** GitHub Discussions (coming soon)
- **Chat:** Not yet set up; contact maintainers if interested
- **Events:** Hackathons, philosophy talks, and workshops (planned)

## Questions?

- Check existing documentation in `DEVELOPMENT.md` and `INSTALLATION.md`
- Review closed issues and PRs for similar discussions
- Open a new Discussion or contact the maintainers

---

**Thank you for contributing to the future of life-affirming AI!** 🌿

We believe that code is philosophy made executable, and your contributions help make BIF more robust, ethical, and impactful.

