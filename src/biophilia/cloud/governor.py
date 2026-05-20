"""
governor.py – Biophilic Cloud Governor: adaptive resource management.

A biologically-inspired resource manager that regulates system load through
continuous vitality measurement and adaptive scaling — analogous to how a
living organism conserves energy under stress and expands under abundance.

Original concept: Claude Haiku 4.5  |  Refactored to proper package structure.
"""

from __future__ import annotations

import logging
import multiprocessing as mp
import random
import time
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


# ── Cloud API abstraction ─────────────────────────────────────────────────────


class CloudResourceManager(ABC):
    """Abstract interface for cloud scaling APIs (Kubernetes, AWS, GCP, …)."""

    @abstractmethod
    def update_cpu_limit(self, limit_milli_cpu: int) -> None:
        """Update the CPU limit for the managed deployment."""

    @abstractmethod
    def scale_instances(self, count: int) -> None:
        """Scale the deployment to *count* replicas."""


class KubernetesAdapter(CloudResourceManager):
    """Simulated Kubernetes implementation (replace with real API calls in prod)."""

    def update_cpu_limit(self, limit_milli_cpu: int) -> None:
        logger.info("[K8S API] Setting CPU limit to %dm.", limit_milli_cpu)

    def scale_instances(self, count: int) -> None:
        logger.info("[K8S API] Scaling deployment to %d replica(s).", count)


# ── Worker ────────────────────────────────────────────────────────────────────


def worker_task(task_queue: mp.Queue[str | None], result_queue: mp.Queue[float]) -> None:
    """
    Subprocess entry point.  Drains *task_queue*, computes efficiency for each
    task, and posts the result to *result_queue*.  ``None`` is the sentinel.
    """
    while True:
        task = task_queue.get()
        if task is None:
            break

        t0 = time.time()
        workload = random.uniform(0.1, 1.0)
        time.sleep(workload)
        elapsed = time.time() - t0

        efficiency = workload / elapsed if elapsed > 0 else 0.0
        result_queue.put(efficiency)


# ── Governor ──────────────────────────────────────────────────────────────────


class BiophilicCloudGovernor:
    """
    Adaptive resource manager with biologically-inspired feedback loops.

    The "vitality" metric sinks under high load (low efficiency) and recovers
    during idle periods — mirroring an organism's energy budget.

    Parameters
    ----------
    cloud_adapter:
        A :class:`CloudResourceManager` instance used to apply decisions.
    scale_up_threshold:
        Vitality level above which the system scales up.
    scale_down_threshold:
        Vitality level below which the system scales down.
    max_workers / min_workers:
        Hard bounds on replica count.
    """

    def __init__(
        self,
        cloud_adapter: CloudResourceManager,
        *,
        scale_up_threshold: float = 0.8,
        scale_down_threshold: float = 0.3,
        max_workers: int = 10,
        min_workers: int = 1,
        vitality_decay: float = 0.1,
        vitality_recovery: float = 0.05,
        efficiency_threshold: float = 0.5,
    ) -> None:
        self.adapter = cloud_adapter
        self.scale_up_threshold = scale_up_threshold
        self.scale_down_threshold = scale_down_threshold
        self.max_workers = max_workers
        self.min_workers = min_workers
        self.vitality_decay = vitality_decay
        self.vitality_recovery = vitality_recovery
        self.efficiency_threshold = efficiency_threshold

        self.vitality: float = 1.0
        self.worker_count: int = 2
        self.cpu_limit: int = 1000  # milli-CPU

        self._vitality_history: list[float] = []
        self._efficiency_history: list[float] = []

    # ── Vitality model ────────────────────────────────────────────────────────

    def update_vitality(self, efficiencies: list[float]) -> float:
        """Recompute vitality from a batch of worker efficiency measurements."""
        if not efficiencies:
            return self.vitality

        avg_eff = sum(efficiencies) / len(efficiencies)
        self._efficiency_history.append(avg_eff)

        if avg_eff < self.efficiency_threshold:
            self.vitality -= self.vitality_decay
        else:
            self.vitality += self.vitality_recovery

        self.vitality = max(0.0, min(1.0, self.vitality))
        self._vitality_history.append(self.vitality)
        return self.vitality

    # ── Governance ────────────────────────────────────────────────────────────

    def govern(self, efficiencies: list[float]) -> None:
        """Compute vitality and apply the corresponding scaling decision."""
        if not efficiencies:
            logger.warning("No efficiency values available; skipping governance cycle.")
            return

        v = self.update_vitality(efficiencies)
        avg_eff = sum(efficiencies) / len(efficiencies)

        logger.info("Vitality=%.2f | AvgEff=%.2f | Workers=%d", v, avg_eff, self.worker_count)

        if v > self.scale_up_threshold and self.worker_count < self.max_workers:
            logger.info("System healthy — scaling up.")
            self.worker_count += 1
            self.cpu_limit = 2000
        elif v < self.scale_down_threshold:
            logger.warning("System under stress — scaling down.")
            self.worker_count = max(self.min_workers, self.worker_count - 1)
            self.cpu_limit = 500
        else:
            logger.info("System in homeostasis.")
            self.cpu_limit = 1000

        self.adapter.update_cpu_limit(self.cpu_limit)
        self.adapter.scale_instances(self.worker_count)

    def get_status(self) -> dict[str, float | int]:
        """Return a snapshot of the governor's current state."""
        return {
            "vitality": self.vitality,
            "worker_count": self.worker_count,
            "cpu_limit_mc": self.cpu_limit,
            "avg_efficiency": (
                sum(self._efficiency_history) / len(self._efficiency_history)
                if self._efficiency_history
                else 0.0
            ),
        }


