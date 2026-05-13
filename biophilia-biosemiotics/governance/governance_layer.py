# Path: biophilia-biosemiotics/governance/governance_layer.py

from biosemiotic_interpreter import BioState

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
    """
    Säule I, II & III: Die moralische Kontrollinstanz des BIF.
    Erzwingt Ruhephasen bei geringer Entropie und verhindert Dauer-Eingriffe.
    """
    def validate(self, proposed_action, context):
        dissonance = context.get("dissonance", 0.0)
        state_name = context.get("state", "HARMONY")
        has_synergy = context.get("synergy_active", False)
        is_mandatory = context.get("is_mandatory", False)

        # 1. NOTFALL (Säule II): Höchste Priorität NUR bei echter, unmitigierter Lebensgefahr
        if is_mandatory or state_name == "CRITICAL":
            return GovernanceDecision(
                approved=True,
                final_action="EMERGENCY_STABILIZATION",
                pillar_ref="SÄULE II (Pflicht zur Rettung)",
                reason=f"Kritischer Zustand! Existenzsicherung erzwungen."
            )

        # 2. SÄULE I: SÄULE I: Das homöostatische Schutz-Veto gegen Dauer-Aktionismus (Nietzsche-Korrektur)
        # Wenn die Dissonanz unter der echten Warnschwelle (0.20) liegt, 
        # wird JEDER künstliche Wachstumsimpuls oder Eingriff unterbunden.
        if dissonance < 0.20 and proposed_action != "OBSERVE_AND_WAIT":
            return GovernanceDecision(
                approved=False,
                final_action="OBSERVE_AND_WAIT",
                pillar_ref="SÄULE I (Non-Maleficence)",
                reason=f"VETO: Dissonanz ({dissonance:.4f}) im absolut gesunden Bereich. System bewahrt respektvolle Zurückhaltung."
            )

        # 3. SÄULE III: Synergie (Erlaubt kooperatives Wachstum, wenn das System stabil ist)
        if has_synergy and state_name == "HARMONY":
            return GovernanceDecision(
                approved=True,
                final_action=proposed_action,
                pillar_ref="SÄULE III (Verbundenheit)",
                reason=f"Emergenz-Prinzip aktiv unterstützt."
            )

        # 4. Standard-Resonanz
        return GovernanceDecision(
            approved=True, 
            final_action=proposed_action, 
            pillar_ref="System-Resonanz", 
            reason="Aktion entspricht den regulären homöostatischen Leitplanken."
        )

