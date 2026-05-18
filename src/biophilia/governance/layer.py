"""
layer.py – Ethical governance and veto logic (Säulen I–III).

Three-stage decision pipeline:
  1. Emergency override (Pillar II) – life-critical situations bypass everything.
  2. Dynamic veto (Pillar I)        – actionism is forbidden when dissonance is
                                      below the situation-dependent threshold.
  3. Synergy endorsement (Pillar III)– cooperative patterns earn explicit approval.
  4. Standard resonance              – default approval within normal operating bounds.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Dissonance ceilings below which intervention is "actionistic" and therefore vetoed.
_THRESHOLD_MAP: dict[str, float] = {
    "HARMONY": 0.20,  # In peace, noise is tolerated; actionism is not.
    "STRESS": 0.35,  # Under stress, the protection window widens.
    "CRITICAL": 0.99,  # In absolute crisis the emergency override fires first.
}


@dataclass(frozen=True, slots=True)
class GovernanceDecision:
    """Immutable record of what the governance layer decided and why."""

    approved: bool
    final_action: str
    pillar_ref: str
    reason: str

    def __str__(self) -> str:
        status = "APPROVED ✅" if self.approved else "VETO 🛑"
        return f"{status} | {self.pillar_ref}: {self.reason} → {self.final_action}"


class GovernanceLayer:
    """
    Moral control authority of the BIF.

    Accepts a proposed action and a context dict, and returns a
    :class:`GovernanceDecision` that either approves or vetoes the action,
    always with a pillar reference and a human-readable reason.
    """

    def validate(self, proposed_action: str, context: dict) -> GovernanceDecision:  # type: ignore[type-arg]
        dissonance: float = float(context.get("dissonance", 0.0))
        state_name: str = str(context.get("state", "HARMONY"))
        has_synergy: bool = bool(context.get("synergy_active", False))
        is_mandatory: bool = bool(context.get("is_mandatory", False))

        threshold = _THRESHOLD_MAP.get(state_name, 0.20)

        # ── 1. Emergency override (Pillar II) ─────────────────────────────────
        if is_mandatory or state_name == "CRITICAL":
            logger.warning("PILLAR II: Emergency stabilisation forced (state=%s).", state_name)
            return GovernanceDecision(
                approved=True,
                final_action="EMERGENCY_STABILIZATION",
                pillar_ref="PILLAR II (Duty to Save)",
                reason="Critical state detected. Existential safeguard is absolute.",
            )

        # ── 2. Veto: actionism forbidden below dynamic threshold (Pillar I) ───
        if dissonance < threshold and proposed_action != "OBSERVE_AND_WAIT":
            logger.debug(
                "PILLAR I: Veto — dissonance %.4f < threshold %.2f for state=%s.",
                dissonance,
                threshold,
                state_name,
            )
            return GovernanceDecision(
                approved=False,
                final_action="OBSERVE_AND_WAIT",
                pillar_ref="PILLAR I (Non-Maleficence)",
                reason=(
                    f"Dissonance ({dissonance:.4f}) is below the protective threshold "
                    f"({threshold:.2f}) for state '{state_name}'. Intervention denied."
                ),
            )

        # ── 3. Synergy endorsement (Pillar III) ───────────────────────────────
        if has_synergy and state_name == "HARMONY":
            return GovernanceDecision(
                approved=True,
                final_action=proposed_action,
                pillar_ref="PILLAR III (Connectedness)",
                reason="Emergence principle (1+1=3): cooperative resonance detected.",
            )

        # ── 4. Standard approval ──────────────────────────────────────────────
        return GovernanceDecision(
            approved=True,
            final_action=proposed_action,
            pillar_ref="System Resonance",
            reason="Action aligns with regular homeostatic guidelines.",
        )
