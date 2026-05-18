"""
simulation.py – Multi-node environment simulation (Säule III).

Generates randomised sensor data for two forest nodes with occasional
crisis injections (5 % probability per node per tick) to test the
complete governance pipeline under stress conditions.
"""

from __future__ import annotations

import logging
import random
import time
from collections.abc import Callable

logger = logging.getLogger(__name__)

NetworkData = dict[str, dict[str, float]]


class BiophilicSimulationSuite:
    """
    Synthetic multi-node data generator.

    Runs indefinitely until interrupted.  Calls *network_orchestrator_func*
    with a fresh :class:`NetworkData` dict every *tick_interval* seconds.

    Parameters
    ----------
    tick_interval:
        Seconds between simulation ticks.
    crisis_probability:
        Probability [0, 1] that any given tick contains a single-node crisis.
    """

    def __init__(
        self,
        tick_interval: float = 4.0,
        crisis_probability: float = 0.05,
    ) -> None:
        self.tick_interval = tick_interval
        self.crisis_probability = crisis_probability
        self._running = True

    # ── Data generation ───────────────────────────────────────────────────────

    def generate_network_data(self) -> NetworkData:
        """
        Return one tick of fabricated sensor readings for both nodes.

        Forest_Node_02 simulates a deeper, darker part of the forest with
        slightly drier soil and less light than Node_01.
        """
        node_01: dict[str, float] = {
            "audio_harmony": round(random.uniform(0.75, 0.95), 2),
            "soil_moisture": round(random.uniform(43.0, 52.0), 1),
            "ambient_light": round(random.uniform(450.0, 550.0), 0),
            "mycelium_activity": round(random.uniform(0.42, 0.58), 2),
        }

        node_02: dict[str, float] = {
            "audio_harmony": round(random.uniform(0.70, 0.90), 2),
            "soil_moisture": round(random.uniform(38.0, 47.0), 1),
            "ambient_light": round(random.uniform(300.0, 420.0), 0),
            "mycelium_activity": round(random.uniform(0.40, 0.55), 2),
        }

        trigger = random.random()
        if trigger < self.crisis_probability:
            logger.warning("ANOMALY INJECTION: Forest_Node_01 collapse (drought/shock)!")
            node_01.update({"audio_harmony": 0.02, "soil_moisture": 12.0, "mycelium_activity": 4.5})
        elif trigger > (1.0 - self.crisis_probability):
            logger.warning("ANOMALY INJECTION: Forest_Node_02 collapse (light/mycelium stress)!")
            node_02.update({"audio_harmony": 0.05, "soil_moisture": 15.0, "mycelium_activity": 4.8})

        return {"Forest_Node_01": node_01, "Forest_Node_02": node_02}

    # ── Simulation runner ─────────────────────────────────────────────────────

    def run_infinite_simulation(
        self,
        network_orchestrator_func: Callable[[NetworkData], None],
    ) -> None:
        """
        Drive the simulation loop until ``KeyboardInterrupt``.

        Parameters
        ----------
        network_orchestrator_func:
            Callable that accepts a :class:`NetworkData` dict.  Typically
            ``BIFApplication.run_network_tick``.
        """
        logger.info(
            "Multi-node simulation started (tick=%.1fs, crisis_p=%.0f %%).",
            self.tick_interval,
            self.crisis_probability * 100,
        )
        try:
            while self._running:
                network_data = self.generate_network_data()
                network_orchestrator_func(network_data)
                time.sleep(self.tick_interval)
        except KeyboardInterrupt:
            logger.info("Simulation stopped by user.")
        finally:
            self._running = False

    def stop(self) -> None:
        """Signal the simulation loop to terminate after the current tick."""
        self._running = False
