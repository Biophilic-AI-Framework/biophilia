"""
interface.py – Physical actuator interface with ethical gate (Säule II).

All public action methods are wrapped by ``@impact_audit``, which reads the
current system dissonance from ``self._detector`` and blocks execution when
the calculated harm potential exceeds the declared ceiling.

Security requirement: ``BIF_SECRET_KEY`` must be set in the environment.
The application's entry point should validate this before constructing the
object (fail-fast); the constructor enforces it as a final-line defence.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

from biophilia.audit.chronicle import IntegrityChronicle
from biophilia.audit.impact_audit import impact_audit
from biophilia.biosemiotics.entropy_detector import BiophilicEntropyDetector

logger = logging.getLogger(__name__)

_MAX_IRRIGATION_SECONDS = 300


class BiophilicActionInterface:
    """
    Executing arm of the BIF.

    Parameters
    ----------
    pump_api_url:
        Endpoint for the irrigation actuator.
    detector_ref:
        Reference to the active :class:`BiophilicEntropyDetector` so that the
        ``@impact_audit`` decorator can read ``last_calculated_dissonance``
        without any module-level import.
    log_dir:
        Directory where the chronicle file lives.  Forwarded to
        :class:`IntegrityChronicle`.
    """

    def __init__(
        self,
        pump_api_url: str = "http://localhost/pump",
        detector_ref: BiophilicEntropyDetector | None = None,
        log_dir: Path | None = None,
    ) -> None:
        secret_key = os.getenv("BIF_SECRET_KEY")
        if not secret_key:
            raise RuntimeError(
                "CRITICAL_SECURITY_FAILURE: BIF_SECRET_KEY is not set. Actuator access denied."
            )

        self.pump_url = pump_api_url
        self._api_key: str = secret_key
        self._detector = detector_ref
        self.chronicle = IntegrityChronicle(log_dir=log_dir)

    # ── Actions ───────────────────────────────────────────────────────────────

    @impact_audit(max_maleficence=0.01, min_synergy=4.0)
    def trigger_irrigation(self, duration_seconds: int, **kwargs: float) -> bool:
        """
        Activate the irrigation pump for *duration_seconds*.

        The declared ``maleficence=0.0`` in kwargs tells the audit decorator
        that this call is benign.  The duration is capped at 5 minutes to
        prevent accidental flooding.
        """
        if duration_seconds <= 0:
            logger.warning("Ignoring zero or negative irrigation duration.")
            return False

        if duration_seconds > _MAX_IRRIGATION_SECONDS:
            logger.warning(
                "Irrigation duration %ds exceeds safety limit; capped to %ds.",
                duration_seconds,
                _MAX_IRRIGATION_SECONDS,
            )
            duration_seconds = _MAX_IRRIGATION_SECONDS

        logger.info("VITAL-ACTION: Pump activated for %d s.", duration_seconds)
        return True

    @impact_audit(max_maleficence=0.0, min_synergy=5.0)
    def lock_system_port(self, port: int, **kwargs: float) -> bool:
        """
        Isolate *port* in response to an acoustic threat signal.

        The zero-tolerance maleficence ceiling (0.0) means this action will
        be blocked whenever the system is already under any measurable stress.
        """
        if not 1 <= port <= 65535:
            logger.error("Invalid port %d suppressed.", port)
            return False

        logger.warning("PROTECTION MODE: System port %d isolated.", port)
        return True

    # ── Veto handler ──────────────────────────────────────────────────────────

    def handle_veto(
        self,
        action_name: str,
        error_message: str,
        node_name: str = "SYSTEM",
    ) -> None:
        """Record a vetoed action in the tamper-evident chronicle."""
        self.chronicle.record_action(
            node_name=node_name,
            action_name=f"VETO_{action_name}",
            pillar="PILLAR I (Non-Maleficence)",
            reason=f"Action blocked by audit: {error_message}",
            synergy_score=0.0,
        )
