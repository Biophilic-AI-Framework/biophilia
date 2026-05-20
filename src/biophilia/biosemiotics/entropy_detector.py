"""
entropy_detector.py – Weighted dissonance calculation per network node (Säule I).

Dissonance is a normalised, weighted deviation of current sensor readings from
their biological ideals.  A dead-zone of 5 % is applied before weighting to
suppress sensor noise that lies within healthy variance.

A single high-impact sensor can dominate the overall score when its weighted
deviation exceeds 0.25, providing an early-warning floor for acute shocks.
"""

from __future__ import annotations

import json
import logging
from importlib.resources import files
from pathlib import Path

logger = logging.getLogger(__name__)

_FALLBACK_NODE = "Forest_Node_01"


class BiophilicEntropyDetector:
    """
    Compute and cache the dissonance score for any node in the network.

    Parameters
    ----------
    baseline_path:
        Path to a *network* baseline JSON file (multi-node format).
        Pass ``None`` to load the bundled default from ``biophilia._data``.
    """

    def __init__(self, baseline_path: Path | str | None = None) -> None:
        if baseline_path is None:
            data_file = files("biophilia._data").joinpath("biophilic_baseline.json")
            config: dict = json.loads(data_file.read_text(encoding="utf-8"))  # type: ignore[assignment]
        else:
            with open(baseline_path, encoding="utf-8") as fh:
                config = json.load(fh)

        if "nodes" in config:
            self.nodes_matrix: dict = config["nodes"]  # type: ignore[assignment]
        else:
            # Backwards-compatible single-node format.
            self.nodes_matrix = {
                _FALLBACK_NODE: {
                    "baseline": config.get("baseline", {}),
                    "thresholds": config.get("thresholds", {}),
                }
            }

        self.last_calculated_dissonance: float = 0.0
        logger.debug(
            "EntropyDetector loaded %d nodes: %s",
            len(self.nodes_matrix),
            list(self.nodes_matrix),
        )

    # ── Core calculation ──────────────────────────────────────────────────────

    def calculate_dissonance(self, node_name: str, current_sensors: dict[str, float]) -> float:
        """
        Return a [0, ∞) dissonance score for *node_name* given *current_sensors*.

        The result is stored in ``last_calculated_dissonance`` for use by the
        impact-audit decorator without any module-level coupling.
        """
        node_cfg = self.nodes_matrix.get(node_name, self.nodes_matrix[_FALLBACK_NODE])
        baseline: dict[str, dict[str, float]] = node_cfg["baseline"]

        total_deviation = 0.0
        total_weight = 0.0
        max_single_deviation = 0.0
        _DEAD_ZONE = 0.05

        for sensor, value in current_sensors.items():
            if sensor not in baseline:
                continue
            ideal: float = baseline[sensor]["ideal"]
            weight: float = baseline[sensor]["weight"]

            raw_dev = abs(value - ideal) / (ideal + 1e-9)
            effective_dev = max(0.0, raw_dev - _DEAD_ZONE)
            weighted_dev = effective_dev * weight

            total_deviation += weighted_dev
            total_weight += weight

            if weighted_dev > max_single_deviation:
                max_single_deviation = weighted_dev

        avg = total_deviation / total_weight if total_weight > 0 else 0.0

        # Acute single-sensor shock must not be averaged away.
        final = max(avg, max_single_deviation * 0.8) if max_single_deviation > 0.25 else avg
        self.last_calculated_dissonance = round(final, 4)
        return self.last_calculated_dissonance

    def get_status(self, node_name: str, dissonance: float) -> str:
        """Map a dissonance score to a human-readable severity label."""
        node_cfg = self.nodes_matrix.get(node_name, self.nodes_matrix[_FALLBACK_NODE])
        thresholds: dict[str, float] = node_cfg["thresholds"]

        if dissonance >= thresholds["dissonance_critical"]:
            return "CRITICAL_DISSONANCE"
        if dissonance >= thresholds["dissonance_warning"]:
            return "WARNING_DISSONANCE"
        return "HARMONY"
