# Path: biophilia-biosemiotics/governance/synergy_logic.py

class SynergyLogic:
    """
    Säule III: Demokratisierung des Wissens & Organische Bindung.
    Sucht nach Mustern der Kohärenz (1 + 1 = 3), um Emergenz zu fördern.
    Verhindert mathematische Starre durch ein fließendes Toleranz-Modell.
    """

    def __init__(self):
        # Die 'Golden Zones' definieren den Bereich, in dem Leben optimal schwingt
        # Leicht erweitert, damit die Simulation diese Zonen stabil durchschreitet
        self.golden_zones = {
            "audio_harmony": (0.75, 0.95),
            "soil_moisture": (42.0, 55.0),
            "ambient_light": (400.0, 650.0),
            "mycelium_activity": (0.40, 0.60),
            "air_quality_co2": (380.0, 420.0)
        }

    def _calculate_coherence(self, val1, range1, val2, range2):
        """
        Berechnet, wie synchron zwei Werte in ihren Komfortzonen schwingen.
        Nutzt die relative Nähe zum biologischen Ideal (Mittelpunkt).
        """
        # Bestimme die biologischen Mittelpunkte (Ideale)
        ideal1 = (range1[0] + range1[1]) / 2.0
        ideal2 = (range2[0] + range2[1]) / 2.0
        
        # Maximale Spannweite zur Normierung
        span1 = (range1[1] - range1[0]) / 2.0
        span2 = (range2[1] - range2[0]) / 2.0

        # Berechne die relative Abweichung vom Ideal (0.0 = Perfekt am Ideal)
        dev1 = abs(val1 - ideal1) / (span1 + 1e-9)
        dev2 = abs(val2 - ideal2) / (span2 + 1e-9)

        # Wenn beide Werte innerhalb ihrer Komfortzone liegen (Abweichung <= 1.0)
        if dev1 <= 1.0 and dev2 <= 1.0:
            # Reiner Synergie-Effekt: Kohärenz ist maximal, wenn beide nah am Ideal sind
            return round(1.0 - (abs(dev1 - dev2) * 0.5), 2)
        
        return 0.0

    def analyze_synergies(self, sensor_data):
        active_synergies = []
        
        audio = sensor_data.get("audio_harmony", 0.85)
        light = sensor_data.get("ambient_light", 500.0)
        moisture = sensor_data.get("soil_moisture", 45.0)
        mycelium = sensor_data.get("mycelium_activity", 0.5)

        # --- 1. BIOSEMIOTISCHE KOPPLUNG (Säule III: Organische Bindung) ---
        # Kopplung von Audio (Vögel/Waldklang) und Myzel (Boden/Gedächtnis)
        forest_coupling = self._calculate_coherence(
            audio, self.golden_zones["audio_harmony"],
            mycelium, self.golden_zones["mycelium_activity"]
        )

        # Ab 0.65 Kohärenz erkennen wir das Muster der Verbundenheit an
        if forest_coupling > 0.65:
            active_synergies.append({
                "pattern": "Biosemiotic Coupling",
                "action": "Amplify symbiotic information flow",
                "impact": f"Resonance Efficiency: {forest_coupling:.2f}",
                "recommendation": "Interspecies communication high. Knowledge sharing active (1+1=3)."
            })

        # --- 2. GEMMAS MEDITATIVE LOGIK (Seele / Energie-Harmonie) ---
        # Kopplung von Licht und Waldgesang
        light_audio_coupling = self._calculate_coherence(
            audio, self.golden_zones["audio_harmony"],
            light, self.golden_zones["ambient_light"]
        )
        
        if light_audio_coupling > 0.70:
            active_synergies.append({
                "pattern": "Meditative Synergy",
                "action": "Optimize metabolic frequency",
                "impact": f"Energy Reserve Gain: +{(light_audio_coupling * 10):.1f}%",
                "recommendation": "High resonance between light and audio. Transitioning to efficient monitoring."
            })

        # --- 3. RHIZOMATISCHES GLEICHGEWICHT (Physis / Fundament) ---
        # Wenn Feuchtigkeit und Myzel perfekt ineinandergreifen
        rhizome_coupling = self._calculate_coherence(
            moisture, self.golden_zones["soil_moisture"],
            mycelium, self.golden_zones["mycelium_activity"]
        )
        
        if rhizome_coupling > 0.70:
            active_synergies.append({
                "pattern": "Rhizomatic Equilibrium",
                "action": "Prioritize nutrient flow",
                "impact": f"Biomass Emergence Index: {rhizome_coupling:.2f}",
                "recommendation": "Optimal root-mycelium coupling detected. Physical integrity solid."
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
