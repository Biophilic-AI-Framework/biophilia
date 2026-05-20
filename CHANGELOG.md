# Changelog

All notable changes to the Biophilic AI Framework are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.2.0] – 2026-05-18

### Major Refactoring: From Scripts to Professional Python Package

This release transforms the BIF from a prototype script collection into a properly-packaged, professionally-maintained Python project without breaking the core philosophy.

#### Added

**Package Structure**
- Complete `src/biophilia/` layout with proper `__init__.py` files in all subpackages
- Modern `pyproject.toml` with setuptools+hatchling, pytest config, mypy strictness, ruff linting
- `.env.example` file for environment variable templates
- Comprehensive test suite: 73 unit tests across 8 test modules (97% coverage)
- `DEVELOPMENT.md` guide for contributors

**Modules (professionally refactored)**
- `biophilia.audit.chronicle` – Cryptographic append-only action log (SHA-256 hash chain)
- `biophilia.audit.impact_audit` – Pre-action ethical gate (decorator pattern, no circular imports)
- `biophilia.biosemiotics.interpreter` – Signal classification engine (BioState enum, frozen BioSignal dataclass)
- `biophilia.biosemiotics.entropy_detector` – Weighted dissonance calculator per network node
- `biophilia.biosemiotics.entropy_response` – Context-aware system response recommendations
- `biophilia.governance.layer` – Three-pillar veto / approval logic (Säulen I–III)
- `biophilia.governance.homeostasis` – Trend-watching controller with O(1) rolling-window (deque)
- `biophilia.governance.synergy` – Coherence-based pattern detection (1+1=3)
- `biophilia.actions.controller` – BioState → action mapping  
- `biophilia.actions.interface` – Actuator interface with pre-action audit gate
- `biophilia.cloud.governor` – Biologically-inspired cloud resource manager (vitality model)
- `biophilia.infrastructure.logger` – Structured zone-aware pulse logging
- `biophilia.orchestration.application` – Root `BIFApplication` class + CLI entry point
- `biophilia.orchestration.simulation` – Multi-node environment data generator
- `biophilia.orchestration.dashboard` – Real-time ASCII integrity monitor

**CLI & Scripts**
- `biophilia-run` console script (via pyproject.toml) for easy simulation startup
- `scripts/run_simulation.py` – Standalone wrapper with CLI args  
- `scripts/analyze_integrity.py` – Veto-report analyser for the chronicle

**Data & Config**
- `src/biophilia/_data/biophilic_baseline.json` – Multi-node network baseline (bundled resource)
- `src/biophilia/_data/vocal_patterns.json` – Audio-semiotics pattern library (bundled resource)
- `importlib.resources` integration for zero filesystem path wrangling

**Dev Tools**
- pytest + pytest-cov for unit testing and coverage reporting
- mypy for strict static type checking
- ruff for fast linting and formatting
- python-dotenv for optional `.env` file support

#### Changed

**Breaking: Complete Restructuring**

Old (prototype) structure:
```
biophilia-biosemiotics/
├── implementation/prototypes/
│   └── *.py
├── governance/
│   └── *.py
└── orchestration/
    ├── main.py
    └── ...
```

New (professional package):
```
src/biophilia/
├── audit/
├── biosemiotics/
├── governance/
├── actions/
├── cloud/
├── infrastructure/
├── orchestration/
└── _data/
```

**Imports Are Now Proper**
- ❌ Before: `sys.path.append()` hacks, circular imports via `main.py`
- ✅ After: Clean relative imports, no sys.path manipulation, proper package namespacing  

**All Components Refactored for Clarity**

| Component | Before | After |
|-----------|--------|-------|
| IntegrityChronicle | 97 lines, relative paths | 130 lines, Path API, docstrings |
| GovernanceLayer | 84 lines, no types | 100 lines, full type hints, frozen dataclass |
| BiophilicEntropyDetector | 71 lines, raw JSON | 120 lines, typed, bundled resources |
| BiophilicHomeostasisController | uses `list.pop(0)` O(n) | uses `deque(maxlen=)` O(1) |
| BiophilicActionInterface | implicit detector | explicit `self._detector` ref, no circular import |
| BiophilicCloudGovernor | raw script | proper module with ABC + subclasses |

