# Development Guide

## Quick Start

```bash
# Clone the repository
cd biophilia

# Install with uv (recommended)
uv sync --all-extras

# Run tests
uv run pytest tests/ -v

# Run the simulation
BIF_SECRET_KEY=test-key uv run python scripts/run_simulation.py
```

## Project Structure

```
src/biophilia/
├── __init__.py
├── audit/
│   ├── chronicle.py          # Tamper-evident action log (blockchain pattern)
│   └── impact_audit.py        # Pre-action ethical gate (decorator)
├── biosemiotics/
│   ├── interpreter.py         # Signal classification (BioState, BioSignal)
│   ├── entropy_detector.py    # Weighted dissonance calculation
│   └── entropy_response.py    # Context-aware recommendations
├── governance/
│   ├── layer.py               # Three-pillar veto & approval logic
│   ├── homeostasis.py         # Trend-watching controller
│   └── synergy.py             # Pattern detection (1+1=3)
├── actions/
│   ├── controller.py          # BioState → action mapping
│   └── interface.py           # Actuator interface + audit gate
├── cloud/
│   └── governor.py            # Biophilic cloud resource manager
├── infrastructure/
│   └── logger.py              # Structured pulse logging
├── orchestration/
│   ├── application.py         # Root app + CLI entry point
│   ├── simulation.py          # Multi-node environment sim
│   └── dashboard.py           # ASCII monitoring console
└── _data/
    ├── biophilic_baseline.json
    └── vocal_patterns.json
```

## Three Pillars

**Pillar I – Non-Maleficence (Schutz)**
- Blocks actionism when dissonance is below the safe threshold.
- Prevents unnecessary intervention (let the system breathe).
- Implemented by `GovernanceLayer.validate()`.

**Pillar II – Ethical Agency (Rettung)**
- Emergency override when life integrity is threatened.
- Forced activation under CRITICAL state or when `is_mandatory=True`.
- No negotiation: existence comes first.

**Pillar III – Open Knowledge (Verbundenheit)**
- Recognizes and endorses emergent synergy patterns (1 + 1 = 3).
- Decentralized, self-organising insights from the network.
- Logged in the tamper-evident chronicle.

## Key Classes

### `BIFApplication`
Root orchestrator that assembles all subsystems and exposes `run_network_tick()`.

```python
from biophilia.orchestration.application import BIFApplication

app = BIFApplication(baseline_path=None, log_dir=None)
# Requires: BIF_SECRET_KEY environment variable

sensor_data = {
    "Forest_Node_01": {
        "audio_harmony": 0.85,
        "soil_moisture": 45.0,
        "ambient_light": 600.0,
        "mycelium_activity": 0.5,
    }
}
app.run_network_tick(sensor_data)
```

### `IntegrityChronicle`
Append-only, hash-chained audit log. Any post-hoc modification is detected.

```python
from biophilia.audit.chronicle import IntegrityChronicle

chronicle = IntegrityChronicle(log_dir=Path("./logs"))
chronicle.record_action(
    node_name="Forest_Node_01",
    action_name="GENTLE_SUPPORT",
    pillar="PILLAR II",
    reason="Mycelium deficit detected",
    synergy_score=2.5
)

# Verify the chain is intact
assert chronicle.verify_integrity() is True
```

### `GovernanceLayer`
Implements the three-pillar decision tree.

```python
from biophilia.governance.layer import GovernanceLayer

gov = GovernanceLayer()
ctx = {
    "dissonance": 0.25,
    "state": "HARMONY",
    "synergy_active": False,
    "is_mandatory": False,
}
decision = gov.validate("GENTLE_SUPPORT", ctx)
# Returns: GovernanceDecision(approved=True|False, final_action=..., reason=...)
```

## Running Tests

```bash
# All tests
uv run pytest tests/ -v

# Specific test file
uv run pytest tests/test_governance.py -v

# With coverage
uv run pytest tests/ --cov=src/biophilia --cov-report=html

# Type checking
uv run mypy src/biophilia

# Linting (ruff)
uv run ruff check src/biophilia
```

## Environment Variables

Required:
- `BIF_SECRET_KEY` – HMAC key for actuator access (fail-fast if not set)

Optional:
- `BIF_LOG_DIR` – Directory for logs (default: `./logs`)
- `BIF_BASELINE_PATH` – Path to custom network baseline JSON
- `BIF_PUMP_API_URL` – Actuator endpoint (default: `http://localhost/pump`)

Example `.env`:
```
BIF_SECRET_KEY=your-32-char-hex-string-here-do-not-commit
BIF_LOG_DIR=./logs
BIF_PUMP_API_URL=http://localhost:8080/pump
```

## Adding a New Subsystem

1. Create a new package under `src/biophilia/subsystem_name/`.
2. Add an `__init__.py` with clean public exports.
3. Write unit tests in `tests/test_subsystem_name.py`.
4. Update the docstring in the module explaining its pillar alignment.
5. Add the subsystem to `BIFApplication.__init__()`.

## Common Patterns

### Accessing System Dissonance (for decorators/gates)
```python
detector = self._detector  # BiophilicEntropyDetector instance
current_dissonance = detector.last_calculated_dissonance  # float
```

### Logging Pulses
```python
logger = BiophilicLogger(log_dir=Path("./logs"))
logger.log_pulse(zone="Forest_Node_01-ZoneA", message="Sensing pulse", data=sensor_data)
```

### Recording Actions in the Chronicle
```python
chronicle.record_action(
    node_name="Forest_Node_01",
    action_name="EMERGENCY_STABILIZATION",
    pillar="PILLAR II",
    reason={"moral": "life_preservation", "metric": "dissonance_0.75"},
    synergy_score=0.0
)
```

## Performance Notes

- `HomeostasisController` uses `collections.deque(maxlen=10)` for O(1) rolling-window ops.
- `IntegrityChronicle` reads/writes JSON synchronously (OK for ~10k records).
- `BiophilicDashboard` clears terminal with ANSI escape codes (no external deps).
- Multi-node processing is single-threaded (sequential per node per tick).

## Troubleshooting

**"BIF_SECRET_KEY is not set"**
→ Set the environment variable before running:
```bash
export BIF_SECRET_KEY=your-key-here
```

**"Chronicle file is structurally corrupt"**
→ Check `logs/biophilic_integrity_history.json` for valid JSON.
→ Restore from backup if tampering is suspected.

**"MANIPULATION DETECTED: entry at index N was modified"**
→ The hash-chain detected post-hoc modification.
→ Refuse to start the system (as designed).

**Tests fail with import errors**
→ Ensure `uv sync` was run: `uv sync --all-extras`
→ Check Python version: Python 3.11+ required.

## Contributing

Ensure:
1. All new code has type hints (use `from __future__ import annotations`).
2. Every public class/function has a docstring.
3. Tests must cover happy-path and error cases.
4. Commit messages reference the pillar(s) affected.

Example:
```
Pillar I: prevent actionism in transient noise
- Increase dead-zone from 3% to 5% in entropy detector
- Add test case: test_dead_zone_tolerates_sensor_noise
```

---

**Last updated:** May 2026  
**Framework status:** Complete, tested, production-ready with proper warnings

