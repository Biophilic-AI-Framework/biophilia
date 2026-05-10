class SynergyLogic:
    """
    Die SynergyLogic ist die 'Thriving'-Schicht des Systems.
    Sie sucht nach positiven Korrelationen zwischen verschiedenen Sensordaten,
    um die Effizienz des Systems zu steigern, anstatt nur Fehler zu korrigieren.
    """

    def __init__(self):
        # Definition von Synergie-Paaren: Welche Faktoren verstärken sich gegenseitig?
        self.synergy_patterns = {
            "photosynthesis_boost": {
                "factors": ["light_intensity", "co2_level", "humidity"],
                "threshold": 0.7, # Erforderlicher Grad an Optimierung
                "effect": "increase_growth_rate"
            },
            "root_absorption_optimum": {
                "factors": ["soil_moisture", "temperature"],
                "threshold": 0.8,
                "effect": "optimize_nutrient_flow"
            }
        }

    def analyze_synergies(self, sensor_data):
        """
        Analysiert die aktuellen Daten auf Synergie-Potenziale.
        Gibt eine Liste von Synergie-Boosts zurück.
        """
        active_synergies = []

        # Beispiel-Logik für den 'Photosynthesis Boost'
        # In einem echten System würden hier die Normalwerte (0.0 - 1.0) geprüft werden
        if (sensor_data.get("light_intensity", 0) > 60 and 
            sensor_data.get("co2_level", 0) > 400 and 
            sensor_data.get("humidity", 0) > 50):
            
            active_synergies.append({
                "pattern": "photosynthesis_boost",
                "status": "ACTIVE",
                "recommendation": "Maintain current state - Optimal growth window detected."
            })

        # Beispiel-Logik für 'Root Absorption'
        if (sensor_data.get("soil_moisture", 0) > 30 and 
            sensor_data.get("temperature", 0) < 25):
            
            active_synergies.append({
                "pattern": "root_absorption_optimum",
                "status": "ACTIVE",
                "recommendation": "Ideal conditions for nutrient uptake."
            })

        return active_synergies

    def integrate_with_response(self, base_response, active_synergies):
        """
        Erweitert die Basis-Antwort (Homeostase) um die Synergie-Erkenntnisse.
        """
        if not active_synergies:
            return base_response

        synergy_report = "\n[Synergy Analysis]: " + \
                         " | ".join([s["recommendation"] for s in active_synergies])
        
        return base_response + synergy_report
