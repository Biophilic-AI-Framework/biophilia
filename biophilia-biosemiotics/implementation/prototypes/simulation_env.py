import random
import time

class BiophilicSimulationSuite:
    """
    Säule III: Stochastische Umwelt-Simulation mit Event-Injektion.
    Erzeugt randomisierte Daten und gezielte biosemiotische Muster.
    """
    def __init__(self):
        self.is_running = True

    def generate_random_data(self):
        # 10% Chance für ein synergetisches Krisen-Event (Test der Säule I & II)
        if random.random() < 0.10:
            return self._generate_crisis_event()
        
        # Standard: Realistisches Rauschen (Dein Original)
        return {
            "audio_harmony": round(random.uniform(0.6, 0.9), 2), # Normaler Waldgesang
            "soil_moisture": round(random.uniform(40.0, 60.0), 1),
            "ambient_light": round(random.uniform(300.0, 800.0), 0),
            "mycelium_activity": round(random.uniform(0.3, 0.7), 2)
        }

    def _generate_crisis_event(self):
        """Erzeugt ein koordiniertes Muster: Stille + Myzelstress."""
        print("🚨 EVENT INJECTED: Biosemiotische Anomalie (Synergie-Test)")
        return {
            "audio_harmony": round(random.uniform(0.0, 0.1), 2),    # Plötzliche Stille
            "soil_moisture": round(random.uniform(10.0, 25.0), 1),   # Kritische Trockenheit
            "ambient_light": round(random.uniform(50.0, 150.0), 0),  # Verdunklung
            "mycelium_activity": round(random.uniform(4.0, 5.0), 2)  # Myzel schreit (Stress)
        }

    def run_infinite_simulation(self, orchestrator_func):
        print("🎲 Start der HYBRID-Simulation (Random + Events). Abbruch mit STRG+C.")
        try:
            while self.is_running:
                data = self.generate_random_data()
                orchestrator_func(data)
                time.sleep(3) # Etwas mehr Zeit für die Analyse-Zyklen
        except KeyboardInterrupt:
            print("\n🛑 Simulation durch Nutzer beendet.")
