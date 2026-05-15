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
    from biosemiotic_interpreter import BiosemioticInterpreter, BioState, BioSignal
    from biophilic_controller import BiophilicHomeostasisController
    from governance_layer import GovernanceLayer
    from dashboard import BiophilicDashboard
except ImportError as e:
    print(f"❌ BIF-Strukturfehler: {e}")
    sys.exit(1)

# =====================================================================
# --- SÄULE II: INITIATION DER BIO-ORGANISCHEN SYSTEMKOMPONENTEN ---
# =====================================================================
BASELINE_PATH = os.path.join(os.path.dirname(__file__), "bio_data/biophilic_baseline.json")

# 1. Datenbasis laden
DETECTOR = BiophilicEntropyDetector(BASELINE_PATH)

# 2. Den korrigierten Controller mit beiden Datenstrukturen füttern
# DETECTOR.thresholds liefert die Dissonanz-Schwellenwerte (z.B. für analyze_trend)
# DETECTOR.baseline liefert die biologischen Idealwerte (z.B. für is_stable)
# [KORREKTUR] Extrahiere die Basisdaten für den globalen Homeostasis-Wächter
# Wir nutzen die Parameter von Forest_Node_01 als netzwerkweiten Standard-Leitfaden
standard_node_config = DETECTOR.nodes_matrix["Forest_Node_01"]

HOMEOSTASIS_WATCHER = HomeostasisController(
    thresholds=standard_node_config['thresholds'], 
    baseline_data=standard_node_config['baseline']
)

# 3. Restliche Organe einmalig global instanziieren (Ressourcenschutz)
# Wir übergeben dem Responder den Detektor, damit er Zugriff auf die Baseline-Gewichtung hat:
RESPONDER = BiophilicResponse(detector_ref=DETECTOR)
INTERPRETER = BiosemioticInterpreter()
BIO_CONTROLLER = BiophilicHomeostasisController(INTERPRETER)
SYNERGY_ENGINE = SynergyLogic()
GOV_LAYER = GovernanceLayer()
CHRONICLE = IntegrityChronicle(filename="biophilic_integrity_history.json")
PULSE_LOGGER = BiophilicLogger()
ACTIONS = BiophilicActionInterface()
DASHBOARD = BiophilicDashboard()


