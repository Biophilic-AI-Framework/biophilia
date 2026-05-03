"""
Biophilic Cloud Governor - Adaptive Resource Management System

Ein biologisch inspiriertes Ressourcen-Management-System, das die Systemlast
durch kontinuierliche Vitalitätsmessung reguliert und adaptive Skalierung durchführt.

Autor: Claude Haiku 4.5
Lizenz: MIT
"""

import multiprocessing as mp
import time
import random
import logging
from abc import ABC, abstractmethod
from typing import List

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ==========================================
# 1. CLOUD API ADAPTER (Interface)
# ==========================================
class CloudResourceManager(ABC):
    """Abstraktion für Cloud-APIs wie Kubernetes oder AWS."""

    @abstractmethod
    def update_cpu_limit(self, limit_milli_cpu: int) -> None:
        """Aktualisiert die CPU-Limitierung."""
        pass

    @abstractmethod
    def scale_instances(self, count: int) -> None:
        """Skaliert die Anzahl der Instanzen."""
        pass


class KubernetesAdapter(CloudResourceManager):
    """Konkrete Implementierung für Kubernetes (Simuliert)."""

    def update_cpu_limit(self, limit_milli_cpu: int) -> None:
        """Simuliert K8s CPU-Limit-Update."""
        logger.info(f"[K8S API] Setting CPU Limit to {limit_milli_cpu}m")
        # In Produktion: requests.patch() an K8s API

    def scale_instances(self, count: int) -> None:
        """Simuliert K8s Deployment-Skalierung."""
        logger.info(f"[K8S API] Scaling Deployment to {count} replicas")
        # In Produktion: requests.patch() an K8s API


# ==========================================
# 2. BIOPHILIC WORKER
# ==========================================
def worker_task(task_queue: mp.Queue, result_queue: mp.Queue) -> None:
    """
    Ein Worker-Prozess, der Aufgaben verarbeitet und seine Effizienz meldet.

    Args:
        task_queue: Queue für eingehende Aufgaben
        result_queue: Queue für Effizienz-Messwerte
    """
    while True:
        task = task_queue.get()
        
        # Sentinel-Wert für sauberes Beenden
        if task is None:
            break

        start_time = time.time()
        
        # Simuliere Arbeit mit variabler Last (Rauschen/Stress)
        work_load = random.uniform(0.1, 1.0)
        time.sleep(work_load)
        
        end_time = time.time()
        actual_time = end_time - start_time
        
        # Effizienz: investierte Arbeit / tatsächliche Zeit
        efficiency = work_load / actual_time if actual_time > 0 else 0
        result_queue.put(efficiency)


# ==========================================
# 3. BIOPHILIC CLOUD GOVERNOR
# ==========================================
class BiophilicCloudGovernor:
    """
    Adaptive Ressourcen-Manager mit biologisch inspirierten Regelkreisen.
    
    Die "Vitalität" des Systems sinkt unter Last und erholt sich in Ruhe,
    ähnlich wie ein lebender Organismus.
    """

    # Konfigurierbare Schwellwerte
    SCALE_UP_THRESHOLD = 0.8
    SCALE_DOWN_THRESHOLD = 0.3
    MAX_WORKERS = 10
    MIN_WORKERS = 1
    VITALITY_DECAY = 0.1  # Senkung bei niedriger Effizienz
    VITALITY_RECOVERY = 0.05  # Steigerung bei hoher Effizienz
    EFFICIENCY_THRESHOLD = 0.5

    def __init__(self, cloud_adapter: CloudResourceManager):
        """
        Initialisiert den Governor.

        Args:
            cloud_adapter: CloudResourceManager-Instanz für API-Aufrufe
        """
        self.adapter = cloud_adapter
        self.vitality = 1.0
        self.worker_count = 2
        self.cpu_limit = 1000  # milli-cpu
        self.vitality_history: List[float] = []
        self.efficiency_history: List[float] = []

    def calculate_vitality(self, efficiencies: List[float]) -> float:
        """
        Berechnet die Systemvitalität basierend auf Durchschnitts-Effizienz.

        Biologisches Modell:
        - Niedrige Effizienz = Stress → Vitalität sinkt
        - Hohe Effizienz = Erholung → Vitalität steigt
        
        Args:
            efficiencies: Liste der Worker-Effizienzwerte
            
        Returns:
            Neue Vitalität (0.0 bis 1.0)
        """
        if not efficiencies:
            return self.vitality

        avg_eff = sum(efficiencies) / len(efficiencies)
        self.efficiency_history.append(avg_eff)

        if avg_eff < self.EFFICIENCY_THRESHOLD:
            self.vitality -= self.VITALITY_DECAY
        else:
            self.vitality += self.VITALITY_RECOVERY

        # Normalisieren auf [0, 1]
        self.vitality = max(0.0, min(1.0, self.vitality))
        self.vitality_history.append(self.vitality)

        return self.vitality

    def govern(self, efficiencies: List[float]) -> None:
        """
        Entscheidungslogik: Berechnet Vitalität und passt Ressourcen an.

        Args:
            efficiencies: Liste der Worker-Effizienzwerte aus diesem Zyklus
        """
        if not efficiencies:
            logger.warning("Keine Effizienzwerte vorhanden")
            return

        v = self.calculate_vitality(efficiencies)
        avg_eff = sum(efficiencies) / len(efficiencies)

        logger.info(
            f"Vitality: {v:.2f} | Avg Efficiency: {avg_eff:.2f} | "
            f"Workers: {self.worker_count}"
        )

        # Entscheidungsbaum
        if v > self.SCALE_UP_THRESHOLD and self.worker_count < self.MAX_WORKERS:
            logger.info("✅ System healthy - scaling up")
            self.worker_count += 1
            self.cpu_limit = 2000
        elif v < self.SCALE_DOWN_THRESHOLD:
            logger.warning("⚠️ System under stress - scaling down")
            self.worker_count = max(self.MIN_WORKERS, self.worker_count - 1)
            self.cpu_limit = 500
        else:
            logger.info("⚖️ System in homeostasis")
            self.cpu_limit = 1000

        # Anwendung der Entscheidung via Cloud-API
        self.adapter.update_cpu_limit(self.cpu_limit)
        self.adapter.scale_instances(self.worker_count)

    def get_status(self) -> dict:
        """Gibt aktuellen Systemstatus zurück."""
        return {
            "vitality": self.vitality,
            "worker_count": self.worker_count,
            "cpu_limit": self.cpu_limit,
            "avg_efficiency": (
                sum(self.efficiency_history) / len(self.efficiency_history)
                if self.efficiency_history else 0
            )
        }


