"""Tests for HomeostasisController: trend analysis, damping, stability."""

from __future__ import annotations

import pytest

from biophilia.governance.homeostasis import HomeostasisController


@pytest.fixture()
def controller() -> HomeostasisController:
    thresholds = {"dissonance_warning": 0.20, "dissonance_critical": 0.50}
    baseline = {
        "soil_moisture": {"ideal": 45.0, "weight": 1.2, "unit": "percentage"},
        "audio_harmony": {"ideal": 0.85, "weight": 5.0, "unit": "harmony_index"},
    }
    return HomeostasisController(thresholds=thresholds, baseline_data=baseline)


class TestTrendAnalysis:
    def test_returns_false_with_insufficient_history(
        self, controller: HomeostasisController
    ) -> None:
        assert controller.analyze_trend(0.05) is False
        assert controller.analyze_trend(0.05) is False
        # Only 2 entries so far → still False.

    def test_stable_readings_return_false(self, controller: HomeostasisController) -> None:
        for _ in range(5):
            assert controller.analyze_trend(0.05) is False

    def test_persistent_high_dissonance_returns_true(
        self, controller: HomeostasisController
    ) -> None:
        for _ in range(5):
            result = controller.analyze_trend(0.25)
        assert result is True

    def test_acute_spike_returns_true_immediately(self, controller: HomeostasisController) -> None:
        # Feed two stable readings first (not enough for avg, but sets up history).
        controller.analyze_trend(0.01)
        controller.analyze_trend(0.01)
        # Spike at 1.5× warning_threshold (0.20) = 0.30; use 0.31 to avoid floating-point edge.
        result = controller.analyze_trend(0.31)
        assert result is True

    def test_rolling_window_limits_memory(self, controller: HomeostasisController) -> None:
        """Deque must not grow beyond maxlen."""
        for _ in range(50):
            controller.analyze_trend(0.01)
        assert len(controller.dissonance_history) <= 10


class TestDamping:
    def test_damping_reduces_delta(self, controller: HomeostasisController) -> None:
        delta = 10.0
        damped = controller.apply_damping(delta)
        assert damped < delta
        assert damped == pytest.approx(delta * 0.7)

    def test_zero_delta_stays_zero(self, controller: HomeostasisController) -> None:
        assert controller.apply_damping(0.0) == 0.0


class TestStabilityCheck:
    def test_value_at_ideal_is_stable(self, controller: HomeostasisController) -> None:
        assert controller.is_stable(45.0, "soil_moisture") is True

    def test_value_within_threshold_is_stable(self, controller: HomeostasisController) -> None:
        # 5 % of 45.0 = 2.25; value 46.0 is within range.
        assert controller.is_stable(46.0, "soil_moisture") is True

    def test_value_outside_threshold_is_not_stable(self, controller: HomeostasisController) -> None:
        # 48.0 → deviation = 3/45 ≈ 6.7 % > 5 %.
        assert controller.is_stable(48.0, "soil_moisture") is False

    def test_unknown_parameter_returns_stable(self, controller: HomeostasisController) -> None:
        assert controller.is_stable(999.0, "nonexistent") is True


class TestCorrectionHistory:
    def test_log_correction_stores_record(self, controller: HomeostasisController) -> None:
        controller.log_correction("soil_moisture", 30.0, 5.0)
        assert len(controller.correction_history) == 1

    def test_correction_history_is_bounded(self, controller: HomeostasisController) -> None:
        for i in range(150):
            controller.log_correction("p", float(i), 0.0)
        assert len(controller.correction_history) <= 100
