class SynergyLogic:
    """
    Säule III: Das Prinzip der Emergenz (1 + 1 = 3).
    Sucht nach Mustern der Harmonie, um von 'Stabil' zu 'Exzellent' zu gelangen.
    Fokus: Metabolische Effizienz und Wachstums-Optimierung.
    """

    def __init__(self):
        # Definition der "Golden Zones" basierend auf der Forest_Node_01 Baseline
        self.golden_zones = {
            "audio_harmony": (0.8, 1.0),
            "soil_moisture": (40.0, 55.0),
            "ambient_light": (300.0, 700.0),
            "mycelium_activity": (0.4, 0.6),
            "air_quality_co2": (380.0, 420.0)
        }
        
        # Definition von Synergie-Paaren (aus deinem Ur-Entwurf)
        self.synergy_patterns = {
            "photosynthesis_boost": {
                "factors": ["ambient_light", "air_quality_co2", "soil_moisture"],
                "threshold": 0.7,
                "effect": "increase_growth_rate"
            },
            "rhizomatic_optimum": {
                "factors": ["soil_moisture", "mycelium_activity"],
                "threshold": 0.8,
                "effect": "optimize_nutrient_flow"
            }
        }

    def analyze_synergies(self, sensor_data):
        """
        Analysiert die Semiosphäre auf positive Korrelationen.
        Kombiniert die strukturelle Analyse mit Gemmas 'Meditative'-Logik.
        """
        active_synergies = []

        # --- 1. GEMMAS MEDITATIVE LOGIK (Seele) ---
        # Hohe Audio-Harmonie + stabiles Licht
        audio = sensor_data.get("audio_harmony", 0)
        light = sensor_data.get("ambient_light", 0)
        
        if (audio >= self.golden_zones["audio_harmony"][0] and 
            self.golden_zones["ambient_light"][0] <= light <= self.golden_zones["ambient_light"][1]):
            
            active_synergies.append({
                "pattern": "Meditative Synergy",
                "action": "Optimize metabolic frequency",
                "impact": "Energy Reserve Increase",
                "recommendation": "High resonance detected. Transitioning to efficient monitoring."
            })

        # --- 2. DEINE STRUKTURELLE ANALYSE (Physis) ---
        # Prüft das Rhizomatische Gleichgewicht
        moisture = sensor_data.get("soil_moisture", 0)
        mycelium = sensor_data.get("mycelium_activity", 0)

        if (self.golden_zones["soil_moisture"][0] <= moisture <= self.golden_zones["soil_moisture"][1] and 
            self.golden_zones["mycelium_activity"][0] <= mycelium <= self.golden_zones["mycelium_activity"][1]):
            
            active_synergies.append({
                "pattern": "Rhizomatic Equilibrium",
                "action": "Prioritize nutrient flow",
                "impact": "Biomass Emergence",
                "recommendation": "Optimal root-mycelium coupling detected."
            })

        # --- 3. ALLGEMEINE MUSTER-ERKENNUNG (Zukunftssicherheit) ---
        # Hier könnten weitere komplexe Verknüpfungen aus self.synergy_patterns folgen
        
        return active_synergies

    def get_synergy_recommendations(self, sensor_data):
        """
        Schnittstelle für die main.py zur Extraktion handlungsorientierter Daten.
        """
        results = self.analyze_synergies(sensor_data)
        
        # Sicherstellung des Formats für die IntegrityChronicle
        recommendations = []
        for res in results:
            recommendations.append({
                "pattern": res["pattern"],
                "action": res.get("action", "N/A"),
                "impact": res.get("impact", "N/A"),
                "recommendation": res.get("recommendation", "No specific detail provided.")
            })
        return recommendations
