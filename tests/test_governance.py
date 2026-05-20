"""Tests for GovernanceLayer decision logic (Säulen I–III)."""

from __future__ import annotations

import pytest

from biophilia.governance.layer import GovernanceDecision, GovernanceLayer


@pytest.fixture()
def gov() -> GovernanceLayer:
    return GovernanceLayer()


class TestEmergencyOverride:
    """Pillar II: life-critical situations must always force stabilisation."""

    def test_is_mandatory_forces_emergency(self, gov: GovernanceLayer) -> None:
        ctx = {"dissonance": 0.1, "state": "HARMONY", "is_mandatory": True, "synergy_active": False}
        d = gov.validate("OBSERVE_AND_WAIT", ctx)
        assert d.approved is True
        assert d.final_action == "EMERGENCY_STABILIZATION"
        assert "PILLAR II" in d.pillar_ref

    def test_critical_state_forces_emergency(self, gov: GovernanceLayer) -> None:
        ctx = {
            "dissonance": 0.9,
            "state": "CRITICAL",
            "is_mandatory": False,
            "synergy_active": False,
        }
        d = gov.validate("GENTLE_SUPPORT", ctx)
        assert d.approved is True
        assert d.final_action == "EMERGENCY_STABILIZATION"


class TestDynamicVeto:
    """Pillar I: actionism below the dynamic dissonance threshold must be denied."""

    def test_veto_in_harmony_below_threshold(self, gov: GovernanceLayer) -> None:
        ctx = {
            "dissonance": 0.05,
            "state": "HARMONY",
            "is_mandatory": False,
            "synergy_active": False,
        }
        d = gov.validate("GENTLE_SUPPORT", ctx)
        assert d.approved is False
        assert d.final_action == "OBSERVE_AND_WAIT"
        assert "PILLAR I" in d.pillar_ref

    def test_observe_and_wait_not_vetoed(self, gov: GovernanceLayer) -> None:
        """OBSERVE_AND_WAIT is never a harmful action; it must pass the veto check."""
        ctx = {
            "dissonance": 0.01,
            "state": "HARMONY",
            "is_mandatory": False,
            "synergy_active": False,
        }
        d = gov.validate("OBSERVE_AND_WAIT", ctx)
        assert d.approved is True

    def test_stress_state_has_higher_threshold(self, gov: GovernanceLayer) -> None:
        # HARMONY threshold = 0.20; STRESS threshold = 0.35.
        # When dissonance is low, action is vetoed in both states.
        # When dissonance is moderate (0.20–0.35), it's OK in HARMONY but still vetoed in STRESS.
        ctx_harmony_moderate = {
            "dissonance": 0.25,
            "state": "HARMONY",
            "is_mandatory": False,
            "synergy_active": False,
        }
        ctx_stress_moderate = {
            "dissonance": 0.25,
            "state": "STRESS",
            "is_mandatory": False,
            "synergy_active": False,
        }
        ctx_stress_high = {
            "dissonance": 0.40,
            "state": "STRESS",
            "is_mandatory": False,
            "synergy_active": False,
        }

        # At 0.25: approved in HARMONY (0.25 >= 0.20), vetoed in STRESS (0.25 < 0.35).
        assert gov.validate("GENTLE_SUPPORT", ctx_harmony_moderate).approved is True
        assert gov.validate("GENTLE_SUPPORT", ctx_stress_moderate).approved is False
        # At 0.40: approved in both.
        assert gov.validate("GENTLE_SUPPORT", ctx_stress_high).approved is True


class TestSynergyEndorsement:
    """Pillar III: synergy patterns in HARMONY earn explicit endorsement."""

    def test_synergy_approved_in_harmony(self, gov: GovernanceLayer) -> None:
        ctx = {
            "dissonance": 0.30,  # above HARMONY threshold (0.20)
            "state": "HARMONY",
            "synergy_active": True,
            "is_mandatory": False,
        }
        d = gov.validate("ENHANCE_VITALITY", ctx)
        assert d.approved is True
        assert "PILLAR III" in d.pillar_ref

    def test_synergy_irrelevant_in_stress(self, gov: GovernanceLayer) -> None:
        ctx = {
            "dissonance": 0.40,  # above STRESS threshold (0.35)
            "state": "STRESS",
            "synergy_active": True,
            "is_mandatory": False,
        }
        d = gov.validate("GENTLE_SUPPORT", ctx)
        # Falls through to standard resonance (not PILLAR III).
        assert d.approved is True
        assert "III" not in d.pillar_ref


class TestGovernanceDecision:
    def test_string_representation_approved(self) -> None:
        d = GovernanceDecision(True, "ENHANCE_VITALITY", "P III", "emergent synergy")
        assert "APPROVED" in str(d)

    def test_string_representation_veto(self) -> None:
        d = GovernanceDecision(False, "OBSERVE_AND_WAIT", "P I", "actionism denied")
        assert "VETO" in str(d)