def process_single_node(node_name, current_sensor_data, network_context):
    """
    DEINE ORIGINAL-SCHLEIFE: Modularisiert für unendliche Skalierbarkeit.
    Verarbeitet die Biosphäre eines spezifischen Knotens mit 100% Datenintegrität.
    """
    # --- ZONE A & B: WAHRNEHMUNG & INTERPRETATION ---
    PULSE_LOGGER.log_pulse(f"{node_name}-Zone A", "Sensing Pulse", current_sensor_data)
    dissonance = DETECTOR.calculate_dissonance(node_name, current_sensor_data)
    status = DETECTOR.get_status(node_name, dissonance)


    # Biosemiotik: Signale interpretieren
    sig_m = INTERPRETER.interpret_mycelium(current_sensor_data.get("mycelium_activity", 0.5), 0.5)
    # VORHER: sig_a = interpreter.interpret_acoustics(30, current_sensor_data.get("audio_harmony", 0.8))
    # NACHHER: Wir nutzen die Varianz direkt aus den Simulationsdaten   
    audio_val = current_sensor_data.get("audio_harmony", 0.85)
    # Wir simulieren eine gesunde Varianz, die invers zur Harmonie läuft
    simulated_variance = round(1.0 - audio_val, 2) 
    sig_a = INTERPRETER.interpret_acoustics(30, simulated_variance)

    holistic_state = INTERPRETER.synthesize_state([sig_m, sig_a])

    PULSE_LOGGER.log_pulse(f"{node_name}-Zone B", f"Zustand: {holistic_state.value} | Dissonanz: {dissonance:.4f}")

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

    # WISSENS-SCHNIPSEL FÜR DAS ASCII-DASHBOARD SPEICHERN
    node_snapshot = {
        "sensors": current_sensor_data,
        "detector": {"dissonance": dissonance, "status": status},
        "interpreter": {"state_value": holistic_state.value},
        "synergies": active_synergies,
        "governance": {
            "pillar": decision.pillar_ref,
            "action": decision.final_action,
            "reason": decision.reason.replace("VETO: ", "")[:85]
        }
    }
    DASHBOARD.update_node_state(node_name, node_snapshot)

    # --- ZONE D: EXEKUTIVE & AUDIT ---
    if not decision.approved:
        # SÄULE I: Das System bricht ab, weil kein Eingriff nötig ist.
        if decision.final_action == "OBSERVE_AND_WAIT":
            # SÄULE III (Synergien einblenden): Wenn das System stabil ist, 
            # zeigen wir die kooperativen Schwingungen TROTZ des Veto-Stopps an!
            if active_synergies:
                for s in active_synergies:
                    # Wir loggen die Synergie parallel als wertvolle Erkenntnis in die Chronik
                    CHRONICLE.record_action(node_name, f"{s['pattern']}_{node_name}", "Säule III", f"{s['pattern']}: {s['recommendation']}", 3.0)
            
            PULSE_LOGGER.log_pulse(f"{node_name}-Zone C", f"Resonanz gewahrt: {decision.reason}")
            CHRONICLE.record_action(node_name, f"RESONANCE_{node_name}", decision.pillar_ref, decision.reason, dissonance)
        else:
            # Echtes, blockierendes Veto gegen eine gefährliche Aktion
            PULSE_LOGGER.log_pulse(f"{node_name}-Zone C", f"VETO: {decision.reason}")
            CHRONICLE.record_action(node_name, f"VETO_{node_name}", decision.pillar_ref, decision.reason, dissonance)
        return  # Zyklus respektvoll beenden

    final_action = decision.final_action
    is_stable_threat = HOMEOSTASIS_WATCHER.analyze_trend(dissonance)

    # Handlungs-Check: Müssen wir aktiv werden? (Säule II im Krisenfall)
    if is_stable_threat or status == "CRITICAL_DISSONANCE" or holistic_state == BioState.CRITICAL or final_action != "OBSERVE_AND_WAIT":
        try:
            action_detail = BIO_CONTROLLER.apply_action(final_action)

            # SÄULE II: INTERSPEZIFISCHE NETZWERK-SOLIDARITÄT BEI GEFAHR
            if final_action in ["EMERGENCY_STABILIZATION", "GENTLE_SUPPORT"]:
                neighbor_name = "Forest_Node_02" if node_name == "Forest_Node_01" else "Forest_Node_01"
                neighbor_data = network_context.get(neighbor_name, {})
                
                # Wir ermitteln die Dissonanz des Nachbarn für den Solidaritäts-Check
                # Wir übergeben dem Detektor sowohl den Namen des Nachbarn als auch dessen Sensordaten!
                neighbor_dissonance = DETECTOR.calculate_dissonance(neighbor_name, neighbor_data) if neighbor_data else 0.0

                if any(s.source in ["Mycelium_Deficit", "Mycelium_Overload"] for s in [sig_m, sig_a]):
                    if neighbor_dissonance < 0.20:
                        # Nachbar spendet Ressourcen
                        ACTIONS.trigger_irrigation(duration_seconds=150, maleficence=0.0, synergy=5.5)
                    else:
                        # Nachbar selbst im Stress, autarker Schutzmodus
                        ACTIONS.trigger_irrigation(duration_seconds=120, maleficence=0.0, synergy=4.5)
                elif any(s.source == "Acoustics_Vigilance" for s in [sig_m, sig_a]):
                    ACTIONS.lock_system_port(port=8080, maleficence=0.0, synergy=5.0)

            # Dokumentation in der fälschungssicheren Chronik
            rich_reason = {
                "node": node_name,
                "pillar": decision.pillar_ref,
                "moral_justification": decision.reason,
                "biological_intent": action_detail,
                "systemic_analysis": response.get('description', 'N/A'),
                "biosemiotic_state": holistic_state.value,
                "system_status": status,
                "trend_alert": is_stable_threat
            }
            
            PULSE_LOGGER.log_pulse(f"{node_name}-Zone C", f"INTERVENTION: {final_action}")
            CHRONICLE.record_action(node_name, f"{final_action}_{node_name}", decision.pillar_ref, rich_reason, dissonance)

        except BiophilicAuditError as e:
            PULSE_LOGGER.log_pulse(f"{node_name}-Zone C", f"CRITICAL_ETHIK_STOPP: {e}")
            CHRONICLE.record_action(node_name, f"CRITICAL_VETO_{node_name}", "Audit-Layer", str(e), dissonance)


