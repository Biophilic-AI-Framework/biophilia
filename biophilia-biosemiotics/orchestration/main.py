import sys
import os
import time

# Pfad-Brücke: Verbindet den Orchestrator mit den stabilen Prototypen
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../implementation/prototypes')))

try:
    from entropy_detector import BiophilicEntropyDetector
    from entropy_response import BiophilicResponse
except ImportError as e:
    print(f"❌ Architektur-Fehler: Module in ../implementation/prototypes nicht gefunden: {e}")
    sys.exit(1)

def run_biophilic_loop(current_sensor_data):
    """
    Säule II: Orchestriert den symbiotischen Zyklus.
    Verwebt Wahrnehmung, Dissonanz-Messung und nuancierte Handlung.
    """
    # 1. Initialisierung mit dem genetischen Code (Baseline)
    baseline_path = os.path.join(os.path.dirname(__file__), "biophilic_baseline.json")
    
    detector = BiophilicEntropyDetector(baseline_path)
    responder = BiophilicResponse()

    print(f"\n--- 🌿 Biophiler Zyklus: {time.strftime('%H:%M:%S')} ---")

    # 2. Dissonanz-Messung (Fühlen statt nur Messen)
    dissonance = detector.calculate_dissonance(current_sensor_data)
    status = detector.get_status(dissonance)
    
    # 3. Nuancierte Antwort-Ermittlung (Layer 4: Gradualismus)
    response_packet = responder.resolve(status, dissonance, current_sensor_data)
    
    # 4. Ausgabe & Transparenz (Säule III)
    print(f"Status: {status} (Score: {dissonance:.4f})")
    print(f"Ebene:  {response_packet['level']}")
    print(f"Aktion: {response_packet['action']}")
    print(f"Grund:  {response_packet['description']}")
    print(f"------------------------------------------\n")

if __name__ == "__main__":
    # TEST-SZENARIO: Kritische Dissonanz durch Myzel-Stress und Trockenheit
    mock_data = {
        "soil_moisture": 25.0,      # Deutlich unter Ideal (45.0)
        "ambient_light": 580.0,     # Nah am Ideal (600.0)
        "mycelium_activity": 0.95,  # Hoher Stress (Ideal: 0.5)
        "air_quality_co2": 405.0    # Stabil (400.0)
    }
    
    run_biophilic_loop(mock_data)
