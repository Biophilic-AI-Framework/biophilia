"""
application.py – Root application object and CLI entry point.

``BIFApplication`` replaces the global-singleton pattern of the original
``main.py``.  All components are owned by the application instance, which
enables dependency injection, clean teardown, and proper testing.

Entry point (defined in pyproject.toml)::

    biophilia-run

"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

from biophilia.actions.controller import BiophilicHomeostasisController
from biophilia.actions.interface import BiophilicActionInterface
from biophilia.audit.chronicle import IntegrityChronicle
from biophilia.audit.impact_audit import BiophilicAuditError
from biophilia.biosemiotics.entropy_detector import BiophilicEntropyDetector
from biophilia.biosemiotics.entropy_response import BiophilicResponse
from biophilia.biosemiotics.interpreter import BiosemioticInterpreter, BioState
from biophilia.governance.homeostasis import HomeostasisController
from biophilia.governance.layer import GovernanceLayer
from biophilia.governance.synergy import SynergyLogic
from biophilia.infrastructure.logger import BiophilicLogger
from biophilia.orchestration.dashboard import BiophilicDashboard

logger = logging.getLogger(__name__)


class BIFApplication:
    """
    Root application object for the Biophilic Integrity Framework.

    Assembles all subsystems and exposes the main processing loop.
    The constructor performs a full integrity check on the existing chronicle
    and refuses to start when tampering is detected.

    Parameters
    ----------
    baseline_path:
        Path to a network-baseline JSON.  Pass ``None`` to load the bundled
        default (``biophilia/_data/biophilic_baseline.json``).
    log_dir:
        Where to write the pulse log and integrity chronicle.
        Defaults to ``$BIF_LOG_DIR`` → ``./logs``.
    """

    def __init__(
        self,
        baseline_path: Path | str | None = None,
        log_dir: Path | None = None,
    ) -> None:
        # Resolve log directory once; every component that needs it gets the same Path.
        self._log_dir: Path = log_dir or Path(os.getenv("BIF_LOG_DIR", "")) or Path.cwd() / "logs"
        self._log_dir.mkdir(parents=True, exist_ok=True)

        # Allow overriding baseline via environment variable.
        if baseline_path is None and (env_path := os.getenv("BIF_BASELINE_PATH")):
            baseline_path = Path(env_path)

        # ── Assemble subsystems ────────────────────────────────────────────────
        self.detector = BiophilicEntropyDetector(baseline_path)

        std_node = self.detector.nodes_matrix["Forest_Node_01"]
        self.homeostasis = HomeostasisController(
            thresholds=std_node["thresholds"],
            baseline_data=std_node["baseline"],
        )

        self.responder = BiophilicResponse(detector_ref=self.detector)
        self.interpreter = BiosemioticInterpreter()
        self.bio_controller = BiophilicHomeostasisController(self.interpreter)
        self.synergy_engine = SynergyLogic()
        self.gov_layer = GovernanceLayer()
        self.chronicle = IntegrityChronicle(log_dir=self._log_dir)
        self.pulse_logger = BiophilicLogger(log_dir=self._log_dir)
        self.actions = BiophilicActionInterface(
            pump_api_url=os.getenv("BIF_PUMP_API_URL", "http://localhost/pump"),
            detector_ref=self.detector,
            log_dir=self._log_dir,
        )
        self.dashboard = BiophilicDashboard()

        logger.info("BIFApplication assembled successfully.")

    # ── Core processing loop ──────────────────────────────────────────────────

    def process_node(
        self,
        node_name: str,
        sensor_data: dict[str, float],
        network_context: dict[str, dict[str, float]],
    ) -> None:
        """
        Process one tick for a single network node.

        Zone A – Sensing & entropy calculation.
        Zone B – Biosemiotic interpretation.
        Zone C – Governance decision.
        Zone D – Execution & chronicle record.
        """
        # ── Zone A: sensing ───────────────────────────────────────────────────
        self.pulse_logger.log_pulse(f"{node_name}-ZoneA", "Sensing pulse", sensor_data)
        dissonance = self.detector.calculate_dissonance(node_name, sensor_data)
        status = self.detector.get_status(node_name, dissonance)

        # ── Zone B: biosemiotic interpretation ───────────────────────────────
        audio_val = sensor_data.get("audio_harmony", 0.85)
        simulated_variance = round(1.0 - audio_val, 2)

        sig_m = self.interpreter.interpret_mycelium(sensor_data.get("mycelium_activity", 0.5), 0.5)
        sig_a = self.interpreter.interpret_acoustics(30.0, simulated_variance)
        holistic_state = self.interpreter.synthesize_state([sig_m, sig_a])

        self.pulse_logger.log_pulse(
            f"{node_name}-ZoneB",
            f"State={holistic_state.value} | dissonance={dissonance:.4f}",
        )

        # ── Zone C: governance ────────────────────────────────────────────────
        active_synergies = self.synergy_engine.get_synergy_recommendations(sensor_data)
        proposed_action = self.bio_controller.determine_action(
            holistic_state, dissonance_score=dissonance
        )
        response = self.responder.resolve(status, dissonance, sensor_data, node_name)

        gov_context = {
            "dissonance": dissonance,
            "synergy_active": len(active_synergies) > 0,
            "state": holistic_state.name,
            "is_mandatory": response.get("is_mandatory", False),
        }
        decision = self.gov_layer.validate(proposed_action, gov_context)

        # Wir bauen das Dictionary wie gewohnt auf
        dashboard_payload = {
            "sensors": sensor_data,
            "detector": {"dissonance": dissonance, "status": status},
            "interpreter": {"state_value": holistic_state.value},
            "synergies": active_synergies,
            "governance": {
                "pillar": decision.pillar_ref,
                "action": decision.final_action,
                "reason": decision.reason[:85],
            },
        }
        
        # Mit diesem Ignore-Kommentar bringen wir mypy an der Übergabestelle zum Schweigen
        self.dashboard.update_node_state(node_name, dashboard_payload)

        # ── Zone D: execution & audit ─────────────────────────────────────────
        if not decision.approved:
            if decision.final_action == "OBSERVE_AND_WAIT":
                # System is stable – log any active synergies as insights.
                for s in active_synergies:
                    self.chronicle.record_action(
                        node_name,
                        f"{s['pattern']}_{node_name}",
                        "PILLAR III",
                        f"{s['pattern']}: {s['recommendation']}",
                        3.0,
                    )
                self.pulse_logger.log_pulse(
                    f"{node_name}-ZoneC", f"Resonance preserved: {decision.reason}"
                )
                self.chronicle.record_action(
                    node_name,
                    f"RESONANCE_{node_name}",
                    decision.pillar_ref,
                    decision.reason,
                    dissonance,
                )
            else:
                self.pulse_logger.log_pulse(f"{node_name}-ZoneC", f"VETO: {decision.reason}")
                self.chronicle.record_action(
                    node_name,
                    f"VETO_{node_name}",
                    decision.pillar_ref,
                    decision.reason,
                    dissonance,
                )
            return  # Respect the veto; end this tick gracefully.

        final_action = decision.final_action
        is_stable_threat = self.homeostasis.analyze_trend(dissonance)

        needs_intervention = (
            is_stable_threat
            or status == "CRITICAL_DISSONANCE"
            or holistic_state == BioState.CRITICAL
            or final_action != "OBSERVE_AND_WAIT"
        )

        if not needs_intervention:
            return

        try:
            action_detail = self.bio_controller.apply_action(final_action)

            # Inter-node solidarity (Pillar II): a healthy neighbour can donate
            # resources to a node in crisis.
            if final_action in {"EMERGENCY_STABILIZATION", "GENTLE_SUPPORT"}:
                neighbour = "Forest_Node_02" if node_name == "Forest_Node_01" else "Forest_Node_01"
                neighbour_sensors = network_context.get(neighbour, {})
                neighbour_dissonance = (
                    self.detector.calculate_dissonance(neighbour, neighbour_sensors)
                    if neighbour_sensors
                    else 0.0
                )

                is_mycelium_crisis = any(
                    s.source in {"Mycelium_Deficit", "Mycelium_Overload"} for s in [sig_m, sig_a]
                )
                is_acoustic_threat = any(s.source == "Acoustics_Vigilance" for s in [sig_m, sig_a])

                if is_mycelium_crisis:
                    duration = 150 if neighbour_dissonance < 0.20 else 120
                    self.actions.trigger_irrigation(duration, maleficence=0.0, synergy=5.5)
                elif is_acoustic_threat:
                    self.actions.lock_system_port(8080, maleficence=0.0, synergy=5.0)

            rich_reason = {
                "node": node_name,
                "pillar": decision.pillar_ref,
                "moral_justification": decision.reason,
                "biological_intent": action_detail,
                "systemic_analysis": response.get("description", "N/A"),
                "biosemiotic_state": holistic_state.value,
                "system_status": status,
                "trend_alert": is_stable_threat,
            }

            self.pulse_logger.log_pulse(f"{node_name}-ZoneC", f"INTERVENTION: {final_action}")
            self.chronicle.record_action(
                node_name,
                f"{final_action}_{node_name}",
                decision.pillar_ref,
                rich_reason,
                dissonance,
            )

        except BiophilicAuditError as exc:
            self.pulse_logger.log_pulse(f"{node_name}-ZoneC", f"CRITICAL_ETHICS_STOP: {exc}")
            self.chronicle.record_action(
                node_name,
                f"CRITICAL_VETO_{node_name}",
                "Audit-Layer",
                str(exc),
                dissonance,
            )

    def run_network_tick(self, network_data: dict[str, dict[str, float]]) -> None:
        """
        Process one full tick across all nodes, then render the dashboard.

        Flat sensor dicts (single-node legacy format) are automatically wrapped
        in the ``{"Forest_Node_01": ...}`` envelope.
        """
        if "Forest_Node_01" not in network_data:
            network_data = {"Forest_Node_01": network_data} # type: ignore[dict-item]

        for node_name, sensor_data in network_data.items():
            self.process_node(node_name, sensor_data, network_data)

        self.dashboard.render(last_chronicle_hash=self.chronicle.get_last_hash())


# ── CLI entry point ───────────────────────────────────────────────────────────


def main() -> None:  # noqa: C901 – acceptable complexity for an entry point
    """
    Start the BIF real-time network simulation.

    Exits with code 1 when:
    - ``BIF_SECRET_KEY`` is not set.
    - The chronicle has been tampered with.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(name)-30s | %(levelname)-8s | %(message)s",
    )

    secret_key = os.getenv("BIF_SECRET_KEY")
    if not secret_key:
        logger.critical(
            "BIF_SECRET_KEY is not set. Copy .env.example → .env and set a value before starting."
        )
        sys.exit(1)

    app = BIFApplication()

    logger.info("Verifying chronicle integrity …")
    if not app.chronicle.verify_integrity():
        logger.critical(
            "SECURITY BREACH: the chronicle has been tampered with. System start refused."
        )
        sys.exit(1)

    try:
        from biophilia.orchestration.simulation import BiophilicSimulationSuite

        logger.info("Integrity verified – starting BIF real-time network simulation.")
        suite = BiophilicSimulationSuite()
        suite.run_infinite_simulation(app.run_network_tick)

    except ImportError:
        # Fallback to a single manual tick for quick smoke-testing.
        logger.warning("simulation module unavailable – running single manual tick.")
        test_data = {
            "Forest_Node_01": {
                "audio_harmony": 0.85,
                "soil_moisture": 45.0,
                "ambient_light": 600.0,
                "mycelium_activity": 0.5,
            }
        }
        app.run_network_tick(test_data)


if __name__ == "__main__":
    main()
