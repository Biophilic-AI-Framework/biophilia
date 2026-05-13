import json

class BiophilicEntropyDetector:
    """
    Säule I: Bewahrt die Ganzheitlichkeit des Lebens.
    Erlaubt organisches Atmen (Toleranzkorridor) und blockiert tech-bedingte Hyperaktivität.
    """
    def __init__(self, baseline_path):
        with open(baseline_path, 'r') as f:
            self.config = json.load(f)
        self.baseline = self.config['baseline']
        self.thresholds = self.config['thresholds']
        self.last_calculated_dissonance = 0.0

    def calculate_dissonance(self, current_sensors):
        """
        Berechnet die gewichtete Dissonanz mit biologischer Totzone (Deadzone)
        und asymptotischem Maximum-Schutz bei echten Krisen.
        """
        total_deviation = 0.0
        total_weight = 0.0
        max_single_deviation = 0.0

        for sensor, value in current_sensors.items():
            if sensor in self.baseline:
                ideal = self.baseline[sensor]['ideal']
                weight = self.baseline[sensor]['weight']
                
                # Relative Abweichung berechnen
                raw_deviation = abs(value - ideal) / (ideal + 1e-9)
                
                # SÄULE I: Organischer Pufferkorridor (Deadzone)
                # Reduziert von 12% auf 5%. Kleine Schwankungen bis 5% sind Grundrauschen.
                # Alles darüber atmet fließend und wird feinfühlig erfasst.
                if raw_deviation <= 0.05:
                    deviation = 0.0
                else:
                    # Lineare Skalierung direkt ab der feinen Toleranzgrenze
                    deviation = raw_deviation - 0.05
                
                weighted_deviation = deviation * weight
                total_deviation += weighted_deviation
                total_weight += weight
                
                if weighted_deviation > max_single_deviation:
                    max_single_deviation = weighted_deviation

        # Arithmetischer Teilschnitt
        avg_dissonance = total_deviation / total_weight if total_weight > 0 else 0.0
        
        # SÄULE I: Dynamischer Schutz
        # Der Maximum-Verstärker greift erst ein, wenn eine gewichtete Einzelabweichung 
        # die Warnschwelle (0.20) signifikant überschreitet.
        if max_single_deviation > 0.25:
            final_dissonance = max(avg_dissonance, max_single_deviation * 0.8)
        else:
            final_dissonance = avg_dissonance
        
        self.last_calculated_dissonance = round(final_dissonance, 4)
        return self.last_calculated_dissonance

    def get_status(self, dissonance):
        if dissonance >= self.thresholds['dissonance_critical']:
            return "CRITICAL_DISSONANCE"
        elif dissonance >= self.thresholds['dissonance_warning']:
            return "WARNING_DISSONANCE"
        return "HARMONY"
