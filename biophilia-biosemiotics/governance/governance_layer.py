# Path: biophilia-biosemiotics/governance/governance_layer.py

class GovernanceDecision:
    def __init__(self, approved, final_action, pillar_ref, reason):
        self.approved = approved
        self.final_action = final_action
        self.pillar_ref = pillar_ref
        self.reason = reason

    def __repr__(self):
        status = "✅ APPROVED" if self.approved else "🛑 VETO"
        return f"{status} | {self.pillar_ref}: {self.reason} -> Action: {self.final_action}"

class GovernanceLayer:
    def validate(self, proposed_action, context):
        dissonance = context.get("dissonance", 0.0)
        state = context.get("state", "UNKNOWN")
        has_synergy = context.get("synergy_active", False)

        # 1. DYNAMISCHE VETO-SCHWELLE (Säule I)
        threshold_map = {
            "HARMONY": 0.20,
            "STRESS": 0.12,
            "CRITICAL": 0.05
        }
        # Standard-Schwelle 0.15, falls State unbekannt
        dynamic_threshold = threshold_map.get(state, 0.15)

        # --- SÄULE I: SCHUTZ DER INTEGRITÄT ---
        if dissonance < dynamic_threshold and proposed_action != "OBSERVE_AND_WAIT":
            return GovernanceDecision(
                approved=False, 
                final_action="OBSERVE_AND_WAIT",
                pillar_ref="SÄULE I (Integrität)",
                reason=f"Veto: Ganzheit gewahrt. Schwelle für {state} ({dynamic_threshold}) unterschritten."
            )

        # 2. AUTOMATISCHE INTENSIVIERUNG --- SÄULE II: VERANTWORTUNG ---
        # Wenn der Zustand kritisch ist oder die Dissonanz hoch, erzwingen wir SÄULE II
        intensity = self.modulate_response(dissonance, 1.0)
        
        if (intensity > 0.7 or state == "CRITICAL") and proposed_action != "EMERGENCY_STABILIZATION":
            return GovernanceDecision(
                approved=True,
                final_action="EMERGENCY_STABILIZATION",
                pillar_ref="SÄULE II (Pflicht zur Rettung)",
                reason=f"Intensivierung: {state}-Zustand mit Dissonanz {dissonance:.2f} erfordert proaktive Existenzsicherung."
            )

        # --- SÄULE III: OFFENHEIT/SYNERGIE ---
        if has_synergy:
            return GovernanceDecision(
                approved=True,
                final_action=proposed_action,
                pillar_ref="SÄULE III (Verbundenheit)",
                reason=f"Synergie-Resonanz im Zustand {state} aktiv unterstützt."
            )

        # Standard-Resonanz (Falls keine Säule spezifisch triggert)
        return GovernanceDecision(
            approved=True, 
            final_action=proposed_action, 
            pillar_ref="System-Resonanz", 
            reason="Im Einklang mit biophilen Parametern."
        )

    @staticmethod
    def modulate_response(entropy_score, current_stability):
        return round(min(entropy_score * current_stability, 1.0), 2)