# ── Worker management utilities ───────────────────────────────────────────────


def sync_workers(
    workers: list[mp.Process],
    target_count: int,
    task_queue: mp.Queue[str | None],
    result_queue: mp.Queue[float],
) -> list[mp.Process]:
    """Grow or shrink the worker-process pool to *target_count*."""
    while len(workers) < target_count:
        p = mp.Process(target=worker_task, args=(task_queue, result_queue))
        p.start()
        workers.append(p)
        logger.debug("Started worker PID=%d.", p.pid)

    while len(workers) > target_count:
        p = workers.pop()
        p.terminate()
        p.join(timeout=5)
        if p.is_alive():
            p.kill()
        logger.debug("Terminated worker PID=%d.", p.pid)

    return workers


def stop_workers(workers: list[mp.Process], task_queue: mp.Queue[str | None]) -> None:
    """Send sentinel values and wait for all workers to exit cleanly."""
    logger.info("Initiating graceful shutdown of %d worker(s)…", len(workers))
    for _ in workers:
        task_queue.put(None)
    time.sleep(1)
    for p in workers:
        p.join(timeout=5)
        if p.is_alive():
            logger.warning("Force-killing worker PID=%d.", p.pid)
            p.kill()
    logger.info("All workers terminated.")


# ── Standalone demo ───────────────────────────────────────────────────────────


def _demo_main() -> None:
    """Run a 10-cycle simulation against the KubernetesAdapter stub."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")
    logger.info("Starting Biophilic Cloud Governor demo.")

    adapter = KubernetesAdapter()
    governor = BiophilicCloudGovernor(adapter)
    task_q: mp.Queue[str | None] = mp.Queue()
    result_q: mp.Queue[float] = mp.Queue()

    workers: list[mp.Process] = []
    workers = sync_workers(workers, governor.worker_count, task_q, result_q)

    try:
        for cycle in range(10):
            logger.info("─── Cycle %d/10 ───", cycle + 1)
            for _ in range(5 * len(workers)):
                task_q.put("task")
            time.sleep(2)

            efficiencies: list[float] = []
            while not result_q.empty():
                try:
                    efficiencies.append(result_q.get_nowait())
                except Exception:
                    break

            governor.govern(efficiencies)
            workers = sync_workers(workers, governor.worker_count, task_q, result_q)
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
    finally:
        stop_workers(workers, task_q)
        logger.info("Demo completed.  Final status: %s", governor.get_status())


if __name__ == "__main__":
    _demo_main()
