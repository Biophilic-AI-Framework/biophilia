"""Tests for BiosemioticInterpreter: signal classification and state synthesis."""

from __future__ import annotations

import pytest
from dataclasses import FrozenInstanceError

from biophilia.biosemiotics.interpreter import BioSignal, BioState, BiosemioticInterpreter


@pytest.fixture()
def interp() -> BiosemioticInterpreter:
    return BiosemioticInterpreter()


class TestMyceliumInterpretation:
    def test_high_voltage_below_drop_is_critical_deficit(
        self, interp: BiosemioticInterpreter
    ) -> None:
        sig = interp.interpret_mycelium(0.1, 0.5)
        assert sig.token == BioState.CRITICAL
        assert sig.source == "Mycelium_Deficit"
        assert 0.0 < sig.intensity <= 1.0

    def test_zero_voltage_is_maximum_intensity(self, interp: BiosemioticInterpreter) -> None:
        sig = interp.interpret_mycelium(0.0, 0.5)
        assert sig.intensity == pytest.approx(1.0)

    def test_overload_voltage_is_critical(self, interp: BiosemioticInterpreter) -> None:
        sig = interp.interpret_mycelium(8.5, 0.5)
        assert sig.token == BioState.CRITICAL
        assert sig.source == "Mycelium_Overload"
        assert sig.intensity > 0.8  # large excess → high intensity

    def test_harmony_range_is_harmony(self, interp: BiosemioticInterpreter) -> None:
        sig = interp.interpret_mycelium(0.5, 0.5)
        assert sig.token == BioState.HARMONY

    def test_low_voltage_in_transition_is_dormant(self, interp: BiosemioticInterpreter) -> None:
        sig = interp.interpret_mycelium(0.3, 0.5)
        assert sig.token == BioState.DORMANT

    def test_signal_is_frozen_dataclass(self, interp: BiosemioticInterpreter) -> None:
        sig = interp.interpret_mycelium(0.5, 0.5)
        with pytest.raises(FrozenInstanceError):
            sig.intensity = 0.99  # type: ignore[misc]  # frozen dataclass


class TestAcousticsInterpretation:
    def test_absolute_silence_is_critical(self, interp: BiosemioticInterpreter) -> None:
        sig = interp.interpret_acoustics(30, 0.0)
        assert sig.token == BioState.CRITICAL
        assert sig.source == "Acoustics_Vigilance"

    def test_high_variance_is_stress(self, interp: BiosemioticInterpreter) -> None:
        sig = interp.interpret_acoustics(30, 0.9)
        assert sig.token == BioState.STRESS

    def test_moderate_variance_is_harmony(self, interp: BiosemioticInterpreter) -> None:
        sig = interp.interpret_acoustics(30, 0.3)
        assert sig.token == BioState.HARMONY


class TestStateSynthesis:
    def test_any_critical_wins(self, interp: BiosemioticInterpreter) -> None:
        signals = [
            BioSignal(BioState.HARMONY, 0.9, "X"),
            BioSignal(BioState.CRITICAL, 0.8, "Y"),
        ]
        assert interp.synthesize_state(signals) == BioState.CRITICAL

    def test_stress_beats_harmony(self, interp: BiosemioticInterpreter) -> None:
        signals = [
            BioSignal(BioState.HARMONY, 0.9, "X"),
            BioSignal(BioState.STRESS, 0.5, "Y"),
        ]
        assert interp.synthesize_state(signals) == BioState.STRESS

    def test_all_harmony_returns_harmony(self, interp: BiosemioticInterpreter) -> None:
        signals = [
            BioSignal(BioState.HARMONY, 0.9, "A"),
            BioSignal(BioState.HARMONY, 0.8, "B"),
        ]
        assert interp.synthesize_state(signals) == BioState.HARMONY
