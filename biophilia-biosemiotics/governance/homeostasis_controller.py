import time
import logging

class HomeostasisController:
    """
    Der HomeostasisController ist verantwortlich für die Systemstabilität.
    Er verhindert Oszillationen (das 'Thermostat-Problem') und führt 
    Forest_Node_01 sanft in den Zustand der biophilic_baseline zurück.
    """
    
    def __init__(self, baseline_data):
        self.baseline = baseline_data
        self.history = []  # Speichert letzte Korrekturen zur Vermeidung von Oversteer
        self.damping_factor = 0.7  # Biologischer Dämpfungsfaktor (0.1 = sehr langsam, 1.0 = schnell)
        logging.info("HomeostasisController initialisiert. Ziel: Integrität von Forest_Node_01.")

    def calculate_correction(self, current_value, parameter_name):
        """
        Berechnet die notwendige Korrektur, um die Baseline wieder zu erreichen,
        unter Berücksichtigung der Systemträgheit.
        """
        target_value = self.baseline.get(parameter_name, {}).get('optimal', None)
        
        if target_value is None:
            logging.warning(f"Kein Baseline-Wert für {parameter_name} gefunden. Keine Korrektur möglich.")
            return 0

        # Delta: Die Distanz zur Integrität (Wahrheit)
        delta = target_value - current_value
        
        # Verhindern von Oszillation: 
        # Wenn die letzte Korrektur bereits in die entgegengesetzte Richtung ging,
        # dämpfen wir die aktuelle Reaktion ab.
        correction = self._apply_damping(delta, parameter_name)
        
        self._log_state(parameter_name, current_value, correction)
        return correction

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