def run_biophilic_loop(network_data):
    """
    SÄULE III: Der zentrale Netzwerk-Orchestrator.
    Erkennt verschachtelte Multi-Knoten-Pakete automatisch und verarbeitet
    Node_01 und Node_02 nacheinander, bevor das Dashboard gerendert wird.
    """
    # Wenn die Simulation flache Daten liefert (Abwärtskompatibilität), kapseln wir sie
    if "Forest_Node_01" not in network_data:
        network_data = {"Forest_Node_01": network_data}

    # Sequenzielle Verarbeitung beider Welten
    for node_name, sensor_data in network_data.items():
        process_single_node(node_name, sensor_data, network_data)
    
    # AM ENDE DES GESAMT-TAKTS: Das ASCII-Dashboard rendert unaufhaltsam beide Knoten parallel!
    # Wir ziehen den echten, kryptografischen Kettenschwanz aus dem Dateibuffer
    last_hash = "0" * 64
    if os.path.exists(CHRONICLE.filename):
        with open(CHRONICLE.filename, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
                if history:
                    last_hash = history[-1].get("current_hash", "0" * 64)
            except Exception:
                pass

    DASHBOARD.render(last_chronicle_hash=last_hash)


if __name__ == "__main__":
    # =====================================================================
    # SÄULE I: KOMPROMISSRECHTER SCHUTZ-CHECK (VORABSTURZ BEI KEY-MANGEL)
    # =====================================================================
    secret_key = os.getenv("BIF_SECRET_KEY")
    if not secret_key:
        print("🚨 CRITICAL_SECURITY_FAILURE: BIF_SECRET_KEY ist nicht gesetzt!")
        print("🛑 Auslands- und Schutzbetrieb zum Wohle des Lebens verweigert.")
        sys.exit(1)

    # --- AB HIER LÄUFT DEIN KRYPTOGRAFISCHER START-CHECK WEITER ---
    print("🔒 Initiiere Integritätsprüfung der biophilen Chronik...")
    init_chronicle = IntegrityChronicle(filename="biophilic_integrity_history.json")
    # ...

    import json
    print("🔒 Initiiere Integritätsprüfung der biophilen Chronik...")
    init_chronicle = IntegrityChronicle(filename="biophilic_integrity_history.json")
    
    if not init_chronicle.verify_integrity():
        print("🚨 CRITICAL_SECURITY_BREACH: Die historische Chronik wurde manipuliert!")
        print("🛑 Systemstart zum Schutz der biophilen Wahrheit verweigert.")
        sys.exit(1)
        
    try:
        sys.path.append(os.path.join(BASE_PATH, 'implementation/prototypes'))
        from simulation_env import BiophilicSimulationSuite
        
        print("🚀 Integrität verifiziert. Starte BIF-Echtzeit-Netzwerk-Simulation...")
        suite = BiophilicSimulationSuite()
        # Wir übergeben die universelle Schleife an die Suite
        suite.run_infinite_simulation(run_biophilic_loop)
            
    except ImportError:
        print("⚠️ simulation_env.py nicht im Pfad. Starte manuellen Einzel-Test...")
        test_data = {
            "Forest_Node_01": {
                "audio_harmony": 0.85, "soil_moisture": 45.0, 
                "ambient_light": 600.0, "mycelium_activity": 0.5
            }
        }
        run_biophilic_loop(test_data)
