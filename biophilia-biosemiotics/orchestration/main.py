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
    from governance_layer import GovernanceLayer
except ImportError as e:
    print(f"❌ BIF-Strukturfehler: {e}")
    sys.exit(1)

def run_biophilic_loop(current_sensor_data):
    # 1. ORGANE INITIALISIEREN
    baseline_path = os.path.join(os.path.dirname(__file__), "bio_data/biophilic_baseline.json")
    detector = BiophilicEntropyDetector(baseline_path)
    responder = BiophilicResponse()
    interpreter = BiosemioticInterpreter()
    bio_controller = BiophilicHomeostasisController(interpreter)
    trend_watcher = HomeostasisController(detector.thresholds)
    synergy_engine = SynergyLogic()
    gov_layer = GovernanceLayer()
    chronicle = IntegrityChronicle(filename="biophilic_integrity_history.json")
    pulse_logger = BiophilicLogger()
    actions = BiophilicActionInterface()

    print(f"\n--- 🌿 BIF INTEGRITY CYCLE | {time.strftime('%H:%M:%S')} ---")

    # --- ZONE A & B: WAHRNEHMUNG & INTERPRETATION ---
    pulse_logger.log_pulse("Zone A", "Sensing Pulse", current_sensor_data)
    dissonance = detector.calculate_dissonance(current_sensor_data)
    status = detector.get_status(dissonance)
    
    # Biosemiotik: Signale interpretieren
    sig_m = interpreter.interpret_mycelium(current_sensor_data.get("mycelium_activity", 0.5), 0.5)
    sig_a = interpreter.interpret_acoustics(30, current_sensor_data.get("audio_harmony", 0.8))
    holistic_state = interpreter.synthesize_state([sig_m, sig_a])
    
    pulse_logger.log_pulse("Zone B", f"Zustand: {holistic_state.value} | Dissonanz: {dissonance:.4f}")

    # --- ZONE C: VORBEREITUNG DER ENTSCHEIDUNG ---
    # Synergien erkennen
    active_synergies = synergy_engine.get_synergy_recommendations(current_sensor_data)
    
    # Vorläufige Aktions-Wahl durch den Controller
    proposed_action = bio_controller.determine_action(holistic_state.name, dissonance_score=dissonance)

    # --- ZONE C: GOVERNANCE FILTER (Die ethische Instanz) ---
    gov_context = {
        "dissonance": dissonance,
        "synergy_active": len(active_synergies) > 0,
        "state": holistic_state.name
    }

    # Die moralische Prüfung der vorgeschlagenen Aktion
    decision = gov_layer.validate(proposed_action, gov_context)

    # --- ZONE D: EXEKUTIVE & AUDIT ---
    if not decision.approved:
        print(f"🛑 VETO durch {decision.pillar_ref}: {decision.reason}")
        pulse_logger.log_pulse("Zone C", f"VETO: {decision.reason}")
        chronicle.record_action("VETO", decision.pillar_ref, decision.reason, dissonance)
        return  # Zyklus abbrechen, Integrität wahren

    # Wenn genehmigt, nutzen wir die (evtl. modulierte) finale Aktion
    final_action = decision.final_action
    is_stable_threat = trend_watcher.analyze_trend(dissonance)
    
    # Handlungs-Check: Müssen wir aktiv werden?
    if is_stable_threat or status == "CRITICAL_DISSONANCE" or holistic_state == BioState.CRITICAL or final_action != "OBSERVE_AND_WAIT":
        
        response = responder.resolve(status, dissonance, current_sensor_data)
        
        try:
            # 4. TAT-AUSFÜHRUNG
            action_detail = bio_controller.apply_action(final_action)
            
            # Physische Schnittstelle (z.B. Bewässerung)
            if final_action in ["EMERGENCY_STABILIZATION", "GENTLE_SUPPORT"]:
                actions.trigger_irrigation(duration_seconds=300, maleficence=0.0, synergy=4.5)

            # Dokumentation in der Chronik
            rich_reason = {
                "pillar": decision.pillar_ref,
                "moral_justification": decision.reason,
                "biological_intent": action_detail,
                "systemic_analysis": response.get('description', 'N/A'),
                "biosemiotic_state": holistic_state.value,
                "trend_alert": is_stable_threat
            }
            
            pulse_logger.log_pulse("Zone C", f"INTERVENTION: {final_action}")
            chronicle.record_action(final_action, decision.pillar_ref, rich_reason, dissonance)
            print(f"⚠️ AKTION: {final_action} | {decision.pillar_ref}: {decision.reason}")

        except BiophilicAuditError as e:
            print(f"🛑 KRITISCHER ETHIK-STOPP: {e}")
            pulse_logger.log_pulse("Zone C", f"VETO: {e}")
            chronicle.record_action("CRITICAL_VETO", "Audit-Layer", str(e), dissonance)

    elif active_synergies:
        # Synergie-Pfad (Säule III: Wissensfluss & Bindung)
        for s in active_synergies:
            synergy_msg = f"{s['pattern']}: {s['recommendation']}"
            pulse_logger.log_pulse("Zone C", f"SYNERGY: {s['pattern']}")
            chronicle.record_action(s['pattern'], "Säule III", synergy_msg, 3.0)
            print(f"✨ SYNERGIE: {synergy_msg}")
            
    else:
        print(f"✅ RESONANZ: System stabil ({dissonance:.4f}). Keine Intervention nötig.")

if __name__ == "__main__":
    try:
        # Versuch, die Simulationsumgebung zu laden
        sys.path.append(os.path.join(BASE_PATH, 'implementation/prototypes'))
        from simulation_env import BiophilicSimulationSuite
        
        print("🚀 Starte BIF-Echtzeit-Simulation...")
        suite = BiophilicSimulationSuite()
        suite.run_infinite_simulation(run_biophilic_loop)
            
    except ImportError:
        print("⚠️ simulation_env.py nicht im Pfad. Starte manuellen Einzel-Test...")
        # Manueller Test-Datensatz
        test_data = {
            "audio_harmony": 0.2,      
            "soil_moisture": 35.0,
            "ambient_light": 400.0,
            "mycelium_activity": 0.3
        }
        run_biophilic_loop(test_data)
