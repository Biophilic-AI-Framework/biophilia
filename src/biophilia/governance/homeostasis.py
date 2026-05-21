"""
homeostasis.py – Trend-watching and damping controller (Säule I).

Detects whether the system is drifting towards instability by maintaining a
rolling window of dissonance scores.  An acute spike is never smoothed away
by the averaging algorithm (Pillar I: an acute threat must not be hidden).

Bug fixed vs. original: ``correction_history`` now uses a ``deque`` with a
fixed ``maxlen``, eliminating the O(n) ``list.pop(0)`` anti-pattern.
"""

from __future__ import annotations

import collections
import logging
import time
from typing import Any

logger = logging.getLogger(__name__)


class HomeostasisController:
    """
    Stateful trend-watcher for a single network node.

    Parameters
    ----------
    thresholds:
        Dict with at least ``dissonance_warning`` (float).
    baseline_data:
        Nested dict ``{sensor_name: {"ideal": float, ...}, ...}``.
    history_depth:
        Number of past dissonance scores kept in the rolling window.
    correction_history_depth:
        Maximum number of correction records kept in memory.
    """

    _SPIKE_MULTIPLIER = 1.5  # factor above warning threshold that triggers instant alert

    def __init__(
        self,
        thresholds: dict[str, float],
        baseline_data: dict[str, Any],
        history_depth: int = 10,
        correction_history_depth: int = 100,
    ) -> None:
        self.warning_threshold: float = thresholds.get("dissonance_warning", 0.2)
        self.baseline = baseline_data
        self.damping_factor: float = 0.7

        # Rolling window – cheap appends and finite memory.
        self.dissonance_history: collections.deque[float] = collections.deque(maxlen=history_depth)
        self.correction_history: collections.deque[dict] = collections.deque(  # type: ignore[type-arg]
            maxlen=correction_history_depth
        )

        logger.info(
            "HomeostasisController initialised (warning_threshold=%.2f).", self.warning_threshold
        )

    # ── Public interface ──────────────────────────────────────────────────────

    def analyze_trend(self, current_dissonance: float) -> bool:
        """
        Return ``True`` when the trend suggests an emerging stability threat.

        An *acute spike* (≥ 1.5× the warning threshold) triggers immediately,
        regardless of the rolling average, so that a sudden shock is never
        dampened before the system can respond.
        """
        self.dissonance_history.append(current_dissonance)

        if len(self.dissonance_history) < 3:
            return False

        # Pillar I: acute spikes must never be averaged away.
        if current_dissonance >= self.warning_threshold * self._SPIKE_MULTIPLIER:
            logger.debug(
                "Acute spike detected: dissonance=%.4f, spike_floor=%.4f.",
                current_dissonance,
                self.warning_threshold * self._SPIKE_MULTIPLIER,
            )
            return True

        avg = sum(self.dissonance_history) / len(self.dissonance_history)
        return avg >= self.warning_threshold

    def apply_damping(self, delta: float, parameter_name: str | None = None) -> float:
        """Asymptotic correction: scale *delta* by the damping factor to prevent overshoot."""
        return delta * self.damping_factor

    def log_correction(self, param: str, value: float, correction: float) -> None:
        """Record a corrective action for Pillar III (full traceability)."""
        self.correction_history.append(
            {
                "timestamp": time.time(),
                "parameter": param,
                "value": value,
                "correction": correction,
            }
        )

    def is_stable(self, current_value: float, parameter_name: str, threshold: float = 0.05) -> bool:
        """
        Return ``True`` when *current_value* is within *threshold* of the
        biological ideal for *parameter_name*.
        """
        from typing import cast

        # Wir casten den Rückgabewert aus dem verschachtelten Dict explizit zu einem float
        target = cast(float, self.baseline.get(parameter_name, {}).get("ideal", 0.0))
        
        if target == 0.0:
            return True
            
        deviation = abs(target - current_value) / target
        return deviation <= threshold
