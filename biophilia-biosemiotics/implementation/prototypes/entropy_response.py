class BiophilicResponse:
    """
    Säule II: Transformiert erkannte Dissonanz in kontextgerechtes Handeln.
    Verpflichtet die Autorität zur gewichteten, lückenlosen Durchdringung.
    """
    def __init__(self, detector_ref=None):
        self.detector = detector_ref

    def resolve(self, status, dissonance, sensor_data):
        status_mapping = {
            "CRITICAL_DISSONANCE": "CRITICAL",
            "WARNING_DISSONANCE": "STRESS",
            "HARMONY": "HARMONY"
        }
        normalized_status = status_mapping.get(status, "UNKNOWN")
        
        if normalized_status == "HARMONY":
            return {
                "level": "RESONANCE",
                "action": "Maintain steady state.",
                "description": f"System in biologischer Harmonie (Dissonanz: {dissonance:.4f})."
            }
        
        if normalized_status == "STRESS":
            # SÄULE II: Ermittle den Stressor gewichtet und unter Beachtung des Atemfensters
            primary_stressor = "unknown"
            max_weighted_dev = -1.0
            
            if self.detector and hasattr(self.detector, 'baseline'):
                for sensor, val in sensor_data.items():
                    if sensor in self.detector.baseline:
                        ideal = self.detector.baseline[sensor]['ideal']
                        weight = self.detector.baseline[sensor]['weight']
                        
                        # Relative Roh-Abweichung
                        raw_dev = abs(val - ideal) / (ideal + 1e-9)
                        
                        # Abgleich mit der 12% Deadzone aus dem EntropyDetector
                        actual_dev = max(0.0, raw_dev - 0.12)
                        
                        # SÄULE II: Die gewichtete Abweichung bestimmt die Priorität der Rettung
                        weighted_dev = actual_dev * weight
                        
                        if weighted_dev > max_weighted_dev:
                            max_weighted_dev = weighted_dev
                            primary_stressor = sensor
            else:
                # Modifizierter Fallback: Sucht bei fehlendem Detektor den Sensor mit dem kleinsten 
                # (oft kritischsten) oder extremsten Wert relativ zu typischen Sensor-Keys
                primary_stressor = max(sensor_data, key=lambda k: sensor_data[k])

            return {
                "level": "SOFT_CORRECTION",
                "action": f"Initiate gradual support for '{primary_stressor}'.",
                "description": f"Leichte gewichtete Dissonanz ({dissonance:.2f}) bei '{primary_stressor}'. System strebt zurück zum Gleichgewicht."
            }
        
        if normalized_status == "CRITICAL":
            return {
                "level": "STABILIZATION",
                "action": "EMERGENCY_STABILIZATION",
                "description": f"Kritische biologische Dissonanz ({dissonance:.2f})! Integrität des Lebens gefährdet.",
                "is_mandatory": True
            }
        
        return {"level": "UNKNOWN", "action": "Re-evaluate sensors.", "description": "Status nicht definierbar."}
