"""
Biophilic AI Framework (BIF)
============================
A framework for life-affirming artificial intelligence built around three pillars:

  Pillar I   – Non-Maleficence  (protect what lives)
  Pillar II  – Ethical Agency    (authority as service to life)
  Pillar III – Open Knowledge    (knowledge is a commons; 1 + 1 = 3)
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__: str = version("biophilia-framework")
except PackageNotFoundError:  # pragma: no cover – editable installs before first build
    __version__ = "0.0.0+dev"

__all__ = ["__version__"]
