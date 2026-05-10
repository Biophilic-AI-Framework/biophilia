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
    from biophilic_logger import BiophilicLogger
    from impact_audit import BiophilicAuditError # NEU: Für die ethische Bremse
    from action_interface import BiophilicActionInterface # NEU: Die Hände des BIF
except ImportError as e:
    print(f"❌ BIF-Strukturfehler: Ein Modul wurde nicht gefunden. Details: {e}")
    sys.exit(1)

def run_biophilic_loop(current_sensor_data):
    """
    Säule II: Das Zentralnervensystem des BIF (Forest_Node_01).
    Verwebt Wahrnehmung, Governance, ethisches Handeln und Gedächtnis.
    """
    baseline_path = os.path.join(os.path.dirname(__file__), "biophilic_baseline.json")
    
    # 1. Initialisierung der biophilen Organe
    detector = BiophilicEntropyDetector(baseline_path)
    responder = BiophilicResponse()
    controller = HomeostasisController(detector.thresholds)
    synergy = SynergyLogic()
    chronicle = IntegrityChronicle(filename="biophilic_integrity_history.json")
    pulse_logger = BiophilicLogger()
    actions = BiophilicActionInterface() # Das physische Interface

    print(f"\n--- 🌿 BIF INTEGRITY CYCLE | {time.strftime('%H:%M:%S')} ---")

    # 2. Zone A & B: Sensing & Interpretation
    pulse_logger.log_pulse("Zone A", "Sensing Pulse", current_sensor_data)
    dissonance = detector.calculate_dissonance(current_sensor_data)
    status = detector.get_status(dissonance)
    pulse_logger.log_pulse("Zone B", f"Dissonanz analysiert: {dissonance:.4f} ({status})")
    
    # 3. Zone C: Governance (Homeostase & Synergie)
    is_stable_threat = controller.analyze_trend(dissonance)
    active_synergies = synergy.analyze_synergies(current_sensor_data)

    # 4. Entscheidung & Ethische Exekutive
    if is_stable_threat or status == "CRITICAL_DISSONANCE":
        response = responder.resolve(status, dissonance, current_sensor_data)
        
        try:
            # Versuch der physischen Tat (Echtzeit-Audit durch Decorator im Interface)
            if "soil_moisture" in response['description'].lower():
                # Synergie-Score wird hier dynamisch aus der Synergie-Engine gespeist (Default 4.0)
                actions.trigger_irrigation(duration_seconds=300, maleficence=0.0, synergy=4.0)
            
            if status == "CRITICAL_DISSONANCE" and current_sensor_data.get("audio_harmony") == 0:
                actions.lock_system_port(port=8080, maleficence=0.0, synergy=5.0)

            # Erfolg dokumentieren
            pulse_logger.log_pulse("Zone C", f"INTERVENTION: {response['action']}")
            chronicle.record_action(response['level'], "Säule I & II", response['description'], dissonance)

        except BiophilicAuditError as e:
            # Veto-Fall: Die ethische Bremse hat gegriffen
            actions.handle_veto(response['level'], str(e))
            pulse_logger.log_pulse("Zone C", f"VETO: {e}")
            print(f"🛑 ETHIK-VETO: {e}")

    elif active_synergies:
        for s in active_synergies:
            synergy_msg = f"{s['pattern']}: {s['action']}"
            print(f"✨ {synergy_msg}")
            pulse_logger.log_pulse("Zone C", f"SYNERGY-BOOST: {s['pattern']}")
            chronicle.record_action(s['pattern'], "Säule III", synergy_msg, 3.0)
    else:
        pulse_logger.log_pulse("Zone C", "Passive Homöostase stabil.")
        print(f"INFO: System in Resonanz ({dissonance:.4f}).")
    
    print("------------------------------------------\n")

if __name__ == "__main__":
    # TEST-SZENARIO: Kritische Stille (Vigilanz-Test)
    run_biophilic_loop({
        "audio_harmony": 0.0,      # Alarm: Stille
        "soil_moisture": 45.0,
        "ambient_light": 600.0,
        "mycelium_activity": 0.5
    })
