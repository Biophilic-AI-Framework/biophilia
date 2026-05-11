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
    from impact_audit import BiophilicAuditError
    from action_interface import BiophilicActionInterface
    from biosemiotic_interpreter import BiosemioticInterpreter, BioState
    from biophilic_controller import BiophilicHomeostasisController
except ImportError as e:
    print(f"❌ BIF-Strukturfehler: {e}")
    sys.exit(1)

def run_biophilic_loop(current_sensor_data):
    # Pfade und Organe initialisieren
    baseline_path = os.path.join(os.path.dirname(__file__), "bio_data/biophilic_baseline.json")
    detector = BiophilicEntropyDetector(baseline_path)
    responder = BiophilicResponse()
    interpreter = BiosemioticInterpreter()
    bio_controller = BiophilicHomeostasisController(interpreter)
    trend_watcher = HomeostasisController(detector.thresholds)
    synergy_engine = SynergyLogic()
    chronicle = IntegrityChronicle(filename="biophilic_integrity_history.json")
    pulse_logger = BiophilicLogger()
    actions = BiophilicActionInterface()

    print(f"\n--- 🌿 BIF INTEGRITY CYCLE | {time.strftime('%H:%M:%S')} ---")

    # 1. ZONE A & B: Wahrnehmung & Interpretation
    pulse_logger.log_pulse("Zone A", "Sensing Pulse", current_sensor_data)
    dissonance = detector.calculate_dissonance(current_sensor_data)
    status = detector.get_status(dissonance)
    
    # Semiotik
    sig_m = interpreter.interpret_mycelium(current_sensor_data.get("mycelium_activity", 0.5), 0.5)
    sig_a = interpreter.interpret_acoustics(30, current_sensor_data.get("audio_harmony", 0.8))
    holistic_state = interpreter.synthesize_state([sig_m, sig_a])
    
    pulse_logger.log_pulse("Zone B", f"Zustand: {holistic_state.value} | Dissonanz: {dissonance:.4f} ({status})")

    # 2. ZONE C: Governance & Entscheidung
    active_synergies = synergy_engine.get_synergy_recommendations(current_sensor_data)
    
    # Der entscheidende Fix: Wir übergeben die Dissonanz an den Controller
    action_key = bio_controller.determine_action(holistic_state.name, dissonance_score=dissonance)

    # 3. GOVERNANCE & EXEKUTIVE (Vereint)
    is_stable_threat = trend_watcher.analyze_trend(dissonance)
    
    # Wir entscheiden, ob wir handeln müssen
    if is_stable_threat or status == "CRITICAL_DISSONANCE" or holistic_state == BioState.CRITICAL or action_key != "OBSERVE_AND_WAIT":
        
        # Systemische & Biologische Begründung einholen
        response = responder.resolve(status, dissonance, current_sensor_data)
        
        try:
            # 4. TAT-AUSFÜHRUNG (Mit ethischer Bremse)
            action_detail = bio_controller.apply_action(action_key)
            
            # Physischer Trigger (Audit-Decorator im Interface prüft hier!)
            if action_key in ["EMERGENCY_STABILIZATION", "GENTLE_SUPPORT"]:
                actions.trigger_irrigation(duration_seconds=300, maleficence=0.0, synergy=4.5)

            # Reiche Daten für die Chronik vorbereiten
            rich_reason = {
                "biological_intent": action_detail,
                "systemic_analysis": response['description'],
                "biosemiotic_state": holistic_state.value,
                "trend_alert": is_stable_threat
            }
            
            pulse_logger.log_pulse("Zone C", f"INTERVENTION: {action_key}")
            chronicle.record_action(action_key, "Säule I & II", rich_reason, dissonance)
            print(f"⚠️ AKTION: {action_key} -> {rich_reason}")

        except BiophilicAuditError as e:
            # Deine gerettete ethische Bremse fängt den Fehler ab
            print(f"🛑 ETHIK-VETO: {e}")
            pulse_logger.log_pulse("Zone C", f"VETO: {e}")
            chronicle.record_action("VETO", "Säule I", str(e), dissonance)

    elif active_synergies:
        # Synergie-Block (Bleibt als positive Alternative)
        for s in active_synergies:
            synergy_msg = f"{s['pattern']}: {s['recommendation']}"
            pulse_logger.log_pulse("Zone C", f"SYNERGY-BOOST: {s['pattern']}")
            chronicle.record_action(s['pattern'], "Säule III", synergy_msg, 3.0)
            print(f"✨ SYNERGIE: {synergy_msg}")
            
    else:
        print(f"✅ RESONANZ: System stabil ({dissonance:.4f}).")

if __name__ == "__main__":
    # --- AUTOMATISIERTER BIF-STRESSTEST ---
    try:
        from simulation_env import BiophilicSimulationSuite
        
        print("🚀 Starte automatisierte BIF-Simulations-Suite...")
        suite = BiophilicSimulationSuite()
    
        # Der Zufall übernimmt das Steuer
        # Wir übergeben die Funktion selbst als Referenz
        suite.run_infinite_simulation(run_biophilic_loop)
            
    except ImportError:
        print("⚠️ simulation_env.py nicht gefunden. Falle zurück auf manuellen Test.")
        # Manueller Fallback-Test (Vigilanz-Alarm)
        run_biophilic_loop({
            "audio_harmony": 0.0,      
            "soil_moisture": 45.0,
            "ambient_light": 500.0,
            "mycelium_activity": 0.5
        })
