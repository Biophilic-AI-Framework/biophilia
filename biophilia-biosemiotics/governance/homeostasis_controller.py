import time
import logging
import collections

class HomeostasisController:
    """
    Der HomeostasisController ist verantwortlich für die Systemstabilität.
    Er verhindert Oszillationen (das 'Thermostat-Problem') und führt 
    Forest_Node_01 sanft in den Zustand der biophilic_baseline zurück.
    """
    """
    Zone C: Bewahrt die Stabilität. 
    Verhindert Oszillation durch Dämpfung und Trend-Analyse.
    """
    def __init__(self, thresholds, history_depth=10):
        self.warning_threshold = thresholds.get('dissonance_warning', 0.2)
        self.history = collections.deque(maxlen=history_depth)

    def analyze_trend(self, current_dissonance):
        """
        Der Wächter gegen Rauschen. 
        Gibt True zurück, wenn die Dissonanz stabil über dem Limit liegt.
        """
        self.history.append(current_dissonance)
        
        if len(self.history) < 3:
            return False # Nicht genug Daten für eine Trend-Aussage
            
        # Berechne gleitenden Durchschnitt
        avg = sum(self.history) / len(self.history)
        
        # Ein Trend gilt als stabil, wenn der Durchschnitt die Warnschwelle reißt
        return avg >= self.warning_threshold
    
    def __init__(self, baseline_data):
        self.baseline = baseline_data
        self.history = []  # Speichert letzte Korrekturen zur Vermeidung von Oversteer
        self.damping_factor = 0.7  # Biologischer Dämpfungsfaktor (0.1 = sehr langsam, 1.0 = schnell)
        logging.info("HomeostasisController initialisiert. Ziel: Integrität von Forest_Node_01.")

    def _apply_damping(self, delta, parameter_name):
        """
        Implementiert eine einfache biophile Dämpfung.
        Verhindert, dass das System 'übersteuert'.
        """
        # Hier könnte eine PID-Logik implementiert werden, aber für BIF nutzen wir 
        # eine 'sanfte Annäherung' (Asymptotisches Verhalten).
        return delta * self.damping_factor

    def _log_state(self, param, value, correction):
        # Speichert den Zustand für die integrity_chronicle.py
        self.history.append({
            'timestamp': time.time(),
            'parameter': param,
            'value': value,
            'correction': correction
        })
        # Begrenzung des Gedächtnisses
        if len(self.history) > 100:
            self.history.pop(0)

    def is_stable(self, current_value, parameter_name, threshold=0.05):
        """
        Prüft, ob das System wieder in der 'Ruhephase' der Baseline angekommen ist.
        """
        target_value = self.baseline.get(parameter_name, {}).get('optimal', 0)
        deviation = abs(target_value - current_value) / target_value if target_value != 0 else 0
        return deviation <= threshold
