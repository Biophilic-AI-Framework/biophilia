# Path: biophilia-biosemiotics/governance/synergy_logic.py

class SynergyLogic:
    """
    Säule III: Demokratisierung des Wissens & Organische Bindung.
    Sucht nach Mustern der Kohärenz (1 + 1 = 3), um Emergenz zu fördern.
    """

    def __init__(self):
        # Die 'Golden Zones' definieren den Bereich, in dem Leben optimal schwingt
        self.golden_zones = {
            "audio_harmony": (0.8, 1.0),
            "soil_moisture": (40.0, 55.0),
            "ambient_light": (300.0, 700.0),
            "mycelium_activity": (0.4, 0.6),
            "air_quality_co2": (380.0, 420.0)
        }

    def _calculate_coherence(self, val1, range1, val2, range2):
        """Berechnet, wie synchron zwei Werte in ihren Zielbereichen liegen."""
        # Normierung der Werte auf 0.0 - 1.0 innerhalb ihrer Golden Zones
        norm1 = (val1 - range1[0]) / (range1[1] - range1[0]) if (range1[1]-range1[0]) != 0 else 0
        norm2 = (val2 - range2[0]) / (range2[1] - range2[0]) if (range2[1]-range2[0]) != 0 else 0
        
        # Kohärenz ist hoch, wenn beide Werte nah beieinander und im Zielbereich liegen
        if 0 <= norm1 <= 1 and 0 <= norm2 <= 1:
            return 1.0 - abs(norm1 - norm2) # 1.0 = Perfekte Kopplung
        return 0.0

    def analyze_synergies(self, sensor_data):
        active_synergies = []
        
        audio = sensor_data.get("audio_harmony", 0)
        light = sensor_data.get("ambient_light", 0)
        moisture = sensor_data.get("soil_moisture", 0)
        mycelium = sensor_data.get("mycelium_activity", 0)

        # --- 1. BIOSEMIOTISCHE KOPPLUNG (Säule III: Organische Bindung) ---
        # Neu: Kopplung von Audio (Vögel) und Myzel (Boden)
        # Wenn die 'Stimme des Waldes' mit dem 'Gedächtnis des Bodens' schwingt
        forest_coupling = self._calculate_coherence(
            audio, self.golden_zones["audio_harmony"],
            mycelium, self.golden_zones["mycelium_activity"]
        )

        if forest_coupling > 0.7:
            active_synergies.append({
                "pattern": "Biosemiotic Coupling",
                "action": "Amplify symbiotic information flow",
                "impact": f"Resonance Efficiency: {forest_coupling:.2f}",
                "recommendation": "Interspecies communication high. Knowledge sharing active."
            })

        # --- 2. GEMMAS MEDITATIVE LOGIK (Seele) ---
        if (audio >= self.golden_zones["audio_harmony"][0] and 
            self.golden_zones["ambient_light"][0] <= light <= self.golden_zones["ambient_light"][1]):
            
            active_synergies.append({
                "pattern": "Meditative Synergy",
                "action": "Optimize metabolic frequency",
                "impact": "Energy Reserve Increase",
                "recommendation": "High resonance detected. Transitioning to efficient monitoring."
            })

        # --- 3. RHIZOMATISCHES GLEICHGEWICHT (Physis) ---
        if (self.golden_zones["soil_moisture"][0] <= moisture <= self.golden_zones["soil_moisture"][1] and 
            self.golden_zones["mycelium_activity"][0] <= mycelium <= self.golden_zones["mycelium_activity"][1]):
            
            active_synergies.append({
                "pattern": "Rhizomatic Equilibrium",
                "action": "Prioritize nutrient flow",
                "impact": "Biomass Emergence",
                "recommendation": "Optimal root-mycelium coupling detected."
            })

        return active_synergies

    def get_synergy_recommendations(self, sensor_data):
        results = self.analyze_synergies(sensor_data)
        recommendations = []
        for res in results:
            recommendations.append({
                "pattern": res["pattern"],
                "action": res.get("action", "N/A"),
                "impact": res.get("impact", "N/A"),
                "recommendation": res.get("recommendation", "No specific detail provided.")
            })
        return recommendations
