#!/usr/bin/env python3
"""
analyze_integrity.py – Veto-report analyser for the BIF chronicle.

Scans the integrity chronicle and prints all records where the governance
layer issued a "true" veto (i.e. a blocking intervention was proposed but
the systemic analysis says the system was in harmony).

Usage:
    python scripts/analyze_integrity.py [--chronicle PATH]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SRC = Path(__file__).parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Analyse BIF veto records.")
    p.add_argument(
        "--chronicle",
        type=Path,
        default=Path("logs") / "biophilic_integrity_history.json",
        help="Path to the chronicle JSON (default: logs/biophilic_integrity_history.json).",
    )
    return p.parse_args()


def analyze_vetos(chronicle_path: Path) -> None:
    if not chronicle_path.exists():
        print(f"Chronicle not found: {chronicle_path}", file=sys.stderr)
        sys.exit(1)

    with chronicle_path.open(encoding="utf-8") as fh:
        try:
            history = json.load(fh)
        except json.JSONDecodeError as exc:
            print(f"Could not parse chronicle: {exc}", file=sys.stderr)
            sys.exit(1)

    print(f"── 🛡️  BIF VETO REPORT (Pillar II) ── {len(history)} records total\n")

    vetos_found = 0
    for entry in history:
        reason = entry.get("reason")
        if not isinstance(reason, dict):
            continue

        systemic = reason.get("systemic_analysis", "")
        bio_state = reason.get("biosemiotic_state", "")
        action = entry.get("action", "")

        # A "true" veto: system claims harmony but an intervention was still attempted.
        if "harmony" in systemic.lower() and action != "ENHANCE_VITALITY":
            ts = entry.get("timestamp", "unknown")
            print(f"[{ts}]  VETO DETECTED")
            print(f"  Systemic analysis : {systemic}")
            print(f"  Biosemiotic state : {bio_state}")
            print(f"  Chosen action     : {action}\n")
            vetos_found += 1

    if vetos_found == 0:
        print("No veto anomalies detected.  The chronicle is clean.")
    else:
        print(f"Total veto anomalies: {vetos_found}")


def main() -> None:
    args = _parse_args()
    analyze_vetos(args.chronicle)


if __name__ == "__main__":
    main()

