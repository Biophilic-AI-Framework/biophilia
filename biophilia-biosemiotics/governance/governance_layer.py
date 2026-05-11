class GovernanceLayer:
    """
    Säule II: Reguliert die Intensität der Reaktion (Gradualismus).
    Stellt sicher, dass das System homeostatisch bleibt.
    """
    
    @staticmethod
    def modulate_response(entropy_score, current_stability):
        # Layer 4: Nuancierung
        # Wenn die Stabilität gering ist, reagiere vorsichtiger, um nicht zu übersteuern
        base_intensity = entropy_score * current_stability
        
        # Layer 3: Homeostatische Bremse
        if base_intensity > 0.8:
            return 0.8 # Niemals 100% Schock-Reaktion
        return round(base_intensity, 2)

    @staticmethod
    def validate_alignment(action_type, pillar_target):
        # Layer 1: Core-Alignment
        # Prüft, ob die geplante Aktion (z.B. Pumpe) das Ziel (Säule I) stützt
        valid_pairs = [("PUMP", "SERVICE"), ("PORT_LOCK", "PROTECTION")]
        return any(a == action_type and p == pillar_target for a, p in valid_pairs)

class NuanceModulator:
    @staticmethod
    def calculate_response_magnitude(bio_state):
        """
        Vermeidet binäre Reaktionen. 
        Ein leichter Stress (0.2) führt zu einer sanften Korrektur.
        Ein kritischer Zustand (0.9) führt zu einer maximalen Intervention.
        """
        if bio_state.state == "STABLE":
            return 0.0
        
        # Sanfte Steigerungskurve (z.B. quadratisch), um Übersteuerung zu vermeiden
        magnitude = (bio_state.intensity ** 2) 
        return round(magnitude, 2)
