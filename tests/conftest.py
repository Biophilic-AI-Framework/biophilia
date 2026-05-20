"""
conftest.py – Shared pytest fixtures.

All tests that touch the filesystem use ``tmp_path`` (pytest's built-in
temporary directory fixture) so no real log files are created during CI.
"""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def bif_secret_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """Inject a dummy secret key so BiophilicActionInterface can be instantiated in tests."""
    monkeypatch.setenv("BIF_SECRET_KEY", "test-secret-key-do-not-use-in-prod")


@pytest.fixture()
def sensor_data_harmony() -> dict[str, float]:
    return {
        "audio_harmony": 0.85,
        "soil_moisture": 45.0,
        "ambient_light": 600.0,
        "mycelium_activity": 0.5,
    }


@pytest.fixture()
def sensor_data_crisis() -> dict[str, float]:
    """Sensor readings that mimic a severe drought + mycelium overload."""
    return {
        "audio_harmony": 0.02,
        "soil_moisture": 12.0,
        "ambient_light": 600.0,
        "mycelium_activity": 4.5,
    }


@pytest.fixture()
def network_data_harmony(sensor_data_harmony: dict[str, float]) -> dict[str, dict[str, float]]:
    return {
        "Forest_Node_01": dict(sensor_data_harmony),
        "Forest_Node_02": dict(sensor_data_harmony),
    }
