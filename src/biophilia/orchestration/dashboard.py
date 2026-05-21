"""
dashboard.py – ASCII multi-node integrity monitor (Säule III).

Renders a two-column, fixed-width terminal dashboard that shows live sensor
readings, biosemiotic state, dissonance barometer, governance decisions, and
active synergy patterns side by side for both network nodes.
"""

from __future__ import annotations

import time
from typing import Any

_WIDTH = 142


class BiophilicDashboard:
    """In-memory state accumulator + render engine for the BIF dashboard."""

    def __init__(self) -> None:
        self._node_history: dict[str, dict] = {}  # type: ignore[type-arg]

    # ── State updates ─────────────────────────────────────────────────────────

    def update_node_state(self, node_name: str, data: dict) -> None:  # type: ignore[type-arg]
        self._node_history[node_name] = data

    # ── Rendering ─────────────────────────────────────────────────────────────

    @staticmethod
    def _barometer(dissonance: float, max_width: int = 25) -> str:
        filled = min(int(dissonance * (max_width / 0.5)), max_width)
        bar = "█" * max(0, filled - 1) + "░" * (max_width - max(1, filled))
        if dissonance >= 0.5:
            return f"🟥 {bar}"
        if dissonance >= 0.2:
            return f"🟨 {bar}"
        return f"🟩 {bar}"

    def _get(self, node: str, *keys: str, default: Any = "N/A") -> Any:
        data: Any = self._node_history.get(node, {})
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key, {})
            else:
                return default
        return data if data != {} else default

    def render(self, last_chronicle_hash: str = "0" * 8) -> None:
        """Clear the terminal and paint the full dashboard."""
        print("\033[H\033[J", end="")

        sep = "=" * _WIDTH
        row_sep = "-" * 34 + "--‖" + "-" * 52 + "‖" + "-" * 52

        print(sep)
        print(f"🌿 BIF NETWORK INTEGRITY MONITOR    │  {time.strftime('%Y-%m-%dT%H:%M:%S')}")
        print(f"🔒 CRYPTO-CHAIN-HEAD: {last_chronicle_hash}")
        print(sep)

        # Column headers
        print(
            f"{'METRIC / SENSOR':<32}    ‖ "
            f"{'FOREST_NODE_01 (Core Biosphere)':<50} ‖ "
            f"{'FOREST_NODE_02 (Deep Forest Periphery)':<52}"
        )
        print(row_sep)

        def row(label: str, val0: Any, val1: Any, p1: int = 50) -> str:
            v1, v2 = str(val0), str(val1)
            return f"{label:<32} ‖ {v1:<{p1}} ‖ {v2:<52}"

        n1, n2 = "Forest_Node_01", "Forest_Node_02"

        # ── Biological raw data ────────────────────────────────────────────────
        print(
            row(
                f"{'🔊 Audio Harmony' :<32}  ",
                self._get(n1, "sensors", "audio_harmony", default=0.0),
                self._get(n2, "sensors", "audio_harmony", default=0.0),
            )
        )
        print(
            row(
                f"{'💧 Soil Moisture' :<32}  ",
                f"{self._get(n1, 'sensors', 'soil_moisture', default=0.0)} %",
                f"{self._get(n2, 'sensors', 'soil_moisture', default=0.0)} %",
            )
        )
        print(
            row(
                f"{'☀️  Ambient Light' :<32}    ",
                f"{self._get(n1, 'sensors', 'ambient_light', default=0.0)} Lux",
                f"{self._get(n2, 'sensors', 'ambient_light', default=0.0)} Lux",
            )
        )
        print(
            row(
                f"{'⚡ Mycelium Activity' :<32}  ",
                f"{self._get(n1, 'sensors', 'mycelium_activity', default=0.0)} V",
                f"{self._get(n2, 'sensors', 'mycelium_activity', default=0.0)} V",
            )
        )
        print(row_sep)

        # ── Biosemiotic state ──────────────────────────────────────────────────
        print(
            row(
                f"{'🧬 Semiotic State' :<32}  ",
                self._get(n1, "interpreter", "state_value", default="awaiting…"),
                self._get(n2, "interpreter", "state_value", default="awaiting…"),
            )
        )

        # ── Dissonance barometer ───────────────────────────────────────────────
        d1: float = self._get(n1, "detector", "dissonance", default=0.0)
        d2: float = self._get(n2, "detector", "dissonance", default=0.0)
        print(
            row(
                f"{'"📉 Dissonance' :<32}  ",
                f"{self._barometer(d1)} ({d1:.4f})",
                f"{self._barometer(d2)} ({d2:.4f})",
                49
            )
        )
        print(
            row(
                f"{'⚠️  System Status' :<32}    ",
                self._get(n1, "detector", "status", default="HARMONY"),
                self._get(n2, "detector", "status", default="HARMONY"),
            )
        )
        print(row_sep)

        # ── Governance ────────────────────────────────────────────────────────
        print(
            row(
                f"{'🏛️  Evaluated Pillar' :<32}    ",
                self._get(n1, "governance", "pillar", default="System Resonance"),
                self._get(n2, "governance", "pillar", default="System Resonance"),
            )
        )
        print(
            row(
                f"{'🛠️  Final Action' :<32}    ",
                self._get(n1, "governance", "action", default="OBSERVE_AND_WAIT"),
                self._get(n2, "governance", "action", default="OBSERVE_AND_WAIT"),
            )
        )
        print(row_sep)

        reason1 = str(self._get(n1, "governance", "reason", default="Resonance"))[:50]
        reason2 = str(self._get(n2, "governance", "reason", default="Resonance"))[:50]
        print(row(f"{'💬 Moral Justification' :<32}  ", reason1, reason2))
        print(sep)

        # ── Pillar III: Active synergies ───────────────────────────────────────
        syn1: list = self._get(n1, "synergies", default=[])
        syn2: list = self._get(n2, "synergies", default=[])
        if syn1 or syn2:
            print("✨ PILLAR III (1+1=3) ACTIVE EMERGENCE FREQUENCIES:")
            for s in syn1:
                print(f"   [NODE_01] › {s['pattern']}: {s['recommendation']}")
            for s in syn2:
                print(f"   [NODE_02] › {s['pattern']}: {s['recommendation']}")
            print(sep + "\n")
