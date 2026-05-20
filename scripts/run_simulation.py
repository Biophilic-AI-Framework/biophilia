#!/usr/bin/env python3
"""
run_simulation.py – Convenience wrapper for the BIF real-time simulation.

Usage:
    python scripts/run_simulation.py [--log-dir PATH] [--baseline PATH]

The script reads BIF_SECRET_KEY from the environment (or a .env file if
python-dotenv is installed).
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path

# Try to load .env automatically when python-dotenv is available.
try:
    from dotenv import load_dotenv

    load_dotenv()
except ModuleNotFoundError:
    pass  # Optional dependency – skip silently.

# Ensure the package is importable when running from the repo root without
# an editable install.
_SRC = Path(__file__).parent.parent / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Start the BIF network simulation.")
    p.add_argument(
        "--log-dir",
        type=Path,
        default=None,
        help="Directory for pulse log and chronicle (default: ./logs).",
    )
    p.add_argument(
        "--baseline",
        type=Path,
        default=None,
        help="Path to a custom network-baseline JSON (default: bundled data).",
    )
    p.add_argument(
        "--tick",
        type=float,
        default=4.0,
        help="Seconds between simulation ticks (default: 4).",
    )
    p.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging level (default: INFO).",
    )
    return p.parse_args()


def main() -> None:
    args = _parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s | %(name)-35s | %(levelname)-8s | %(message)s",
    )

    if not os.getenv("BIF_SECRET_KEY"):
        logging.critical(
            "BIF_SECRET_KEY is not set.  "
            "Copy .env.example → .env and provide a value."
        )
        sys.exit(1)

    # Import after sys.path is patched.
    from biophilia.audit.chronicle import IntegrityChronicle
    from biophilia.orchestration.application import BIFApplication
    from biophilia.orchestration.simulation import BiophilicSimulationSuite

    app = BIFApplication(baseline_path=args.baseline, log_dir=args.log_dir)

    logging.info("Verifying chronicle integrity …")
    if not app.chronicle.verify_integrity():
        logging.critical("Chronicle tampered with — aborting.")
        sys.exit(1)

    logging.info("Starting BIF network simulation (tick=%.1fs).", args.tick)
    suite = BiophilicSimulationSuite(tick_interval=args.tick)
    suite.run_infinite_simulation(app.run_network_tick)


if __name__ == "__main__":
    main()

