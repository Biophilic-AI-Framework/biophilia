import sys
import os
import time

# --- BIF ARCHITEKTUR-BRÜCKE ---
BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(BASE_PATH, 'implementation/prototypes'))
sys.path.append(os.path.join(BASE_PATH, 'governance'))

try:
    from entropy_detector import BiophilicEntropyDetector
    from entropy_response import BiophilicResponse
    from homeostasis_controller import HomeostasisController
    from synergy_logic import SynergyLogic
    from integrity_chronicle import IntegrityChronicle
    from biophilic_logger import BiophilicLogger # NEU: Der Puls-Wächter
except ImportError as e:
    print(f"❌ BIF-Strukturfehler: Ein Modul wurde nicht gefunden. Details: {e}")
    sys.exit(1)

def run_biophilic_loop(current_sensor_data):
    """
    Zentralnervensystem des BIF (Forest_Node_01).
    Verwebt Wahrnehmung (Zone A/B), Governance & Gedächtnis (Zone C).
    """
    baseline_path = os.path.join(os.path.dirname(__file__), "biophilic_baseline.json")
    
    # 1. Initialisierung der biophilen Organe
    detector = BiophilicEntropyDetector(baseline_path)
    responder = BiophilicResponse()
    controller = HomeostasisController(detector.thresholds)
    synergy = SynergyLogic()
    chronicle = IntegrityChronicle(filename="biophilic_integrity_history.json")
    pulse_logger = BiophilicLogger() # NEU: Initialisierung des Loggers

    print(f"\n--- 🌿 BIF INTEGRITY CYCLE | {time.strftime('%H:%M:%S')} ---")

    # 2. Zone A: Sensing (Puls aufzeichnen)
    pulse_logger.log_pulse("Zone A", "Sensing Pulse", current_sensor_data)

    # 3. Zone B: Interpretation der Dissonanz
    dissonance = detector.calculate_dissonance(current_sensor_data)
    status = detector.get_status(dissonance)
    pulse_logger.log_pulse("Zone B", f"Dissonanz analysiert: {dissonance:.4f} ({status})")
    
    # 4. Zone C: Governance (Homeostase & Synergie)
    is_stable_threat = controller.analyze_trend(dissonance)
    active_synergies = synergy.analyze_synergies(current_sensor_data)

    # 5. Entscheidung & Dokumentation
    if is_stable_threat or status == "CRITICAL_DISSONANCE":
        response = responder.resolve(status, dissonance, current_sensor_data)
        
        # Protokollierung in Log UND Chronik
        pulse_logger.log_pulse("Zone C", f"INTERVENTION: {response['action']}")
        chronicle.record_action(
            action_name=response['level'],
            pillar="Säule I & II",
            reason=response['description'],
            synergy_score=dissonance
        )
    elif active_synergies:
        for s in active_synergies:
            pulse_logger.log_pulse("Zone C", f"SYNERGY-BOOST: {s['pattern']}")
            chronicle.record_action(
                action_name=s['pattern'],
                pillar="Säule III",
                reason=s['recommendation'],
                synergy_score=3.0
            )
    else:
        pulse_logger.log_pulse("Zone C", "Homeostase stabil.")
        print(f"INFO: System in Resonanz ({dissonance:.4f}).")
    
    print("------------------------------------------\n")

if __name__ == "__main__":
    # TEST: Das perfekte Synergie-Fenster (Vogelgezwitscher, Licht & Myzel im Einklang)
    run_biophilic_loop({
        "audio_harmony": 0.85,
        "soil_moisture": 50.0,
        "ambient_light": 650.0,
        "mycelium_activity": 0.5
    })
