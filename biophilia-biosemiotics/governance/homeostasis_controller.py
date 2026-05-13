import time
import logging
import collections

class HomeostasisController:
    """
    Zone C: Bewahrt die Stabilität von Forest_Node_01.
    Verhindert Oszillaton durch kombinierte Trend- und Dämpfungs-Analyse.
    Führt biologische Parameter asymptotisch in die Komfortzone zurück.
    """
    def __init__(self, thresholds, baseline_data, history_depth=10):
        # Fusionierte Attribute: Verhindert den Überschreib-Kollaps
        self.warning_threshold = thresholds.get('dissonance_warning', 0.2)
        self.baseline = baseline_data
        
        # Typsichere Historie für die Dissonanz-Entwicklung
        self.dissonance_history = collections.deque(maxlen=history_depth)
        
        # Protokoll-Historie für System-Korrekturen
        self.correction_history = []  
        self.damping_factor = 0.7  

        logging.info("🌿 HomeostasisController erfolgreich biophil initialisiert.")

    def analyze_trend(self, current_dissonance):
        """
        Der Wächter gegen Rauschen und plötzliche Schocks.
        Nutzt Max-Validierung, um akute Bedrohungen nicht wegzuglätten.
        """
        self.dissonance_history.append(current_dissonance)
        
        if len(self.dissonance_history) < 3:
            return False 
            
        # SÄULE I: Ein akuter Ausschlag darf niemals weggemittelt werden!
        # Wenn der aktuelle Wert die Schwelle massiv reißt, schlagen wir sofort Alarm
        if current_dissonance >= (self.warning_threshold * 1.5):
            return True

        avg = sum(self.dissonance_history) / len(self.dissonance_history)
        return avg >= self.warning_threshold
    
    def apply_damping(self, delta, parameter_name=None):
        """
        Asymptotische Annäherung an den Zielzustand. Preventiert Oversteer.
        """
        return delta * self.damping_factor

    def log_correction(self, param, value, correction):
        """Säule III: Erzeugt lückenlose Nachvollziehbarkeit."""
        self.correction_history.append({
            'timestamp': time.time(),
            'parameter': param,
            'value': value,
            'correction': correction
        })
        if len(self.correction_history) > 100:
            self.correction_history.pop(0)

    def is_stable(self, current_value, parameter_name, threshold=0.05):
        """Prüft die Rückkehr in die homöostatische Ruhephase."""
        target_value = self.baseline.get(parameter_name, {}).get('ideal', 0)
        if target_value == 0:
            return True
        deviation = abs(target_value - current_value) / target_value
        return deviation <= threshold