# ==========================================
# 4. WORKER MANAGEMENT UTILITIES
# ==========================================
def sync_worker_processes(
    workers: List[mp.Process],
    target_count: int,
    task_queue: mp.Queue,
    result_queue: mp.Queue
) -> List[mp.Process]:
    """
    Synchronisiert die Anzahl der laufenden Worker-Prozesse.

    Args:
        workers: Liste der aktuellen Worker-Prozesse
        target_count: Zielanzahl von Workern
        task_queue: Queue für Task-Verteilung
        result_queue: Queue für Ergebnis-Sammlung
        
    Returns:
        Aktualisierte Worker-Liste
    """
    current_count = len(workers)

    if current_count < target_count:
        # Worker starten
        for _ in range(target_count - current_count):
            p = mp.Process(
                target=worker_task,
                args=(task_queue, result_queue)
            )
            p.start()
            workers.append(p)
            logger.debug(f"Started worker process (PID: {p.pid})")

    elif current_count > target_count:
        # Worker beenden
        for _ in range(current_count - target_count):
            p = workers.pop()
            p.terminate()
            p.join(timeout=5)
            if p.is_alive():
                p.kill()
            logger.debug(f"Terminated worker process (PID: {p.pid})")

    return workers


def cleanup_workers(
    workers: List[mp.Process],
    task_queue: mp.Queue
) -> None:
    """
    Beendet alle Worker-Prozesse ordnungsgemäß.

    Args:
        workers: Liste der Worker-Prozesse
        task_queue: Queue für Sentinels
    """
    logger.info("Initiating graceful shutdown...")

    # Sentinels senden für sauberes Beenden
    for _ in range(len(workers)):
        task_queue.put(None)

    time.sleep(1)

    # Auf Beendigung warten
    for p in workers:
        p.join(timeout=5)
        if p.is_alive():
            logger.warning(f"Force-killing worker (PID: {p.pid})")
            p.kill()

    logger.info("All workers terminated")


# ==========================================
# 5. MAIN SIMULATION
# ==========================================
def main():
    """Hauptprogramm: Führt die Simulation durch."""
    logger.info("Starting Biophilic Cloud Governor Simulation")

    # Setup
    cloud_api = KubernetesAdapter()
    governor = BiophilicCloudGovernor(cloud_api)

    task_queue = mp.Queue()
    result_queue = mp.Queue()

    # Starte initiale Worker
    workers = []
    for _ in range(governor.worker_count):
        p = mp.Process(target=worker_task, args=(task_queue, result_queue))
        p.start()
        workers.append(p)

    logger.info(f"Started {len(workers)} worker processes")

    try:
        # Simulationszyklus
        num_cycles = 10
        tasks_per_cycle = 5

        for cycle in range(num_cycles):
            logger.info(f"\n--- Cycle {cycle + 1}/{num_cycles} ---")

            # Tasks in Queue einqueuen
            for _ in range(tasks_per_cycle * len(workers)):
                task_queue.put("task")

            # Zeit für Verarbeitung
            time.sleep(2)

            # Alle Ergebnisse sammeln
            efficiencies = []
            while not result_queue.empty():
                try:
                    efficiencies.append(result_queue.get_nowait())
                except:
                    break

            # Governor-Entscheidung
            governor.govern(efficiencies)

            # Worker-Anzahl synchronisieren
            workers = sync_worker_processes(
                workers,
                governor.worker_count,
                task_queue,
                result_queue
            )

            # Status ausgeben
            status = governor.get_status()
            logger.debug(f"Status: {status}")

            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Interrupted by user")

    finally:
        # Ordnungsgemäßes Beenden
        cleanup_workers(workers, task_queue)
        logger.info("Simulation completed")


if __name__ == "__main__":
    main()
