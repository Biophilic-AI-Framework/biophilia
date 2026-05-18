"""
entropy_response.py – Context-aware action recommendation (Säule II).

Translates a status code + dissonance score into a structured response dict
that downstream governance and action layers can consume.

Bug fixed vs. original: the detector is now accessed via ``nodes_matrix``
(multi-node format) rather than the removed flat ``baseline`` attribute.
"""

from __future__ import annotations

import logging

from biophilia.biosemiotics.entropy_detector import BiophilicEntropyDetector

logger = logging.getLogger(__name__)

_STATUS_MAP = {
    "CRITICAL_DISSONANCE": "CRITICAL",
    "WARNING_DISSONANCE": "STRESS",
    "HARMONY": "HARMONY",
}


class BiophilicResponse:
    """
    Translate a sensor status into the recommended corrective posture.

    Parameters
    ----------
    detector_ref:
        Optional reference to the active :class:`BiophilicEntropyDetector`.
        When provided, the STRESS branch can identify the *primary stressor*
        (the sensor with the highest normalised, weighted deviation).
    """

    def __init__(self, detector_ref: BiophilicEntropyDetector | None = None) -> None:
        self.detector = detector_ref

    def resolve(
        self,
        status: str,
        dissonance: float,
        sensor_data: dict[str, float],
        node_name: str = "Forest_Node_01",
    ) -> dict:  # type: ignore[type-arg]
        """
        Return a response dict with keys ``level``, ``action``, ``description``,
        and optionally ``is_mandatory`` (only set to ``True`` for CRITICAL).
        """
        normalised = _STATUS_MAP.get(status, "UNKNOWN")

        if normalised == "HARMONY":
            return {
                "level": "RESONANCE",
                "action": "OBSERVE_AND_WAIT",
                "description": (f"System in biological harmony (dissonance: {dissonance:.4f})."),
            }

        if normalised == "STRESS":
            primary_stressor = self._identify_stressor(sensor_data, node_name)
            return {
                "level": "SOFT_CORRECTION",
                "action": f"Initiate gradual support for '{primary_stressor}'.",
                "description": (
                    f"Weighted dissonance {dissonance:.4f} at '{primary_stressor}'. "
                    "System is seeking equilibrium."
                ),
            }

        if normalised == "CRITICAL":
            return {
                "level": "STABILIZATION",
                "action": "EMERGENCY_STABILIZATION",
                "description": (
                    f"Critical biological dissonance ({dissonance:.4f}). "
                    "Life integrity is under threat."
                ),
                "is_mandatory": True,
            }

        return {
            "level": "UNKNOWN",
            "action": "RE_EVALUATE_SENSORS",
            "description": "Status undefined – sensor re-evaluation required.",
        }

    def _identify_stressor(self, sensor_data: dict[str, float], node_name: str) -> str:
        """Return the name of the sensor with the greatest weighted deviation."""
        if self.detector is None:
            # No detector: return the sensor with the largest absolute value as proxy.
            return max(sensor_data, key=lambda k: sensor_data[k]) if sensor_data else "unknown"

        node_cfg = self.detector.nodes_matrix.get(
            node_name, next(iter(self.detector.nodes_matrix.values()))
        )
        baseline: dict[str, dict[str, float]] = node_cfg.get("baseline", {})

        primary = "unknown"
        max_weighted_dev = -1.0

        for sensor, val in sensor_data.items():
            if sensor not in baseline:
                continue
            ideal: float = baseline[sensor]["ideal"]
            weight: float = baseline[sensor]["weight"]
            raw_dev = abs(val - ideal) / (ideal + 1e-9)
            # Apply the same 12 % dead-zone used by BiophilicResponse (legacy compat).
            weighted_dev = max(0.0, raw_dev - 0.12) * weight
            if weighted_dev > max_weighted_dev:
                max_weighted_dev = weighted_dev
                primary = sensor

        return primary
