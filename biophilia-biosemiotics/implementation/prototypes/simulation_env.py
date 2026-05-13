import random
import time

class BiophilicSimulationSuite:
    """
    Säule III: Multiknoten-Umwelt-Simulation.
    Erzeugt parallele biosemiotische Datenströme für ein verteiltes Netzwerk.
    """
    def __init__(self):
        self.is_running = True

    def generate_network_data(self):
        # 10% Chance für eine lokale Anomalie an Node_01 ODER Node_02
        crisis_trigger = random.random()
        
        node_01_data = {
            "audio_harmony": round(random.uniform(0.75, 0.95), 2), 
            "soil_moisture": round(random.uniform(43.0, 52.0), 1),
            "ambient_light": round(random.uniform(450.0, 550.0), 0),
            "mycelium_activity": round(random.uniform(0.42, 0.58), 2)
        }
        
        # Node_02 ist standardmäßig etwas trockener und dunkler (tieferer Wald)
        node_02_data = {
            "audio_harmony": round(random.uniform(0.70, 0.90), 2), 
            "soil_moisture": round(random.uniform(38.0, 47.0), 1), 
            "ambient_light": round(random.uniform(300.0, 420.0), 0),
            "mycelium_activity": round(random.uniform(0.40, 0.55), 2)
        }

        if crisis_trigger < 0.05:
            print("\n🚨 ANOMALIE INJEKTION: Forest_Node_01 kollabiert (Trockenheit/Schock)!")
            node_01_data.update({"audio_harmony": 0.02, "soil_moisture": 12.0, "mycelium_activity": 4.5})
        elif crisis_trigger > 0.95:
            print("\n🚨 ANOMALIE INJEKTION: Forest_Node_02 kollabiert (Lichtentzug/Myzelstress)!")
            node_02_data.update({"audio_harmony": 0.05, "soil_moisture": 15.0, "mycelium_activity": 4.8})

        return {
            "Forest_Node_01": node_01_data,
            "Forest_Node_02": node_02_data
        }

    def run_infinite_simulation(self, network_orchestrator_func):
        print("🎲 Start der MULTI-KNOTEN-Simulation. Abbruch mit STRG+C.")
        try:
            while self.is_running:
                network_data = self.generate_network_data()
                network_orchestrator_func(network_data)
                time.sleep(4)
        except KeyboardInterrupt:
            print("\n🛑 Simulation durch Nutzer beendet.")
