import sys
import os

# Pfad-Brücke: Ermöglicht den Zugriff auf die Detektoren in ../implementation/prototypes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../implementation/prototypes')))

try:
    from entropy_detector import BiophilicEntropyDetector
    from entropy_response import BiophilicResponse
except ImportError:
    print("Fehler: Detektor-Module in ../implementation/prototypes nicht gefunden.")
    sys.exit(1)

def run_biophilic_loop(current_sensor_data):
    """
    Orchestriert den biosemiotischen Zyklus: 
    Wahrnehmung -> Dissonanz-Messung -> Reaktion.
    """
    # 1. Initialisierung mit der Baseline-DNA
    baseline_path = os.path.join(os.path.dirname(__file__), "biophilic_baseline.json")
    detector = BiophilicEntropyDetector(baseline_path)
    responder = BiophilicResponse()

    # 2. Berechnung der Dissonanz (Gemma's Entropie-Logik)
    dissonance = detector.calculate_dissonance(current_sensor_data)
    status = detector.get_status(dissonance)
    
    # 3. Ableitung und Ausführung der Reaktion
    action = responder.resolve(status, dissonance, current_sensor_data)
    
    print(f"--- Biophilic Cycle Status ---")
    print(f"Aktuelle Dissonanz: {dissonance:.4f} ({status})")
    print(f"Eingeleitete Maßnahme: {action}")
    print(f"------------------------------")

if __name__ == "__main__":
    # TEST-SZENARIO: Abweichung simulieren (z.B. Myzel-Stress oder Trockenheit)
    mock_data = {
        "soil_moisture": 30.0,      # Ideal: 45.0
        "ambient_light": 580.0,     # Ideal: 600.0
        "mycelium_activity": 0.8,   # Ideal: 0.5 (Stress-Zeichen)
        "air_quality_co2": 410.0    # Ideal: 400.0
    }
    
    run_biophilic_loop(mock_data)