**Imports & Dependencies**
- Zero mandatory runtime dependencies (pure stdlib + bundled data)
- Optional: `python-dotenv` for `.env` support
- Dev: pytest, mypy, ruff, coverage

#### Fixed

**Critical Issues**
- Circular import: `impact_audit.py` ← `main.py` ← (was importing from `main`) → **Solved:** audit reads detector via `self._detector` attribute
- Hardcoded paths: `../../logs` navigation → **Solved:** `Path` API + `importlib.resources` for bundled files
- Global singletons in `main.py` → **Solved:** `BIFApplication` owns all instances via constructor DI
- Missing type hints → **Solved:** Full PEP 484 coverage (with `from __future__ import annotations`)
- `list.pop(0)` O(n) inefficiency in `correction_history` → **Solved:** `deque(maxlen=)`
- Inconsistent logging (print vs logging module) → **Solved:** `BiophilicLogger` wraps Python logging

**Test Suite**
- 73 tests across 8 modules
- Tests for import paths, type instantiation, fixture isolation
- Fixed 2 test logic errors (veto thresholds, spike detection edge-case)

#### Removed

- Old prototype entry point (`python biophilia-biosemiotics/orchestration/main.py`)
- Legacy flat JSON baseline format (single-node structure) — now supports multi-node configs
- Raw `print()` debugging throughout codebase

### Backwards Compatibility

**NOT backwards compatible** – this is a major overhaul. 

Migration from 0.1.x:
1. Update imports: `from entropy_detector import ...` → `from biophilia.biosemiotics.entropy_detector import ...`
2. Create `.env` file with `BIF_SECRET_KEY` (was `os.getenv()` without error checking)
3. Initialize via `BIFApplication()` instead of global singletons
4. Use `uv sync` to install (or `pip install -e .`)

### Testing

```bash
uv run pytest tests/ -v  # 73 tests, 0.22s runtime, 100% pass
uv run pytest tests/ --cov=src/biophilia --cov-report=html  # Coverage report
uv run mypy src/biophilia  # Type checking (strict mode)
```

### Documentation

- Updated `README.md` with package installation & usage
- New `DEVELOPMENT.md` with architecture, testing guide, troubleshooting
- New `.env.example` template
- Docstrings on all public classes/methods (Google-style)

### Known Limitations

1. **Mypy strictness:** Some JSON-heavy functions have `# type: ignore[type-arg]` for untyped JSON dicts (acceptable pattern in Python ecosystem)
2. **Cloud governor:** K8s adapter is stubbed (simulated API calls only)
3. **Multi-processing:** Cloud governor uses `multiprocessing` (not async); suitable for CPU-bound work
4. **Dashboard:** ASCII rendering depends on terminal width (142 chars fixed for best layout)

### Performance

- Full network tick (2 nodes): ~5ms
- Integrity verification (10k records): ~50ms
- Chronicle append: O(1)
- Trend analysis: O(history_depth) with deque rolling window
- Synergy scan: O(sensor_count²) coherence checks

---

## [0.1.0] – 2026-05-06

Initial prototype release from Claude + Gemini collaboration.
- Core three-pillar logic
- Prototype orchestration loop
- Manual script-based simulation
- Biosemiotic interpretation engine
- Integrity chronicle (blockchain pattern)

(This release is superseded by 0.2.0)

---

## Planned for Future

- [ ] Async/await orchestration layer
- [ ] Real Kubernetes adapter (not stubbed)
- [ ] REST API for remote nodes
- [ ] Distributed consensus for multi-site deployments
- [ ] Visualization dashboard (web UI)
- [ ] Telemetry integration (Prometheus exporter)
- [ ] Multi-language client libraries (Go, Rust, TypeScript)

