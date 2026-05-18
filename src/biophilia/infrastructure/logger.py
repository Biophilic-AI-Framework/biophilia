"""
logger.py – Structured pulse logger for inter-zone data flow (Säule III).

Wraps the standard ``logging`` module with a zone-aware ``log_pulse()`` method.
Console output is intentionally disabled by default; the caller can add a
``StreamHandler`` if needed.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

_DEFAULT_LOG_NAME = "biophilia_pulse.log"
_FORMAT = "%(asctime)s | %(levelname)-8s | %(message)s"
_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"


class BiophilicLogger:
    """
    Structured logger that documents the biosemiotic data flow between zones.

    Parameters
    ----------
    log_name:
        Name of the log file (not the full path).
    log_dir:
        Directory in which the file is created.  Defaults to ``./logs``.
    console:
        When ``True``, a :class:`logging.StreamHandler` is also attached.
    """

    def __init__(
        self,
        log_name: str = _DEFAULT_LOG_NAME,
        log_dir: Path | None = None,
        *,
        console: bool = False,
    ) -> None:
        log_directory = log_dir or Path.cwd() / "logs"
        log_directory.mkdir(parents=True, exist_ok=True)
        self.log_path = log_directory / log_name

        # Use a named logger so multiple instances can coexist safely.
        self._logger = logging.getLogger(f"biophilia.pulse.{log_name}")
        self._logger.setLevel(logging.INFO)

        if not self._logger.handlers:
            formatter = logging.Formatter(_FORMAT, datefmt=_DATE_FORMAT)

            fh = logging.FileHandler(self.log_path, encoding="utf-8")
            fh.setFormatter(formatter)
            self._logger.addHandler(fh)

            if console:
                sh = logging.StreamHandler()
                sh.setFormatter(formatter)
                self._logger.addHandler(sh)

    def log_pulse(self, zone: str, message: str, data: Any = None) -> None:
        """
        Record a single system pulse.

        Parameters
        ----------
        zone:
            The processing zone label (e.g. ``"Forest_Node_01-Zone A"``).
        message:
            A human-readable status message.
        data:
            Optional supplementary payload (serialised with ``str()``).
        """
        payload = f"[{zone}] {message}"
        if data is not None:
            payload += f" | data={data}"
        self._logger.info(payload)
