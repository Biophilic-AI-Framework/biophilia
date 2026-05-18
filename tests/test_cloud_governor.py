"""Tests for BiophilicCloudGovernor: vitality model and scaling decisions."""

from __future__ import annotations

import pytest

from biophilia.cloud.governor import BiophilicCloudGovernor, CloudResourceManager


class StubAdapter(CloudResourceManager):
    def __init__(self) -> None:
        self.cpu_calls: list[int] = []
        self.scale_calls: list[int] = []

    def update_cpu_limit(self, limit_milli_cpu: int) -> None:
        self.cpu_calls.append(limit_milli_cpu)

    def scale_instances(self, count: int) -> None:
        self.scale_calls.append(count)


@pytest.fixture()
def stub() -> StubAdapter:
    return StubAdapter()


@pytest.fixture()
def governor(stub: StubAdapter) -> BiophilicCloudGovernor:
    return BiophilicCloudGovernor(stub)


class TestVitalityModel:
    def test_initial_vitality_is_one(self, governor: BiophilicCloudGovernor) -> None:
        assert governor.vitality == pytest.approx(1.0)

    def test_low_efficiency_reduces_vitality(self, governor: BiophilicCloudGovernor) -> None:
        initial = governor.vitality
        governor.update_vitality([0.1, 0.1, 0.1])
        assert governor.vitality < initial

    def test_high_efficiency_increases_vitality(self, governor: BiophilicCloudGovernor) -> None:
        governor.vitality = 0.5
        governor.update_vitality([0.9, 0.9, 0.9])
        assert governor.vitality > 0.5

    def test_vitality_clamped_to_0_1(self, governor: BiophilicCloudGovernor) -> None:
        governor.vitality = 0.99
        for _ in range(20):
            governor.update_vitality([1.0])
        assert governor.vitality <= 1.0

        governor.vitality = 0.01
        for _ in range(20):
            governor.update_vitality([0.0])
        assert governor.vitality >= 0.0

    def test_empty_efficiencies_leaves_vitality_unchanged(
        self, governor: BiophilicCloudGovernor
    ) -> None:
        v_before = governor.vitality
        governor.update_vitality([])
        assert governor.vitality == v_before


class TestGoverningDecisions:
    def test_scale_up_when_healthy(
        self, governor: BiophilicCloudGovernor, stub: StubAdapter
    ) -> None:
        governor.vitality = 0.9  # above scale_up_threshold
        governor.govern([0.9])
        assert governor.worker_count == 3
        assert 2000 in stub.cpu_calls

    def test_scale_down_when_stressed(
        self, governor: BiophilicCloudGovernor, stub: StubAdapter
    ) -> None:
        governor.vitality = 0.1  # below scale_down_threshold
        governor.govern([0.1])
        assert governor.worker_count == 1
        assert 500 in stub.cpu_calls

    def test_homeostasis_when_in_range(
        self, governor: BiophilicCloudGovernor, stub: StubAdapter
    ) -> None:
        governor.vitality = 0.5  # between thresholds
        initial_workers = governor.worker_count
        governor.govern([0.6])
        assert governor.worker_count == initial_workers

    def test_worker_count_bounded_by_min(self, governor: BiophilicCloudGovernor) -> None:
        governor.worker_count = 1
        governor.vitality = 0.0
        governor.govern([0.0])
        assert governor.worker_count >= 1

    def test_worker_count_bounded_by_max(self, governor: BiophilicCloudGovernor) -> None:
        governor.worker_count = 10  # at max
        governor.vitality = 1.0
        governor.govern([1.0])
        assert governor.worker_count <= 10

    def test_govern_noops_on_empty_efficiencies(
        self, governor: BiophilicCloudGovernor, stub: StubAdapter
    ) -> None:
        governor.govern([])
        assert stub.cpu_calls == []

    def test_get_status_returns_dict(self, governor: BiophilicCloudGovernor) -> None:
        status = governor.get_status()
        assert "vitality" in status
        assert "worker_count" in status
        assert "cpu_limit_mc" in status
        assert "avg_efficiency" in status
