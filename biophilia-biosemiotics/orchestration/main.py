import sys
import os
import time

# --- BIF ARCHITEKTUR-BRÜCKE ---
# Sicherstellen, dass die main.py (in orchestration/) ihre Werkzeuge findet
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(BASE_PATH, 'implementation/prototypes'))
sys.path.append(os.path.join(BASE_PATH, 'governance'))

try:
    from entropy_detector import BiophilicEntropyDetector
    from entropy_response import BiophilicResponse
    from homeostasis_controller import HomeostasisController
    from synergy_logic import SynergyLogic
except ImportError as e:
    print(f"❌ BIF-Strukturfehler: Module nicht gefunden. Details: {e}")
    sys.exit(1)

def run_biophilic_loop(current_sensor_data):
    """
    Zentralnervensystem des BIF (Forest_Node_01).
    Verwebt Wahrnehmung (Zone B) mit Governance (Zone C).
    """
    baseline_path = os.path.join(os.path.dirname(__file__), "biophilic_baseline.json")
    
    # 1. Initialisierung der Intelligenz-Layer
    detector = BiophilicEntropyDetector(baseline_path)
    responder = BiophilicResponse()
    # Der Controller nutzt die Schwellenwerte aus der Baseline-Konfiguration
    controller = HomeostasisController(detector.thresholds)

    print(f"\n--- 🌿 BIF INTEGRITY CYCLE | {time.strftime('%H:%M:%S')} ---")

    # 2. Zone B: Dissonanz-Messung (Fühlen)
    dissonance = detector.calculate_dissonance(current_sensor_data)
    status = detector.get_status(dissonance)
    
    # 3. Zone C: Homeostatische Filterung (Dämpfung von Rauschen)
    is_stable_threat = controller.analyze_trend(dissonance)
    
    # 4. Entscheidung & Nuancierung
    # Wir reagieren nur bei stabilem Trend oder kritischem Alarm
    if is_stable_threat or status == "CRITICAL_DISSONANCE":
        response_packet = responder.resolve(status, dissonance, current_sensor_data)
        print(f"STATUS: {status} | AKTION: {response_packet['action']}")
        print(f"GRUND:  {response_packet['description']}")
    else:
        print(f"INFO: Dissonanz ({dissonance:.4f}) erkannt. Homeostase-Dämpfung aktiv.")
    
    print("------------------------------------------\n")

if __name__ == "__main__":
    # TEST-SZENARIO: Kritische Stille (Vigilanz-Test)
    # Simuliert den Moment, in dem die Vögel verstummen
    run_biophilic_loop({
        "audio_harmony": 0.0,      # Alarm: Stille (Gewicht 5.0)
        "soil_moisture": 45.0,
        "ambient_light": 600.0,
        "mycelium_activity": 0.5
    })
