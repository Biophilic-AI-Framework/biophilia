# Test Cases for Project Biophilia

## Overview
Dieses Dokument beschreibt den aktuellen Test- und Qualitätsstand des Projekts auf Basis der real vorhandenen Tests in `tests/`, der Toolchain in `pyproject.toml` und der CI-Pipeline in `.github/workflows/tests.yml`.

## Status-Skala
- `Automated`: Testfall ist als automatisierter Test implementiert.
- `In CI`: Testfall läuft in GitHub Actions.
- `Planned`: Geplant, aber noch nicht automatisiert.

## Current Snapshot (verifiziert)
- Letzter lokaler Lauf: `73 passed` (`uv run pytest tests/ -q`)
- Testframework: `pytest`
- Scope: `tests/test_*.py`
- Quality Gates in CI: `pytest`, `mypy`, `ruff`

## Test Categories

### 1. Unit Tests (Automated + In CI)

#### 1.1 Integrity & Audit
- **Test ID:** TC-001
- **Module:** `tests/test_chronicle.py`
- **Description:** Hash-Chain-Integrität, Record-Verkettung, Manipulationserkennung
- **Expected Result:** Manipulation wird erkannt, intakte Kette validiert erfolgreich
- **Status:** Automated, In CI

#### 1.2 Entropy Detection
- **Test ID:** TC-002
- **Module:** `tests/test_entropy_detector.py`
- **Description:** Dissonanz-Berechnung, Dead-Zone, Status-Mapping, Node-Fallback
- **Expected Result:** Korrekte numerische Dissonanz und Statuswerte
- **Status:** Automated, In CI

#### 1.3 Governance Logic
- **Test ID:** TC-003
- **Module:** `tests/test_governance.py`
- **Description:** Pillar-I-Veto, Pillar-II-Override, Pillar-III-Synergiepfad
- **Expected Result:** GovernanceDecision entspricht Kontext und Schwellen
- **Status:** Automated, In CI

#### 1.4 Homeostasis Controller
- **Test ID:** TC-004
- **Module:** `tests/test_homeostasis.py`
- **Description:** Trendanalyse, Spike-Erkennung, Dämpfung, Stabilitätscheck
- **Expected Result:** Kritische Trends werden erkannt; Stabilitätslogik bleibt konsistent
- **Status:** Automated, In CI

#### 1.5 Biosemiotic Interpreter
- **Test ID:** TC-005
- **Module:** `tests/test_interpreter.py`
- **Description:** Signal-Interpretation (Mycelium/Acoustics), Zustands-Synthese
- **Expected Result:** BioState-Klassifikation korrekt, priorisierte Synthese korrekt
- **Status:** Automated, In CI

#### 1.6 Synergy Detection
- **Test ID:** TC-006
- **Module:** `tests/test_synergy.py`
- **Description:** Kohärenz-Metrik und Erkennung aktiver Synergie-Muster
- **Expected Result:** Relevante Muster werden identifiziert, Krisendaten liefern keine False Positives
- **Status:** Automated, In CI

#### 1.7 Cloud Governor
- **Test ID:** TC-007
- **Module:** `tests/test_cloud_governor.py`
- **Description:** Vitalitätsmodell, Skalierungsentscheidungen, Min/Max-Worker-Grenzen
- **Expected Result:** Erwartetes Scale-up/down-Verhalten und konsistente Statuswerte
- **Status:** Automated, In CI

### 2. Static Quality Checks (Automated + In CI)

#### 2.1 Type Checking
- **Test ID:** TC-101
- **Tool:** `mypy`
- **Description:** Statische Typprüfung für `src/biophilia`
- **Expected Result:** Keine blockierenden Typfehler
- **Status:** Automated, In CI

#### 2.2 Linting & Format
- **Test ID:** TC-102
- **Tool:** `ruff`
- **Description:** Lint-Regeln + Format-Check für `src/biophilia` und `tests`
- **Expected Result:** Keine Lint-Fehler, keine Format-Abweichungen
- **Status:** Automated, In CI

