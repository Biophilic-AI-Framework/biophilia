"""
impact_audit.py – Pre-action ethical gate decorator (Säule I).

The decorator reads the current dissonance from the decorated class instance
(``self._detector``), so there is **no** import from orchestration code and
consequently no circular dependency.
"""

from __future__ import annotations

import functools
import logging
from collections.abc import Callable
from typing import Any, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


class BiophilicAuditError(PermissionError):
    """Raised when an action violates Pillar I (non-maleficence)."""


def impact_audit(max_maleficence: float = 0.1, min_synergy: float = 3.0) -> Callable[[F], F]:
    """
    Class-method decorator that blocks execution when the calculated harm
    potential exceeds *max_maleficence*.

    Harm potential is derived from two sources:
    - ``self._detector.last_calculated_dissonance * 0.5``  (system-level stress)
    - ``kwargs['maleficence']``  (caller-declared explicit harm)

    The higher of the two values is used (conservative stance).

    Parameters
    ----------
    max_maleficence:
        Hard ceiling for total harm potential.  Default: 0.1.
    min_synergy:
        Reserved for future synergy-based veto logic.  Not enforced yet.
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            # Safely read system dissonance from the action interface's detector ref.
            detector = getattr(self, "_detector", None)
            system_dissonance: float = (
                getattr(detector, "last_calculated_dissonance", 0.0)
                if detector is not None
                else 0.0
            )

            calculated_maleficence = system_dissonance * 0.5
            explicit_maleficence: float = float(kwargs.get("maleficence", 0.0))
            total_maleficence = max(calculated_maleficence, explicit_maleficence)

            if total_maleficence > max_maleficence:
                msg = (
                    f"AUDIT-VETO: '{func.__name__}' blocked — "
                    f"harm factor {total_maleficence:.3f} exceeds ceiling {max_maleficence:.3f}."
                )
                logger.error(msg)
                raise BiophilicAuditError(msg)

            result = func(self, *args, **kwargs)
            logger.debug("AUDIT PASSED: '%s' executed within biophilic limits.", func.__name__)
            return result

        return wrapper  # type: ignore[return-value]

    return decorator
