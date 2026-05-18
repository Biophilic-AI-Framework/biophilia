"""
controller.py – Bio-state to action mapping (Säule II).

Translates a BioState + dissonance score into an action key string, then
provides human-readable descriptions for those keys.  The controller never
performs I/O itself; execution is delegated to BiophilicActionInterface.
"""

from __future__ import annotations

import logging

from biophilia.biosemiotics.interpreter import BiosemioticInterpreter, BioState

logger = logging.getLogger(__name__)

_ACTION_DESCRIPTIONS: dict[str, str] = {
    "EMERGENCY_STABILIZATION": "Existential safeguard (maximum protection mode)",
    "GENTLE_SUPPORT": "Regenerative support (healing phase)",
    "ENHANCE_VITALITY": "Synergetic unfolding (growth mode)",
    "OBSERVE_AND_WAIT": "Respectful restraint (observation only)",
}

# Threshold above which dissonance alone forces emergency action,
# regardless of the biosemiotic state label.
_EMERGENCY_ENTROPY_THRESHOLD = 0.3


class BiophilicHomeostasisController:
    """
    Determines the appropriate action based on system state and dissonance.

    The decision hierarchy (Pillar I & II):
      1. High dissonance score  → EMERGENCY_STABILIZATION (entropy beats labels)
      2. CRITICAL bio-state     → EMERGENCY_STABILIZATION
      3. STRESS bio-state       → GENTLE_SUPPORT
      4. HARMONY bio-state      → ENHANCE_VITALITY
      5. RECOVERY bio-state     → GENTLE_SUPPORT
      6. DORMANT / unknown      → OBSERVE_AND_WAIT (respectful restraint)
    """

    def __init__(self, interpreter: BiosemioticInterpreter) -> None:
        self.interpreter = interpreter

    def determine_action(self, bio_state: BioState, dissonance_score: float = 0.0) -> str:
        """Return the most appropriate action key for the given state."""
        if dissonance_score > _EMERGENCY_ENTROPY_THRESHOLD:
            logger.warning(
                "Critical entropy score %.2f — forcing EMERGENCY_STABILIZATION.",
                dissonance_score,
            )
            return "EMERGENCY_STABILIZATION"

        match bio_state:
            case BioState.CRITICAL:
                return "EMERGENCY_STABILIZATION"
            case BioState.STRESS:
                return "GENTLE_SUPPORT"
            case BioState.HARMONY:
                return "ENHANCE_VITALITY"
            case BioState.RECOVERY:
                return "GENTLE_SUPPORT"
            case _:  # DORMANT or any future state
                return "OBSERVE_AND_WAIT"

    def apply_action(self, action_key: str) -> str:
        """Log the execution intent and return the human-readable description."""
        description = _ACTION_DESCRIPTIONS.get(action_key, f"Unknown action: {action_key}")
        logger.info("BIF-EXEC %s: %s", action_key, description)
        return description
