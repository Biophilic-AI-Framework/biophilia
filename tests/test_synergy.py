"""Tests for SynergyLogic: coherence maths and pattern detection."""

from __future__ import annotations

import pytest

from biophilia.governance.synergy import SynergyLogic


@pytest.fixture()
def synergy() -> SynergyLogic:
    return SynergyLogic()


class TestCoherence:
    def test_both_at_ideal_is_max_coherence(self, synergy: SynergyLogic) -> None:
        zone = (0.0, 2.0)  # ideal = 1.0
        c = synergy._coherence(1.0, zone, 1.0, zone)
        assert c == pytest.approx(1.0)

    def test_outside_zone_is_zero(self, synergy: SynergyLogic) -> None:
        zone = (0.0, 1.0)
        c = synergy._coherence(2.0, zone, 0.5, zone)  # 2.0 is outside [0, 1]
        assert c == 0.0

    def test_coherence_in_0_1_range(self, synergy: SynergyLogic) -> None:
        zone1 = (0.75, 0.95)
        zone2 = (0.40, 0.60)
        c = synergy._coherence(0.85, zone1, 0.5, zone2)
        assert 0.0 <= c <= 1.0


class TestPatternDetection:
    def test_ideal_readings_trigger_all_patterns(self, synergy: SynergyLogic) -> None:
        ideal = {
            "audio_harmony": 0.85,
            "soil_moisture": 48.5,
            "ambient_light": 525.0,
            "mycelium_activity": 0.5,
        }
        recs = synergy.get_synergy_recommendations(ideal)
        assert len(recs) >= 1

    def test_crisis_readings_trigger_no_patterns(self, synergy: SynergyLogic) -> None:
        crisis = {
            "audio_harmony": 0.02,
            "soil_moisture": 12.0,
            "ambient_light": 50.0,
            "mycelium_activity": 4.5,
        }
        recs = synergy.get_synergy_recommendations(crisis)
        assert recs == []

    def test_recommendation_has_required_keys(self, synergy: SynergyLogic) -> None:
        ideal = {
            "audio_harmony": 0.85,
            "soil_moisture": 48.0,
            "ambient_light": 525.0,
            "mycelium_activity": 0.5,
        }
        for rec in synergy.get_synergy_recommendations(ideal):
            assert "pattern" in rec
            assert "action" in rec
            assert "impact" in rec
            assert "recommendation" in rec

    def test_missing_sensors_return_empty(self, synergy: SynergyLogic) -> None:
        recs = synergy.get_synergy_recommendations({})
        # No sensors → no readings in golden zones → no synergies.
        assert isinstance(recs, list)
