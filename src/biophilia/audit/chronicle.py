"""
chronicle.py – Tamper-evident, hash-chained action log (Säule III).

Every record is SHA-256 hashed and linked to the previous entry, forming an
append-only chain.  Any post-hoc modification is detected by verify_integrity().
"""

from __future__ import annotations

import datetime
import hashlib
import json
import logging
from pathlib import Path
from typing import Any, cast  # <── Neu importiert für Typisierung und Casting

logger = logging.getLogger(__name__)

_DEFAULT_FILENAME = "biophilic_integrity_history.json"


class IntegrityChronicle:
    """
    Append-only, cryptographically chained audit log.

    Parameters
    ----------
    filename:
        Name of the JSON log file (not the full path).
    log_dir:
        Directory in which the file is created.  Defaults to ``./logs``.
    """

    def __init__(
        self,
        filename: str = _DEFAULT_FILENAME,
        log_dir: Path | None = None,
    ) -> None:
        self._log_dir = log_dir or Path.cwd() / "logs"
        self._log_dir.mkdir(parents=True, exist_ok=True)
        self.filename = self._log_dir / filename

    # ── Private helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _hash(entry: dict[str, Any]) -> str:  # <── Typisiert: dict[str, Any]
        """Deterministic SHA-256 over a JSON-serialised dict."""
        payload = json.dumps(entry, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(payload.encode()).hexdigest()

    def _load(self) -> list[dict[str, object]]:
        if not self.filename.exists():
            return []
        try:
            # cast() hinzugefügt, um den Any-Rückgabewert von json.loads zu binden
            return cast(list[dict[str, object]], json.loads(self.filename.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            logger.error("Chronicle file is structurally corrupt: %s", self.filename)
            return []

    def _save(self, history: list[dict[str, Any]]) -> None:  # <── Typisiert: list[dict[str, Any]]
        self.filename.write_text(
            json.dumps(history, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

    # ── Public API ────────────────────────────────────────────────────────────

    def record_action(
        self,
        node_name: str,
        action_name: str,
        pillar: str,
        reason: str | dict[str, Any],  # <── Typisiert: str | dict[str, Any]
        synergy_score: float,
    ) -> None:
        """
        Append a new record to the chain.

        The record includes a ``previous_hash`` that links it to its predecessor,
        and a ``current_hash`` that fingerprints its own content.
        """
        history = self._load()
        
        # cast zu str hinzugefügt, da history[...] den Typ object liefert
        previous_hash = cast(str, history[-1]["current_hash"]) if history else "0" * 64

        entry: dict[str, Any] = {  # <── Typisiert: dict[str, Any]
            "timestamp": datetime.datetime.now().isoformat(),
            "node": node_name,
            "action": action_name,
            "pillar": pillar,
            "reason": reason,
            "synergy_index": float(synergy_score),
            "previous_hash": previous_hash,
        }
        entry["current_hash"] = self._hash(entry)

        # Ein kleiner technischer Cast, um das dict[str, Any] in die list[dict[str, object]] einzufügen
        history.append(cast(dict[str, object], entry))
        
        # cast zu list[dict[str, Any]] für die Speicherfunktion
        self._save(cast(list[dict[str, Any]], history))

        preview = str(reason)[:70]
        logger.info(
            "Chronicle: [%s] hash=%s… reason=%s…",
            action_name,
            entry["current_hash"][:8],
            preview,
        )

    def get_last_hash(self) -> str:
        """Return the ``current_hash`` of the most recent record, or a genesis string."""
        history = self._load()
        # cast zu str hinzugefügt, da Werte aus dict[str, object] für mypy nur 'object' sind
        return cast(str, history[-1]["current_hash"]) if history else "0" * 64

    def verify_integrity(self) -> bool:
        """
        Walk the entire chain and confirm no entry has been tampered with.

        Returns ``True`` when the chain is intact; ``False`` on any anomaly.
        The chronicle is considered intact when the file does not yet exist.
        """
        if not self.filename.exists():
            return True

        history = self._load()
        if not history:
            return True

        for i, current in enumerate(history):
            check = {k: v for k, v in current.items() if k != "current_hash"}
            claimed_hash = current.get("current_hash")

            if claimed_hash != self._hash(check):
                logger.critical("MANIPULATION DETECTED: entry at index %d was modified!", i)
                return False

            if i > 0 and current["previous_hash"] != history[i - 1]["current_hash"]:
                logger.critical(
                    "CHAIN BREAK DETECTED: link between entries %d and %d is broken!",
                    i - 1,
                    i,
                )
                return False

        logger.info("Integrity check passed: chronicle is intact (%d records).", len(history))
        return True