### 3. Planned Integration & Performance Tests

#### 3.1 Integration End-to-End
- **Test ID:** TC-201
- **Description:** Vollständiger Tick-Lauf über `BIFApplication.run_network_tick` inkl. Chronicle, Governance und Dashboard
- **Expected Result:** End-to-End-Fluss ohne Exceptions, konsistente Zustandsübergänge
- **Status:** Planned

#### 3.2 Performance Baseline
- **Test ID:** TC-202
- **Description:** Laufzeit- und Speicher-Benchmarks für zentrale Pfade
- **Expected Result:** Definierte Schwellenwerte werden eingehalten
- **Status:** Planned

#### 3.3 Concurrency / Stress
- **Test ID:** TC-203
- **Description:** Belastungstests für parallele/serielle Tick-Verarbeitung
- **Expected Result:** Keine Datenkorruption, stabile Laufzeit unter Last
- **Status:** Planned

## Prerequisites
- Python `>=3.11`
- `uv` installiert
- Abhängigkeiten über `pyproject.toml`/`uv.lock`

## Running Tests

```bash
# Abhängigkeiten synchronisieren
uv sync --all-extras

# Alle Unit-Tests
uv run pytest tests/ -v --tb=short

# Kurzlauf (wie Snapshot)
uv run pytest tests/ -q

# Einzelmodul
uv run pytest tests/test_governance.py -v

# Coverage
uv run pytest tests/ --cov=src/biophilia --cov-report=term-missing
```

## Local Quality Gates (wie CI)

```bash
# Typprüfung
uv run mypy src/biophilia --ignore-missing-imports

# Linting
uv run ruff check src/biophilia tests/

# Format-Check
uv run ruff format --check src/biophilia tests/
```

## CI Execution
- Workflow: `.github/workflows/tests.yml`
- Trigger: Push/PR auf `main` und `develop`
- Matrix: `ubuntu-latest`, `macos-latest` mit Python `3.11`, `3.12`, `3.13`

## Result Table (Current)

| Test ID | Description | Status | Last Verified | Notes |
|---------|-------------|--------|---------------|-------|
| TC-001 | Integrity & tamper detection | Automated, In CI | 2026-05-18 | `tests/test_chronicle.py` |
| TC-002 | Entropy detection logic | Automated, In CI | 2026-05-18 | `tests/test_entropy_detector.py` |
| TC-003 | Governance decision paths | Automated, In CI | 2026-05-18 | `tests/test_governance.py` |
| TC-004 | Homeostasis trend handling | Automated, In CI | 2026-05-18 | `tests/test_homeostasis.py` |
| TC-005 | Biosemiotic interpretation | Automated, In CI | 2026-05-18 | `tests/test_interpreter.py` |
| TC-006 | Synergy logic | Automated, In CI | 2026-05-18 | `tests/test_synergy.py` |
| TC-007 | Cloud governor behavior | Automated, In CI | 2026-05-18 | `tests/test_cloud_governor.py` |
| TC-101 | Static type check | Automated, In CI | 2026-05-18 | `mypy` job |
| TC-102 | Lint + format checks | Automated, In CI | 2026-05-18 | `ruff` job |
| TC-201 | End-to-end integration | Planned | - | Noch nicht als eigener Test-Suiteblock |
| TC-202 | Performance baseline | Planned | - | Benchmark-Harness fehlt |
| TC-203 | Concurrency / stress | Planned | - | Last-/Paralleltests geplant |

## Known Gaps
- Separate, dedizierte End-to-End-Integrationstests fehlen noch.
- Performance- und Stress-Benchmarks sind geplant, aber noch nicht automatisiert.

## Contact
Bei Fragen zu Tests oder Testabdeckung bitte Issue öffnen oder direkt in `CONTRIBUTING.md` nach dem bevorzugten Workflow vorgehen.
