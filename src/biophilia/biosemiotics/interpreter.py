"""
interpreter.py – Biosemiotic signal interpretation (Säulen I–III).

Translates raw sensor readings into typed, semantically rich BioSignals and
synthesises them into a holistic BioState.  Vocal-pattern data is loaded from
the bundled package resource so no filesystem path wrangling is needed.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from enum import Enum
from importlib.resources import files

logger = logging.getLogger(__name__)


class BioState(Enum):
    HARMONY = "Harmonie/Wachstum"
    STRESS = "Stress/Alarm"
    DORMANT = "Ruhezustand/Dormanz"
    RECOVERY = "Erholung"
    CRITICAL = "Kritischer Zustand"


@dataclass(frozen=True, slots=True)
class BioSignal:
    token: BioState
    intensity: float
    source: str


class BiosemioticInterpreter:
    """
    Translates sensor streams into the biosemiotic sign-system of the forest.

    Thresholds
    ----------
    mycelium_v_drop:
        Voltage below which mycelium activity signals a critical deficit.
    mycelium_v_max_harmony:
        Voltage ceiling for healthy growth; beyond this → toxic overload.
    acoustic_var_high:
        Variance threshold above which acoustic noise indicates stress.
    """

    _THRESHOLDS: dict[str, float] = {
        "mycelium_v_drop": 0.2,
        "mycelium_v_max_harmony": 1.5,
        "acoustic_var_high": 0.7,
    }

    def __init__(self) -> None:
        self.patterns: dict[str, dict] = {}  # type: ignore[type-arg]
        try:
            data_file = files("biophilia._data").joinpath("vocal_patterns.json")
            raw = json.loads(data_file.read_text(encoding="utf-8"))
            self.patterns = raw.get("patterns", {})
        except Exception:  # noqa: BLE001 – missing resource must not crash the process
            logger.warning("vocal_patterns.json could not be loaded; pattern dict is empty.")

        self.thresholds = dict(self._THRESHOLDS)

    # ── Signal primitives ─────────────────────────────────────────────────────

    def interpret_mycelium(self, voltage: float, conductivity: float) -> BioSignal:
        """Map mycelium voltage + conductivity to a BioSignal."""
        drop_v = self.thresholds["mycelium_v_drop"]
        max_h = self.thresholds["mycelium_v_max_harmony"]

        if voltage < drop_v:
            intensity = round((drop_v - voltage) / drop_v, 4)
            return BioSignal(BioState.CRITICAL, intensity, "Mycelium_Deficit")

        if voltage > max_h:
            # Asymptotic criticality: small exceedances → rising alarm.
            excess = voltage - max_h
            intensity = round(1.0 - 1.0 / (1.0 + excess), 4)
            return BioSignal(BioState.CRITICAL, intensity, "Mycelium_Overload")

        if voltage > 0.4:
            return BioSignal(BioState.HARMONY, round(voltage / max_h, 4), "Mycelium")

        return BioSignal(BioState.DORMANT, 0.5, "Mycelium")

    def interpret_acoustics(self, noise_db: float, variance: float) -> BioSignal:
        """
        Map acoustic environment to a BioSignal.

        Absolute silence (variance ≈ 0) is a *critical* alarm — it signals
        that every organism in the biome has gone quiet out of fear.
        """
        if variance < 0.05:
            return BioSignal(BioState.CRITICAL, 0.95, "Acoustics_Vigilance")

        if variance > self.thresholds["acoustic_var_high"]:
            return BioSignal(BioState.STRESS, round(variance, 4), "Acoustics_Noise")

        return BioSignal(BioState.HARMONY, round(1.0 - variance, 4), "Acoustics")

    # ── Synthesis ─────────────────────────────────────────────────────────────

    def synthesize_state(self, signals: list[BioSignal]) -> BioState:
        """
        Reduce a list of BioSignals to the holistic worst-case state.

        Critical always wins; stress beats harmony.  This implements Pillar I:
        the protection of life overrides all optimistic readings.
        """
        tokens = {s.token for s in signals}
        if BioState.CRITICAL in tokens:
            return BioState.CRITICAL
        if BioState.STRESS in tokens:
            return BioState.STRESS
        if BioState.RECOVERY in tokens:
            return BioState.RECOVERY
        if BioState.DORMANT in tokens:
            return BioState.DORMANT
        return BioState.HARMONY
