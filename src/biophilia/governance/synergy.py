"""
synergy.py – Emergent pattern recognition for Pillar III (1 + 1 = 3).

Detects coherent coupling between sensor pairs and returns actionable
synergy recommendations when both values reside in their respective
"Golden Zones" simultaneously.
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

# Optimal operating ranges per sensor (centre = biological ideal).
_GOLDEN_ZONES: dict[str, tuple[float, float]] = {
    "audio_harmony": (0.75, 0.95),
    "soil_moisture": (42.0, 55.0),
    "ambient_light": (400.0, 650.0),
    "mycelium_activity": (0.40, 0.60),
    "air_quality_co2": (380.0, 420.0),
}

_COUPLING_THRESHOLD = 0.65  # minimum coherence score to acknowledge a synergy


class SynergyLogic:
    """
    Identifies cross-sensor synergies in a sensor reading.

    All returned recommendation dicts share the same schema::

        {
            "pattern":        str,   # human-readable pattern name
            "action":         str,   # recommended system action
            "impact":         str,   # quantified impact string
            "recommendation": str,   # plain-language explanation
        }
    """

    def __init__(self) -> None:
        self.golden_zones: dict[str, tuple[float, float]] = dict(_GOLDEN_ZONES)

    # ── Coherence maths ───────────────────────────────────────────────────────

    def _coherence(
        self,
        val1: float,
        zone1: tuple[float, float],
        val2: float,
        zone2: tuple[float, float],
    ) -> float:
        """
        Measure how synchronously two sensor values sit within their comfort zones.

        Returns a value in [0, 1]:  1.0 = both exactly at their ideal midpoints,
        0.0 = at least one value is outside its zone.
        """
        ideal1 = (zone1[0] + zone1[1]) / 2.0
        ideal2 = (zone2[0] + zone2[1]) / 2.0
        span1 = (zone1[1] - zone1[0]) / 2.0
        span2 = (zone2[1] - zone2[0]) / 2.0

        dev1 = abs(val1 - ideal1) / (span1 + 1e-9)
        dev2 = abs(val2 - ideal2) / (span2 + 1e-9)

        if dev1 > 1.0 or dev2 > 1.0:
            return 0.0

        return round(1.0 - abs(dev1 - dev2) * 0.5, 4)

    # ── Pattern detectors ─────────────────────────────────────────────────────

    def _biosemiotic_coupling(self, audio: float, mycelium: float) -> dict | None:  # type: ignore[type-arg]
        """Kopplung Waldklang ↔ Myzel (Pillar III: organic binding)."""
        c = self._coherence(
            audio,
            self.golden_zones["audio_harmony"],
            mycelium,
            self.golden_zones["mycelium_activity"],
        )
        if c < _COUPLING_THRESHOLD:
            return None
        return {
            "pattern": "Biosemiotic Coupling",
            "action": "Amplify symbiotic information flow",
            "impact": f"Resonance Efficiency: {c:.2f}",
            "recommendation": (
                "Interspecies communication high. Knowledge sharing active (1+1=3)."
            ),
        }

    def _meditative_synergy(self, audio: float, light: float) -> dict | None:  # type: ignore[type-arg]
        """Kopplung Waldklang ↔ Licht (Pillar III: energy harmony)."""
        c = self._coherence(
            audio,
            self.golden_zones["audio_harmony"],
            light,
            self.golden_zones["ambient_light"],
        )
        if c < 0.70:
            return None
        return {
            "pattern": "Meditative Synergy",
            "action": "Optimise metabolic frequency",
            "impact": f"Energy Reserve Gain: +{c * 10:.1f} %",
            "recommendation": (
                "High resonance between light and audio. Transitioning to efficient monitoring."
            ),
        }

    def _rhizomatic_equilibrium(self, moisture: float, mycelium: float) -> dict | None:  # type: ignore[type-arg]
        """Kopplung Feuchtigkeit ↔ Myzel (Pillar I: physical foundation)."""
        c = self._coherence(
            moisture,
            self.golden_zones["soil_moisture"],
            mycelium,
            self.golden_zones["mycelium_activity"],
        )
        if c < 0.70:
            return None
        return {
            "pattern": "Rhizomatic Equilibrium",
            "action": "Prioritise nutrient flow",
            "impact": f"Biomass Emergence Index: {c:.2f}",
            "recommendation": (
                "Optimal root-mycelium coupling detected. Physical integrity solid."
            ),
        }

    # ── Public interface ──────────────────────────────────────────────────────

    def get_synergy_recommendations(self, sensor_data: dict[str, float]) -> list[dict]:  # type: ignore[type-arg]
        """Return a (possibly empty) list of active synergy recommendation dicts."""
        audio = sensor_data.get("audio_harmony", 0.85)
        light = sensor_data.get("ambient_light", 500.0)
        moisture = sensor_data.get("soil_moisture", 45.0)
        mycelium = sensor_data.get("mycelium_activity", 0.5)

        candidates = [
            self._biosemiotic_coupling(audio, mycelium),
            self._meditative_synergy(audio, light),
            self._rhizomatic_equilibrium(moisture, mycelium),
        ]
        active = [r for r in candidates if r is not None]
        logger.debug("Synergy scan: %d active pattern(s) detected.", len(active))
        return active
