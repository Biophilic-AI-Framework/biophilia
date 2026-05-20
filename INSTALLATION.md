# Installation & Usage

## Prerequisites

- Python 3.11 or later
- `uv` package manager (recommended) or `pip`

## Installation

### Option 1: Using `uv` (Recommended)

```bash
# Clone the repository
git clone https://github.com/Biophilic-AI-Framework/biophilia.git
cd biophilia

# Sync dependencies (installs in .venv)
uv sync --all-extras

# Run the simulation
export BIF_SECRET_KEY="your-secret-key-here"
uv run biophilia-run
```

### Option 2: Using `pip`

```bash
git clone https://github.com/Biophilic-AI-Framework/biophilia.git
cd biophilia

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e ".[dev]"

# Run the simulation
export BIF_SECRET_KEY="your-secret-key-here"
python -m biophilia.orchestration.application
```

### Option 3: From PyPI (Coming Soon)

```bash
pip install biophilia-framework
```

## Quick Start

### 1. Set Up Environment

```bash
# Copy the template
cp .env.example .env

# Edit .env and set BIF_SECRET_KEY
nano .env  # or your preferred editor
```

Required environment variable:
- `BIF_SECRET_KEY`: A secret key for HMAC-based actuator authentication (any non-empty string works for testing)

Optional:
- `BIF_LOG_DIR`: Directory for logs (default: `./logs`)
- `BIF_BASELINE_PATH`: Path to a custom network baseline JSON
- `BIF_PUMP_API_URL`: Actuator endpoint (default: `http://localhost/pump`)

### 2. Run the Simulation

```bash
# Load .env and start the simulation
uv run biophilia-run

# Or with command-line overrides
uv run biophilia-run --log-dir ./my_logs --tick 2.0
```

You should see:

```
🌿 BIF NETWORK INTEGRITY MONITOR  │  2026-05-18T14:32:45
🔒 CRYPTO-CHAIN-HEAD: 0000000…
═════════════════════════════════════════════════════════════════
METRIC / SENSOR    ‖ FOREST_NODE_01           ‖ FOREST_NODE_02
────────────────────────────────────────────────────────────────
🔊 Audio Harmony   ‖ 0.85                     ‖ 0.80
💧 Soil Moisture   ‖ 45.0 %                   ‖ 42.0 %
...
```

### 3. Interpret the Dashboard

**Columns:**
- **Left:** Sensor metric labels
- **Center:** Forest_Node_01 (primary biosphere monitoring point)
- **Right:** Forest_Node_02 (deep-forest periphery)

**Key Indicators:**
- 🟩 **Green barometer:** System in harmony (dissonance < 0.2)
- 🟨 **Yellow barometer:** Warning zone (dissonance 0.2–0.5)
- 🟥 **Red barometer:** Critical (dissonance ≥ 0.5)

**Actions:**
- `EMERGENCY_STABILIZATION`: Life-threatening situation (Pillar II)
- `GENTLE_SUPPORT`: Healing phase (intermediate stress)
- `ENHANCE_VITALITY`: System is healthy, supporting growth (Pillar III)
- `OBSERVE_AND_WAIT`: System is stable, no intervention needed

**Pillars:**
- **PILLAR I (Non-Maleficence):** Vetoes actionism when dissonance is below the safe threshold
- **PILLAR II (Duty to Save):** Forces emergency intervention when life is threatened
- **PILLAR III (Connectedness):** Recognizes and endorses cooperative synergy patterns

## Running Tests

```bash
# Run all unit tests
uv run pytest tests/ -v

# Run with coverage report
uv run pytest tests/ --cov=src/biophilia

# Run a specific test module
uv run pytest tests/test_governance.py -v
```

Expected output:
```
============================== 73 passed in 0.22s ==============================
```

## Using in Your Own Code

```python
from biophilia.orchestration.application import BIFApplication
from pathlib import Path
import os

# Set the secret key (security requirement)
os.environ["BIF_SECRET_KEY"] = "your-key-here"

# Instantiate the application
app = BIFApplication(
    baseline_path=None,  # None = use bundled default
    log_dir=Path("./logs")
)

# Verify integrity (fails if chronicle was tampered with)
if not app.chronicle.verify_integrity():
    raise RuntimeError("Chronicle has been modified!")

# Process a single network tick
sensor_data = {
    "Forest_Node_01": {
        "audio_harmony": 0.85,
        "soil_moisture": 45.0,
        "ambient_light": 600.0,
        "mycelium_activity": 0.5,
    }
}

app.run_network_tick(sensor_data)

# Last chronicle hash (for distributed consensus)
last_hash = app.chronicle.get_last_hash()
print(f"Latest chain head: {last_hash}")
```

## Example: Custom Baseline

Create a `custom_baseline.json`:

```json
{
  "framework": "Biophilic_Integrity_Framework",
  "nodes": {
    "My_Custom_Node": {
      "baseline": {
        "temperature": {"ideal": 25.0, "weight": 3.0, "unit": "celsius"},
        "humidity": {"ideal": 60.0, "weight": 2.0, "unit": "percent"}
      },
      "thresholds": {
        "dissonance_warning": 0.25,
        "dissonance_critical": 0.60
      }
    }
  }
}
```

Then:

```bash
export BIF_BASELINE_PATH=./custom_baseline.json
uv run biophilia-run
```

## Troubleshooting

### Error: "BIF_SECRET_KEY is not set"

**Cause:** The environment variable is not defined.

**Solution:**
```bash
export BIF_SECRET_KEY="your-secure-key-here"
# Or add to .env:
echo "BIF_SECRET_KEY=your-key" >> .env
```

### Error: "Chronicle file is structurally corrupt"

**Cause:** The JSON log file is malformed.

**Solution:**
```bash
# Backup and delete the problematic file
mv logs/biophilic_integrity_history.json logs/biophilic_integrity_history.json.bak
# Re-run: a new chronicle will be created
uv run biophilia-run
```

### Error: "MANIPULATION DETECTED"

**Cause:** The integrity check found that the chronicle was modified after recording.

**Solution:** This is a *security feature*. The system refuses to start because the audit log has been tampered with.
- Restore from a backup
- Investigate how the file was modified
- Review access controls

### Tests fail with "import errors"

**Cause:** Dependencies not installed.

**Solution:**
```bash
uv sync --all-extras
```

## File Locations

After running the simulation, you'll see:

```
./
├── .env                                    # Your configuration
├── logs/
│   ├── biophilia_pulse.log                 # Timestamped pulse events
│   └── biophilic_integrity_history.json    # Hash-chained audit log
└── .venv/                                  # Virtual environment (if using pip)
```

Check the logs:

```bash
# Real-time pulse log
tail -f logs/biophilia_pulse.log

# Audit chronicle (JSON)
less logs/biophilic_integrity_history.json
```

## Next Steps

- Read [`DEVELOPMENT.md`](DEVELOPMENT.md) for architecture details
- Review [`CHANGELOG.md`](CHANGELOG.md) for version history
- Explore the three-pillar logic in [`src/biophilia/governance/layer.py`](src/biophilia/governance/layer.py)
- Check [`README.md`](README.md) for the philosophical background

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation
- Review test cases for usage examples

---

**Last updated:** May 2026  
**Framework status:** Production-ready  
**Python version:** 3.11+

