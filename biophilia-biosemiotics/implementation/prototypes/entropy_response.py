class BiophilicResponse:
    @staticmethod
    def resolve(status, dissonance, sensor_data):
        if status == "HARMONY":
            return "System in Balance. Maintaining steady state."
        
        if status == "WARNING_DISSONANCE":
            # Hier könnte eine sanfte Anpassung erfolgen (z.B. Bewässerung +5%)
            return f"Minor Dissonance detected ({dissonance:.2f}). Initiating soft correction."
        
        if status == "CRITICAL_DISSONANCE":
            # Hier erfolgt ein Alarm oder eine Notfallmaßnahme
            return f"CRITICAL DISSONANCE ({dissonance:.2f})! Emergency stabilization required."
