# Import der Enum aus dem Interpreter-Modul
from biosemiotic_interpreter import BioState

class BiophilicHomeostasisController:
    """
    Säule II: Autorität als Dienst am Leben.
    Erzwingt Typsicherheit und kompromisslose Existenzsicherung.
    """
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def determine_action(self, bio_state: BioState, dissonance_score: float = 0.0) -> str:
        # ABSOLUTE EXISTENZSICHERUNG (Säule I & II): Entropie schlägt Label!
        if dissonance_score > 0.3:
            # Bei massiver Dissonanz ist kein Platz für halbe Maßnahmen oder Wachstum
            print(f"⚠️ [CRITICAL ENTROPY] Score {dissonance_score:.2f} erfordert sofortige Stabilisierung!")
            return "EMERGENCY_STABILIZATION"

        # Reguläre, typsichere Kaskade über die Enum
        if bio_state == BioState.CRITICAL:
            return "EMERGENCY_STABILIZATION"
            
        elif bio_state == BioState.STRESS:
            return "GENTLE_SUPPORT"
            
        elif bio_state == BioState.HARMONY:
            return "ENHANCE_VITALITY"
            
        elif bio_state == BioState.RECOVERY:
            return "GENTLE_SUPPORT" # Explizite Zuweisung für Erholungsphasen
            
        # Bei Dormanz oder unbekannten Zuständen: Respektvolle Zurückhaltung
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
