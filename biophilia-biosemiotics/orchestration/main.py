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

# SÄULE II & PERFORMANCE: Einmalige globale Initialisierung (Ressourcenschutz)
# =====================================================================
# --- SÄULE II: INITIATION DER BIO-ORGANISCHEN SYSTEMKOMPONENTEN ---
# =====================================================================
BASELINE_PATH = os.path.join(os.path.dirname(__file__), "bio_data/biophilic_baseline.json")

# 1. Datenbasis laden
DETECTOR = BiophilicEntropyDetector(BASELINE_PATH)

# 2. Den korrigierten Controller mit beiden Datenstrukturen füttern
# DETECTOR.thresholds liefert die Dissonanz-Schwellenwerte (z.B. für analyze_trend)
# DETECTOR.baseline liefert die biologischen Idealwerte (z.B. für is_stable)
HOMEOSTASIS_WATCHER = HomeostasisController(
    thresholds=DETECTOR.thresholds, 
    baseline_data=DETECTOR.baseline
)
# 3. Restliche Organe instanziieren
BASELINE_PATH = os.path.join(os.path.dirname(__file__), "bio_data/biophilic_baseline.json")
DETECTOR = BiophilicEntropyDetector(BASELINE_PATH)
# Wir übergeben dem Responder den Detektor, damit er Zugriff auf die Baseline-Gewichtung hat:
RESPONDER = BiophilicResponse(detector_ref=DETECTOR)
INTERPRETER = BiosemioticInterpreter()
BIO_CONTROLLER = BiophilicHomeostasisController(INTERPRETER)
# TREND_WATCHER = HomeostasisController(DETECTOR.thresholds) **ALT**
SYNERGY_ENGINE = SynergyLogic()
GOV_LAYER = GovernanceLayer()
CHRONICLE = IntegrityChronicle(filename="biophilic_integrity_history.json")
PULSE_LOGGER = BiophilicLogger()
ACTIONS = BiophilicActionInterface()

