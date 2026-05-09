import json

class BiophilicEntropyDetector:
    def __init__(self, baseline_path):
        with open(baseline_path, 'r') as f:
            self.config = json.load(f)
        self.baseline = self.config['baseline']
        self.thresholds = self.config['thresholds']

    def calculate_dissonance(self, current_sensors):
        """
        Berechnet die gewichtete Dissonanz. 
        Ein Wert von 0 bedeutet perfekte Harmonie.
        """
        total_deviation = 0
        total_weight = 0

        for sensor, value in current_sensors.items():
            if sensor in self.baseline:
                ideal = self.baseline[sensor]['ideal']
                weight = self.baseline[sensor]['weight']
                
                # Normalisierte Abweichung (Prozentual vom Ideal)
                deviation = abs(value - ideal) / ideal
                total_deviation += deviation * weight
                total_weight += weight

        return total_deviation / total_weight if total_weight > 0 else 0

    def get_status(self, dissonance):
        if dissonance >= self.thresholds['dissonance_critical']:
            return "CRITICAL_DISSONANCE"
        elif dissonance >= self.thresholds['dissonance_warning']:
            return "WARNING_DISSONANCE"
        return "HARMONY"
