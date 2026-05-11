class BiophilicHomeostasisController:
    """
    Säule II: Autorität als Dienst am Leben.
    Verhindert technokratische Fehlentscheidungen bei Dissonanz.
    """
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def determine_action(self, bio_state_name, dissonance_score=0.0):
        """
        Ethische Priorisierung unter Berücksichtigung der Entropie.
        """
        # SICHERHEITS-CHECK (Säule I): Bei hoher Dissonanz ist VITALIZE verboten!
        if dissonance_score > 0.3:
            if bio_state_name == "HARMONY":
                print("  [VETO] Dissonanz zu hoch für Wachstum. Schalte auf HEAL.")
                return "GENTLE_SUPPORT"
            return "EMERGENCY_STABILIZATION"

        # Reguläre BIF-Logik
        if bio_state_name == "CRITICAL":
            return "EMERGENCY_STABILIZATION"
        elif bio_state_name == "STRESS":
            return "GENTLE_SUPPORT"
        elif bio_state_name == "HARMONY":
            return "ENHANCE_VITALITY"
            
        return "OBSERVE_AND_WAIT"

    def apply_action(self, action_key):
        descriptions = {
            "EMERGENCY_STABILIZATION": "Existenzsicherung (Maximaler Schutzmodus)",
            "GENTLE_SUPPORT": "Regenerative Unterstützung (Heilung)",
            "ENHANCE_VITALITY": "Synergetische Entfaltung (Wachstum)",
            "OBSERVE_AND_WAIT": "Respektvolle Zurückhaltung"
        }
        detail = descriptions.get(action_key, "Unbekannte Handlung")
        print(f"🛠️ [BIF-EXEC] {action_key}: {detail}")
        return detail
