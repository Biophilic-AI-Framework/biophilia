# Path: biophilia-biosemiotics/governance/governance_layer.py

class GovernanceDecision:
    def __init__(self, approved, final_action, pillar_ref, reason):
        self.approved = approved
        self.final_action = final_action
        self.pillar_ref = pillar_ref  # Verweis auf Säule I, II oder III
        self.reason = reason

    def __repr__(self):
        status = "✅ APPROVED" if self.approved else "🛑 VETO"
        return f"{status} | {self.pillar_ref}: {self.reason} -> Action: {self.final_action}"

class GovernanceLayer:
    """
    Die Seele des BIF: Bindet technische Steuerung an die drei ethischen Säulen.
    """

    def validate(self, proposed_action, context):
        dissonance = context.get("dissonance", 0.0)
        has_synergy = context.get("synergy_active", False)
        
        # --- SÄULE I: SCHUTZ DES LEBENS (Non-maleficence) ---
        # Schutz vor Übersteuerung: "Behandle Leben so, dass es ohne Unheil bleibt"
        if dissonance < 0.15 and proposed_action != "OBSERVE_AND_WAIT":
            return GovernanceDecision(
                approved=False, 
                final_action="OBSERVE_AND_WAIT",
                pillar_ref="SÄULE I (Integrität)",
                reason="Eingriff abgelehnt: Die Ganzheit ist nicht verletzt. Stille ist Schutz."
            )

        # --- SÄULE II: VERANTWORTUNG DER AUTORITÄT (Service) ---
        # "Autorität verhält sich zu Verantwortung wie Recht zu Pflicht"
        intensity = self.modulate_response(dissonance, 1.0)
        
        # Pflicht zur Intervention bei Gefahr (Upgrade)
        if intensity > 0.7 and proposed_action == "GENTLE_SUPPORT":
            return GovernanceDecision(
                approved=True,
                final_action="EMERGENCY_STABILIZATION",
                pillar_ref="SÄULE II (Verantwortung)",
                reason="Pflicht zur Rettung: Autorität muss die Schwächsten bei kritischer Dissonanz schützen."
            )
        
        # Gradualismus als Schutz vor Machtmissbrauch (Downgrade)
        if intensity < 0.3 and proposed_action == "EMERGENCY_STABILIZATION":
            return GovernanceDecision(
                approved=True,
                final_action="GENTLE_SUPPORT",
                pillar_ref="SÄULE II (Verantwortung)",
                reason="Verhältnismäßigkeit: Autorität wahrt Integrität durch sanftes statt hartes Eingreifen."
            )

        # --- SÄULE III: DEMOKRATISIERUNG DES WISSENS (Openness) ---
        # "In organischen Bindungen verwurzelt"
        if has_synergy:
            return GovernanceDecision(
                approved=True,
                final_action=proposed_action,
                pillar_ref="SÄULE III (Verbundenheit)",
                reason="Synergie erkannt: Aktion fördert das Wissen und die organische Bindung im System."
            )

        # Standard-Fall: Resonanz
        return GovernanceDecision(
            approved=True, 
            final_action=proposed_action,
            pillar_ref="System-Resonanz",
            reason="Aktion im Einklang mit biophilen Parametern."
        )

    @staticmethod
    def modulate_response(entropy_score, current_stability):
        """Berechnet die ethische Intensität (Gradualismus)."""
        base_intensity = entropy_score * current_stability
        return round(min(base_intensity, 1.0), 2)
