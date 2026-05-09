class BiophilicResponse:
    """
    Säule II: Transformiert erkannte Dissonanz in verantwortungsvolles Handeln.
    Vermeidet binäre Reaktionen zugunsten einer homeostatischen Regulation.
    """

    @staticmethod
    def resolve(status, dissonance, sensor_data):
        """
        Leitet basierend auf dem Dissonanz-Grad und den betroffenen 
        Sensoren die angemessene biophile Antwort ein.
        """
        
        if status == "HARMONY":
            return {
                "level": "RESONANCE",
                "action": "Maintain steady state.",
                "description": f"System in biologischer Harmonie (Dissonanz: {dissonance:.4f})."
            }
        
        if status == "WARNING_DISSONANCE":
            # Spezifische Reaktion auf den primären Stressor (Beispiel: Feuchtigkeit)
            primary_stressor = max(sensor_data, key=lambda k: sensor_data[k])
            return {
                "level": "SOFT_CORRECTION",
                "action": f"Initiate gradual support for '{primary_stressor}'.",
                "description": f"Leichte Dissonanz ({dissonance:.2f}). System strebt zurück zum Gleichgewicht."
            }
        
        if status == "CRITICAL_DISSONANCE":
            # Kritische Störung erfordert lückenlose Durchdringung (Säule I)
            return {
                "level": "STABILIZATION",
                "action": "ACTIVE_INTERVENTION_REQUIRED",
                "description": f"Kritische biologische Dissonanz ({dissonance:.2f})! Integrität des Lebens gefährdet."
            }
        
        return {"level": "UNKNOWN", "action": "Re-evaluate sensors.", "description": "Status nicht definierbar."}