def run_biophilic_loop(current_sensor_data):
    print(f"\n--- 🌿 BIF INTEGRITY CYCLE | {time.strftime('%H:%M:%S')} ---")

    # NETZWERK-BRÜCKE: Wenn die Simulation die Daten verschachtelt liefert,
    # extrahieren wir gezielt die Biosphäre von Forest_Node_01
    if "Forest_Node_01" in current_sensor_data:
        current_sensor_data = current_sensor_data["Forest_Node_01"]

    # --- ZONE A & B: WAHRNEHMUNG & INTERPRETATION ---
    PULSE_LOGGER.log_pulse("Zone A", "Sensing Pulse", current_sensor_data)
    dissonance = DETECTOR.calculate_dissonance(current_sensor_data)
    status = DETECTOR.get_status(dissonance)

    sig_m = INTERPRETER.interpret_mycelium(current_sensor_data.get("mycelium_activity", 0.5), 0.5)
    # VORHER: sig_a = interpreter.interpret_acoustics(30, current_sensor_data.get("audio_harmony", 0.8))
    # NACHHER: Wir nutzen die Varianz direkt aus den Simulationsdaten
    audio_val = current_sensor_data.get("audio_harmony", 0.85)
    # Wir simulieren eine gesunde Varianz, die invers zur Harmonie läuft
    simulated_variance = round(1.0 - audio_val, 2) 
    sig_a = INTERPRETER.interpret_acoustics(30, simulated_variance)

    holistic_state = INTERPRETER.synthesize_state([sig_m, sig_a])
    
    PULSE_LOGGER.log_pulse("Zone B", f"Zustand: {holistic_state.value} | Dissonanz: {dissonance:.4f}")

    # --- ZONE C: VORBEREITUNG & GOVERNANCE ---
    active_synergies = SYNERGY_ENGINE.get_synergy_recommendations(current_sensor_data)
    proposed_action = BIO_CONTROLLER.determine_action(holistic_state, dissonance_score=dissonance)
    
    response = RESPONDER.resolve(status, dissonance, current_sensor_data)

    gov_context = {
        "dissonance": dissonance,
        "synergy_active": len(active_synergies) > 0,
        "state": holistic_state.name,
        "is_mandatory": response.get("is_mandatory", False)
    }

    decision = GOV_LAYER.validate(proposed_action, gov_context)

    # --- ZONE D: EXEKUTIVE & AUDIT ---
    if not decision.approved:
        # SÄULE I: Das System bricht ab, weil kein Eingriff nötig ist.
        if decision.final_action == "OBSERVE_AND_WAIT":
            print(f"✅ RESONANZ: System stabil ({dissonance:.4f}). Keine Intervention nötig.")
            
            # SÄULE III (Synergien einblenden): Wenn das System stabil ist, 
            # zeigen wir die kooperativen Schwingungen TROTZ des Veto-Stopps an!
            if active_synergies:
                for s in active_synergies:
                    print(f"✨ SÄULE III (1+1=3): {s['pattern']} aktiv -> {s['recommendation']}")
                    # Wir loggen die Synergie parallel als wertvolle Erkenntnis in die Chronik
                    CHRONICLE.record_action(s['pattern'], "Säule III", f"{s['pattern']}: {s['recommendation']}", 3.0)
            
            PULSE_LOGGER.log_pulse("Zone C", f"Resonanz gewahrt: {decision.reason}")
            CHRONICLE.record_action("RESONANCE", decision.pillar_ref, decision.reason, dissonance)
        else:
            # Echtes, blockierendes Veto gegen eine gefährliche Aktion
            print(f"🛑 HARD-VETO durch {decision.pillar_ref}: {decision.reason}")
            PULSE_LOGGER.log_pulse("Zone C", f"VETO: {decision.reason}")
            CHRONICLE.record_action("VETO", decision.pillar_ref, decision.reason, dissonance)
        return  # Zyklus respektvoll beenden

    final_action = decision.final_action
    is_stable_threat = HOMEOSTASIS_WATCHER.analyze_trend(dissonance)

    # KOSMETISCHER NETZHAUT-FIX: Zeige die treibenden Synergien auch bei genehmigtem Wachstum!
    if final_action == "ENHANCE_VITALITY" and active_synergies:
        for s in active_synergies:
            print(f"✨ EMERGENZ-TREIBER (1+1=3): {s['pattern']} erzwingt {final_action} -> {s['recommendation']}")
    
    # Handlungs-Check: Müssen wir aktiv werden? (Säule II im Krisenfall)
    if is_stable_threat or status == "CRITICAL_DISSONANCE" or holistic_state == BioState.CRITICAL or final_action != "OBSERVE_AND_WAIT":
        try:
            action_detail = BIO_CONTROLLER.apply_action(final_action)

            # Kontextsensitive Tat (Pumpe oder Isolation)
            if final_action in ["EMERGENCY_STABILIZATION", "GENTLE_SUPPORT"]:
                if any(s.source in ["Mycelium_Deficit", "Mycelium_Overload"] for s in [sig_m, sig_a]):
                    ACTIONS.trigger_irrigation(duration_seconds=120, maleficence=0.0, synergy=4.5)
                elif any(s.source == "Acoustics_Vigilance" for s in [sig_m, sig_a]):
                    ACTIONS.lock_system_port(port=8080, maleficence=0.0, synergy=5.0)

            # Dokumentation in der fälschungssicheren Chronik
            rich_reason = {
                "pillar": decision.pillar_ref,
                "moral_justification": decision.reason,
                "biological_intent": action_detail,
                "systemic_analysis": response.get('description', 'N/A'),
                "biosemiotic_state": holistic_state.value,
                "system_status": status,
                "trend_alert": is_stable_threat
            }
            
            PULSE_LOGGER.log_pulse("Zone C", f"INTERVENTION: {final_action}")
            CHRONICLE.record_action(final_action, decision.pillar_ref, rich_reason, dissonance)
            print(f"⚠️ AKTION BEENDET: {final_action} | {decision.pillar_ref}")

        except BiophilicAuditError as e:
            print(f"🛑 KRITISCHER ETHIK-STOPP: {e}")
            PULSE_LOGGER.log_pulse("Zone C", f"VETO: {e}")
            CHRONICLE.record_action("CRITICAL_VETO", "Audit-Layer", str(e), dissonance)

if __name__ == "__main__":
    # SÄULE III: Validierung der historischen Wahrheit vor Systemstart
    print("🔒 Initiiere Integritätsprüfung der biophilen Chronik...")
    init_chronicle = IntegrityChronicle(filename="biophilic_integrity_history.json")
    
    if not init_chronicle.verify_integrity():
        print("🚨 CRITICAL_SECURITY_BREACH: Die historische Chronik wurde manipuliert!")
        print("🛑 Systemstart zum Schutz der biophilen Wahrheit verweigert.")
        sys.exit(1)
        
    try:
        # Versuch, die Simulationsumgebung zu laden
        sys.path.append(os.path.join(BASE_PATH, 'implementation/prototypes'))
        from simulation_env import BiophilicSimulationSuite
        
        print("🚀 Integrität verifiziert. Starte BIF-Echtzeit-Simulation...")
        suite = BiophilicSimulationSuite()
        suite.run_infinite_simulation(run_biophilic_loop)
            
    except ImportError:
        print("⚠️ simulation_env.py nicht im Pfad. Starte manuellen Einzel-Test...")
        test_data = {
            "audio_harmony": 0.85,      
            "soil_moisture": 45.0,
            "ambient_light": 600.0,
            "mycelium_activity": 0.5
        }
        run_biophilic_loop(test_data)
