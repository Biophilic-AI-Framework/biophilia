import json

class BiophilicEntropyDetector:
    def __init__(self, baseline_path):
        with open(baseline_path, 'r') as f:
            self.config = json.load(f)
        
        # SÄULE I: Akzeptiert die neue Netzwerk-Matrix schadenfrei
        # Falls die alte Struktur geladen wird, greift ein sicherer Fallback
        if 'nodes' in self.config:
            self.nodes_matrix = self.config['nodes']
        else:
            # Abwärtskompatibilität, falls die flache JSON genutzt wird
            self.nodes_matrix = {
                "Forest_Node_01": {
                    "baseline": self.config.get('baseline', {}),
                    "thresholds": self.config.get('thresholds', {})
                }
            }
        self.last_calculated_dissonance = 0.0


    def calculate_dissonance(self, node_name, current_sensors):
        """Berechnet die Dissonanz spezifisch für den jeweiligen Knoten."""
        # Hole die spezifische Baseline des Knotens, falls nicht vorhanden Fallback auf Node_01
        node_config = self.nodes_matrix.get(node_name, self.nodes_matrix["Forest_Node_01"])
        baseline = node_config['baseline']
        
        total_deviation = 0.0
        total_weight = 0.0
        max_single_deviation = 0.0

        for sensor, value in current_sensors.items():
            if sensor in baseline:
                ideal = baseline[sensor]['ideal']
                weight = baseline[sensor]['weight']
                
                raw_deviation = abs(value - ideal) / (ideal + 1e-9)
                
                if raw_deviation <= 0.05:
                    deviation = 0.0
                else:
                    deviation = raw_deviation - 0.05
                
                weighted_deviation = deviation * weight
                total_deviation += weighted_deviation
                total_weight += weight
                
                if weighted_deviation > max_single_deviation:
                    max_single_deviation = weighted_deviation

        avg_dissonance = total_deviation / total_weight if total_weight > 0 else 0.0
        
        if max_single_deviation > 0.25:
            final_dissonance = max(avg_dissonance, max_single_deviation * 0.8)
        else:
            final_dissonance = avg_dissonance
        
        self.last_calculated_dissonance = round(final_dissonance, 4)
        return self.last_calculated_dissonance

    def get_status(self, node_name, dissonance):
        node_config = self.nodes_matrix.get(node_name, self.nodes_matrix["Forest_Node_01"])
        thresholds = node_config['thresholds']
        
        if dissonance >= thresholds['dissonance_critical']:
            return "CRITICAL_DISSONANCE"
        elif dissonance >= thresholds['dissonance_warning']:
            return "WARNING_DISSONANCE"
        return "HARMONY"
