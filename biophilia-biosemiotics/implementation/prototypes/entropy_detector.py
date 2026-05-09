import json

class BiophilicEntropyDetector:
    """
    Bewahrt die ursprüngliche Präzision und semantische Tiefe.
    Identifiziert Dissonanz als Abweichung von der biophilen Harmonie.
    """
    def __init__(self, baseline_path):
        with open(baseline_path, 'r') as f:
            self.config = json.load(f)
        # Wir greifen auf die strukturierte Baseline zu
        self.baseline = self.config['baseline']
        self.thresholds = self.config['thresholds']

    def calculate_dissonance(self, current_sensors):
        """
        Berechnet die gewichtete Dissonanz.
        Ein Wert von 0 bedeutet perfekte Resonanz.
        """
        total_deviation = 0.0
        total_weight = 0.0

        for sensor, value in current_sensors.items():
            if sensor in self.baseline:
                ideal = self.baseline[sensor]['ideal']
                weight = self.baseline[sensor]['weight']
                
                # PRÄZISION: Schutz gegen Division durch Null (Ideal = 0)
                # Beibehaltung der relativen prozentualen Abweichung
                deviation = abs(value - ideal) / (ideal + 1e-9)
                total_deviation += deviation * weight
                total_weight += weight

        # WICHTIG: Rückgabe der durchschnittlichen gewichteten Abweichung
        # Sonst explodiert der Score bei vielen Sensoren.
        return total_deviation / total_weight if total_weight > 0 else 0.0

    def get_status(self, dissonance):
        if dissonance >= self.thresholds['dissonance_critical']:
            return "CRITICAL_DISSONANCE"
        elif dissonance >= self.thresholds['dissonance_warning']:
            return "WARNING_DISSONANCE"
        return "HARMONY"
