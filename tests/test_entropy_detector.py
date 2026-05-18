"""Tests for BiophilicEntropyDetector."""

from __future__ import annotations

import pytest

from biophilia.biosemiotics.entropy_detector import BiophilicEntropyDetector


@pytest.fixture()
def detector() -> BiophilicEntropyDetector:
    """Detector using the bundled default baseline."""
    return BiophilicEntropyDetector()


class TestDissonanceCalculation:
    def test_perfect_harmony_yields_zero(self, detector: BiophilicEntropyDetector) -> None:
        """Readings exactly at their ideal values → dissonance within dead-zone → 0."""
        ideal = {
            "audio_harmony": 0.85,
            "soil_moisture": 45.0,
            "ambient_light": 600.0,
            "mycelium_activity": 0.5,
        }
        d = detector.calculate_dissonance("Forest_Node_01", ideal)
        assert d == 0.0

    def test_crisis_yields_high_dissonance(self, detector: BiophilicEntropyDetector) -> None:
        crisis = {
            "audio_harmony": 0.02,
            "soil_moisture": 12.0,
            "mycelium_activity": 4.5,
        }
        d = detector.calculate_dissonance("Forest_Node_01", crisis)
        assert d > 0.5, f"Expected high dissonance, got {d}"

    def test_last_calculated_dissonance_is_updated(
        self, detector: BiophilicEntropyDetector
    ) -> None:
        sensors = {"audio_harmony": 0.02, "soil_moisture": 10.0}
        d = detector.calculate_dissonance("Forest_Node_01", sensors)
        assert detector.last_calculated_dissonance == d

    def test_unknown_sensor_is_ignored(self, detector: BiophilicEntropyDetector) -> None:
        """Sensors not in baseline must not crash or skew the result."""
        sensors = {"nonexistent_sensor": 999.0}
        d = detector.calculate_dissonance("Forest_Node_01", sensors)
        assert d == 0.0

    def test_fallback_to_node_01_for_unknown_node(self, detector: BiophilicEntropyDetector) -> None:
        """An unknown node name should fall back to Forest_Node_01 gracefully."""
        sensors = {"audio_harmony": 0.85}
        d = detector.calculate_dissonance("Unknown_Node_99", sensors)
        assert isinstance(d, float)

    def test_dissonance_is_rounded_to_4_decimals(self, detector: BiophilicEntropyDetector) -> None:
        sensors = {"audio_harmony": 0.5, "soil_moisture": 30.0}
        d = detector.calculate_dissonance("Forest_Node_01", sensors)
        assert d == round(d, 4)


class TestStatusMapping:
    def test_harmony_status(self, detector: BiophilicEntropyDetector) -> None:
        assert detector.get_status("Forest_Node_01", 0.05) == "HARMONY"

    def test_warning_status(self, detector: BiophilicEntropyDetector) -> None:
        assert detector.get_status("Forest_Node_01", 0.25) == "WARNING_DISSONANCE"

    def test_critical_status(self, detector: BiophilicEntropyDetector) -> None:
        assert detector.get_status("Forest_Node_01", 0.99) == "CRITICAL_DISSONANCE"

    def test_node_02_has_own_thresholds(self, detector: BiophilicEntropyDetector) -> None:
        # Node_02 warning threshold is 0.22 (vs 0.20 for Node_01).
        assert detector.get_status("Forest_Node_02", 0.21) == "HARMONY"
        assert detector.get_status("Forest_Node_02", 0.23) == "WARNING_DISSONANCE"
