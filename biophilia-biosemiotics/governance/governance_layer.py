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
    Nimmt das dynamische Toleranz-Mapping wieder auf, um blinden Aktionismus
    situationsbedingt und unerbittlich per Veto abzufedern.
    """
    def validate(self, proposed_action, context):
        dissonance = context.get("dissonance", 0.0)
        state_name = context.get("state", "HARMONY")
        has_synergy = context.get("synergy_active", False)
        is_mandatory = context.get("is_mandatory", False)

        # =====================================================================
        # 1. DYNAMISCHE VETO-SCHWELLE (Säule I - Reaktiviert & Harmonisiert)
        # =====================================================================
        # Das Mapping definiert das exakte Dissonanz-Fenster, unterhalb dessen 
        # künstliche Eingriffe rigoros als "unüberlegt" verboten werden.
        threshold_map = {
            "HARMONY": 0.20,  # Im Frieden tolerieren wir Rauschen, verbieten aber Aktionismus
            "STRESS": 0.35,   # Unter Stress erhöht sich der Schutzraum, um Übersteuerungen zu blockieren
            "CRITICAL": 0.99  # In der absoluten Krise schlägt der Notfalldurchgriff an
        }
        dynamic_threshold = threshold_map.get(state_name, 0.20)

        # =====================================================================
        # 2. NOTFALL-DURCHGRIFF (Säule II)
        # =====================================================================
        # Höchste Priorität: Wenn das nackte Überleben auf dem Spiel steht (Event-Injektion)
        if is_mandatory or state_name == "CRITICAL":
            return GovernanceDecision(
                approved=True,
                final_action="EMERGENCY_STABILIZATION",
                pillar_ref="SÄULE II (Pflicht zur Rettung)",
                reason=f"Kritischer Zustand! Existenzsicherung absolut erzwungen."
            )

        # =====================================================================
        # 3. SÄULE I: Das dynamische homöostatische Schutz-Veto (Nietzsche-Korrektur)
        # =====================================================================
        # Wenn die aktuelle Dissonanz die dynamische Schwelle des jeweiligen Zustands 
        # UNTERSCHREITET, greift der Schutz des Lebens vor technischer Reizüberflutung.
        if dissonance < dynamic_threshold and proposed_action != "OBSERVE_AND_WAIT":
            return GovernanceDecision(
                approved=False,
                final_action="OBSERVE_AND_WAIT",
                pillar_ref="SÄULE I (Non-Maleficence)",
                reason=f"VETO: Dissonanz ({dissonance:.4f}) liegt unter der Schutzschwelle von {dynamic_threshold:.2f} für {state_name}. Eingriff verweigert."
            )

        # =====================================================================
        # 4. SÄULE III: Offenheit & Synergie-Resonanz
        # =====================================================================
        # Erlaubt kooperatives Wachstum nur, wenn das System die Veto-Hürde gemeistert hat
        if has_synergy and state_name == "HARMONY":
            return GovernanceDecision(
                approved=True,
                final_action=proposed_action,
                pillar_ref="SÄULE III (Verbundenheit)",
                reason=f"Emergenz-Prinzip (1+1=3) aktiv unterstützt."
            )

        # 5. Standard-Resonanz
        return GovernanceDecision(
            approved=True, 
            final_action=proposed_action, 
            pillar_ref="System-Resonanz", 
            reason="Aktion entspricht den regulären homöostatischen Leitplanken."
        )
