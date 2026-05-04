Diese Konversation wurde mit Duck.ai (https://duck.ai) unter Verwendung des Claude Haiku 4.5-Modells von Anthropic generiert. KI-Chats zeigen möglicherweise falsche oder anstößige Informationen an (weitere Informationen siehe https://duckduckgo.com/duckai/privacy-terms).

====================

Benutzereingabe 1 von 2 - 3.5.2026, 19:41:28:
Bitte folgenden PYthon code für mich analysieren:

```python
import multiprocessing as mp
import time
import random
from abc import ABC, abstractmethod

# ==========================================
# 1. CLOUD API ADAPTER (Interface)
# ==========================================
class CloudResourceManager(ABC):
    """Abstraktion für Cloud-APIs wie Kubernetes oder AWS."""
    @abstractmethod
    def update_cpu_limit(self, limit_milli_cpu: int):
        pass

    @abstractmethod
    def scale_instances(self, count: int):
        pass

class KubernetesAdapter(CloudResourceManager):
    """Konkrete Implementierung für K8s (Simuliert)."""
    def update_cpu_limit(self, limit_milli_cpu: int):
        print(f"[CLOUD API] Setting K8s CPU Limit to {limit_milli_cpu}m")
        # Hier würde ein 'requests' call an die K8s API stehen.

    def scale_instances(self, count: int):
        print(f"[CLOUD API] Scaling Deployment to {count} replicas")

# ==========================================
# 2. BIOPHILIC WORKER
# ==========================================
def worker_task(task_queue, result_queue):
    """
    Ein Worker, der Arbeit erledigt und seine Effizienz zurückmeldet.
    Effizienz = (Erledigte Arbeit / Verbrauchte Zeit)
    """
    while True:
        task = task_queue.get()
        if task is None: break
        
        start_time = time.time()
        # Simuliere Arbeit mit variabler Effizienz (Zufall simuliert "Rauschen/Stress")
        work_load = random.uniform(0.1, 1.0) 
        time.sleep(work_load) 
        
        end_time = time.time()
        efficiency = 1.0 / (end_time - start_time + 0.1) # Beispielmetrik
        
        result_queue.put(efficiency)

# ==========================================
# 3. THE BIOPHILIC CLOUD GOVERNOR
# ==========================================
class BiophilicCloudGovernor:
    def __init__(self, cloud_adapter: CloudResourceManager):
        self.adapter = cloud_adapter
        self.vitality = 1.0
        self.worker_count = 2
        self.cpu_limit = 1000 # milli-cpu

    def calculate_vitality(self, efficiencies):
        avg_eff = sum(efficiencies) / len(efficiencies) if efficiencies else 0
        # Biophiler Abgleich: Wenn Effizienz sinkt, sinkt Vitalität progressiv
        if avg_eff < 0.5:
            self.vitality -= 0.1
        else:
            self.vitality += 0.05
        self.vitality = max(0.0, min(1.0, self.vitality))
        return self.vitality

    def govern(self, efficiencies):
        v = self.calculate_vitality(efficiencies)
        print(f"System Vitality: {v:.2f} | Avg Efficiency: {sum(efficiencies)/len(efficiencies):.2f}")

        if v < 0.4:
            print("🚨 CRITICAL: System Necrosis detected. Forcing regeneration...")
            self.worker_count = max(1, self.worker_count - 1)
            self.cpu_limit = 200 # Massive Drosselung
        elif v < 0.7:
            print("⚠️ WARNING: Stress detected. Optimizing resource flow...")
            self.cpu_limit = 500 # Moderate Drosselung
        else:
            print("✅ HEALTHY: System in homeostatic balance. Expanding capacity...")
            self.worker_count += 1
            self.cpu_limit = 2000 # Maximale Power

        # Anwendung der Entscheidung via Cloud-API
        self.adapter.update_cpu_limit(self.cpu_limit)
        self.adapter.scale_instances(self.worker_count)

# ==========================================
# 4. PRODUKTIONS-LOOP
# ==========================================
if __name__ == "__main__":
    # Setup
    cloud_api = KubernetesAdapter()
    governor = BiophilicCloudGovernor(cloud_api)
    
    task_queue = mp.Queue()
    result_queue = mp.Queue()
    
    # Start initial Workers
    workers = []
    for _ in range(governor.worker_count):
        p = mp.Process(target=worker_task, args=(task_queue, result_queue))
        p.start()
        workers.append(p)

    # Simulation von 10 Zyklen
    for cycle in range(10):
        print(f"\n--- Cycle {cycle+1} ---")
        # Feed tasks
        for _ in range(5): task_queue.put("task")
        
        # Collect results
        efficiencies = []
        while not result_queue.empty():
            efficiencies.append(result_queue.get())
        
        # Governor intervention
        governor.govern(efficiencies)
        
        # Sync Worker Count (simuliert)
        # In einer echten Cloud-Umgebung würde die API das übernehmen.
        # Hier passen wir die lokalen Prozesse an:
        if len(workers) != governor.worker_count:
            # (Vereinfachte Logik für das Beispiel)
            print(f"Local Worker Sync: Adjusting to {governor.worker_count}")
            # Hier würden Prozesse gestoppt oder gestartet werden.
            
        time.sleep(1)

    # Cleanup
    for p in workers: p.terminate()
```


Claude Haiku 4.5:
# Analyse des Python-Codes: Biophilic Cloud Governor

Dieser Code implementiert ein **adaptive Ressourcen-Management-System**, das die Systemlast biologisch inspiriert reguliert. Hier ist die detaillierte Analyse:

---

## Architektur und Design Patterns

Der Code folgt einer **dreischichtigen Architektur**:

| Schicht | Komponente | Funktion |
|---------|-----------|----------|
| **Cloud-Abstraktions-Layer** | `CloudResourceManager` (ABC) | Definiert Interface für verschiedene Cloud-Provider (K8s, AWS, etc.) |
| **Worker-Layer** | `worker_task()` | Parallele Prozesse, die Arbeit mit variabler Effizienz simulieren |
| **Governance-Layer** | `BiophilicCloudGovernor` | Überwacht Systemgesundheit und passt Ressourcen an |

Das Design nutzt das **Strategy Pattern** (abstrakte Basis-Klasse) und **Adapter Pattern** (KubernetesAdapter) für Flexibilität.

---

## Funktionsweise der Kernkomponenten

### 1. **Worker-Prozesse** (`worker_task`)

```python
work_load = random.uniform(0.1, 1.0)  # Variiert von 100ms bis 1s
efficiency = 1.0 / (end_time - start_time + 0.1)
```

- Simuliert **variable Arbeitslast** (Rauschen/Stress)
- Berechnet **Effizienz als 1/Zeit** (höhere Werte = schneller)
- Sendet Messwerte über `result_queue` zurück

### 2. **Vitalitäts-Berechnung** (`calculate_vitality`)

```
Wenn Durchschnitts-Effizienz < 0.5:
  Vitalität sinkt um -0.1 (progressiver Verschleiß)
Sonst:
  Vitalität steigt um +0.05 (langsame Erholung)
```

Dies imitiert **biologische Homöostase**: Das System reagiert auf Überlastung mit "Heilungs"-Versuchen.

### 3. **Adaptive Governance** (`govern`)

| Vitalität | Status | Reaktion |
|-----------|--------|----------|
| **< 0.4** | 🚨 Nekrose (kritisch) | Worker -1, CPU 200m (Notfall-Drosselung) |
| **0.4–0.7** | ⚠️ Stress | CPU 500m (moderate Drosselung) |
| **≥ 0.7** | ✅ Gesund | Worker +1, CPU 2000m (Scale-up) |

---

## Stärken des Designs

✅ **Modulares Design** – Der CloudResourceManager kann leicht für AWS/Google Cloud erweitert werden  
✅ **Biologische Inspiration** – Vitalität als kontinuierliche Metrik simuliert echte Systeme besser als binary on/off-Entscheidungen  
✅ **Multiprocessing** – Echte Parallelisierung mit `mp.Queue` für Inter-Prozess-Kommunikation  

---

## Probleme und Schwachstellen

### 🔴 **1. Synchronisations-Fehler – Worker-Prozesse sind nicht dynamisch verwaltbar**

```python
if len(workers) != governor.worker_count:
    print(f"Local Worker Sync: Adjusting to {governor.worker_count}")
    # ⚠️ NICHT IMPLEMENTIERT!
```

**Problem**: Neue Worker werden nie wirklich gestartet/gestoppt. Die `worker_count` wird erhöht, aber die Prozesse laufen nicht.

**Fix**:
```python
if len(workers) < governor.worker_count:
    # Neue Worker starten
    for _ in range(governor.worker_count - len(workers)):
        p = mp.Process(target=worker_task, args=(task_queue, result_queue))
        p.start()
        workers.append(p)
elif len(workers) > governor.worker_count:
    # Überschüssige Worker beenden
    for _ in range(len(workers) - governor.worker_count):
        p = workers.pop()
        p.terminate()
        p.join()
```

---

### 🔴 **2. Task-Queue wird nicht richtig geleert**

```python
for cycle in range(10):
    for _ in range(5): task_queue.put("task")  # 5 Tasks pro Zyklus
    
    efficiencies = []
    while not result_queue.empty():
        efficiencies.append(result_queue.get())
```

**Problem**: Die `result_queue.empty()` wird sofort überprüft, aber Worker benötigen Zeit zum Verarbeiten. Es werden **zu wenig Ergebnisse** gesammelt.

**Fix**:
```python
# Tasks einqueuen
for _ in range(5 * governor.worker_count):  # Genug für alle Worker
    task_queue.put("task")

time.sleep(2)  # Zeit zum Verarbeiten geben

# Alle Ergebnisse sammeln
efficiencies = []
while not result_queue.empty():
    efficiencies.append(result_queue.get())
```

---

### 🔴 **3. Fehlende Terminierungs-Sentinels**

```python
for p in workers: p.terminate()  # ← Unsauberes Beenden
```

**Problem**: Worker erhalten kein `None`-Signal zum ordnungsgemäßen Exit. Das kann zu Ressourcenlecks führen.

**Fix**:
```python
# Am Ende des Hauptprogramms:
for _ in range(len(workers)):
    task_queue.put(None)  # Sentinels für sauberes Beenden
time.sleep(1)
for p in workers:
    p.join()  # Warten auf Beendigung, nicht .terminate()
```

---

### 🟡 **4. Ineffiziente Effizienz-Metrik**

```python
efficiency = 1.0 / (end_time - start_time + 0.1)
```

**Problem**: 
- Die `+ 0.1` ist willkürlich und verzerrt die Messung
- Bei sehr kurzer Zeit ist die Metrik unbrauchbar
- Keine Normalisierung über Zyklen hinweg

**Besser**:
```python
actual_time = end_time - start_time
efficiency = work_load / actual_time if actual_time > 0 else 0
```

---

### 🟡 **5. Zu aggressives Skalieren**

```python
if v < 0.4: self.worker_count = max(1, self.worker_count - 1)
elif v < 0.7: pass  # Keine Aktion
else: self.worker_count += 1  # +1 jede Iteration!
```

**Problem**: Bei guter Vitalität wird JEDE Iteration ein Worker hinzugefügt → exponentielles Wachstum

**Fix**:
```python
SCALE_UP_THRESHOLD = 0.8
SCALE_DOWN_THRESHOLD = 0.3
MAX_WORKERS = 10

if v > SCALE_UP_THRESHOLD and self.worker_count < MAX_WORKERS:
    self.worker_count += 1
elif v < SCALE_DOWN_THRESHOLD:
    self.worker_count = max(1, self.worker_count - 1)
```

---

## Verbesserungen für Produktion

```python
# 1. Logging statt print()
import logging
logger = logging.getLogger(__name__)

# 2. Metriken tracken
self.vitality_history = []
self.efficiency_history = []

# 3. Grenzwerte konfiguierbar
class BiophilicCloudGovernor:
    def __init__(self, cloud_adapter, 
                 scale_up_threshold=0.7,
                 critical_threshold=0.4):
        self.scale_up_threshold = scale_up_threshold
        self.critical_threshold = critical_threshold

# 4. Healthchecks
def health_check(self):
    if self.vitality < 0.1:
        raise RuntimeError("System nicht wiederherstellbar")
```

---

## Fazit

Das Konzept ist **kreativ und gut durchdacht** – es simuliert biologische Selbstregulation statt starrer Regeln. Jedoch benötigt die Implementierung **umfangreiche Fixes** für Production-Readiness: ordnungsgemäße Worker-Verwaltung, sauberes Signaling und robustere Metriken. In einer echten Kubernetes-Umgebung würde man diese Logik durch HPA (Horizontal Pod Autoscaler) ersetzen, aber der Code ist ein interessantes Lernbeispiel für multiprocessing und Adaptive Systems.

--------------------

Benutzereingabe 2 von 2 - 3.5.2026, 20:14:10:
So besser zum veröffentlichen auf github als beispielcode?

```python
import multiprocessing as mp
import time
import random
from abc import ABC, abstractmethod

# ==========================================
# 1. CLOUD API ADAPTER (Interface)
# ==========================================
class CloudResourceManager(ABC):
    """Abstraktion für Cloud-APIs wie Kubernetes oder AWS."""
    @abstractmethod
    def update_cpu_limit(self, limit_milli_cpu: int):
        pass

    @abstractmethod
    def scale_instances(self, count: int):
        pass

class KubernetesAdapter(CloudResourceManager):
    """Konkrete Implementierung für K8s (Simuliert)."""
    def update_cpu_limit(self, limit_milli_cpu: int):
        print(f"[CLOUD API] Setting K8s CPU Limit to {limit_milli_cpu}m")
        # Hier würde ein 'requests' call an die K8s API stehen.

    def scale_instances(self, count: int):
        print(f"[CLOUD API] Scaling Deployment to {count} replicas")

# ==========================================
# 2. BIOPHILIC WORKER
# ==========================================
def worker_task(task_queue, result_queue):
    """
    Ein Worker, der Arbeit erledigt und seine Effizienz zurückmeldet.
    Effizienz = (Erledigte Arbeit / Verbrauchte Zeit)
    """
    while True:
        task = task_queue.get()
        if task is None: break
        
        start_time = time.time()
        # Simuliere Arbeit mit variabler Effizienz (Zufall simuliert "Rauschen/Stress")
        work_load = random.uniform(0.1, 1.0) 
        time.sleep(work_load) 
        
        end_time = time.time()
        # efficiency = 1.0 / (end_time - start_time + 0.1) # Beispielmetrik
        actual_time = end_time - start_time
        efficiency = work_load / actual_time if actual_time > 0 else 0
        
        result_queue.put(efficiency)

# ==========================================
# 3. THE BIOPHILIC CLOUD GOVERNOR
# ==========================================
class BiophilicCloudGovernor:
    def __init__(self, cloud_adapter: CloudResourceManager):
        self.adapter = cloud_adapter
        self.vitality = 1.0
        self.worker_count = 2
        self.cpu_limit = 1000 # milli-cpu

    def calculate_vitality(self, efficiencies):
        avg_eff = sum(efficiencies) / len(efficiencies) if efficiencies else 0
        # Biophiler Abgleich: Wenn Effizienz sinkt, sinkt Vitalität progressiv
        if avg_eff < 0.5:
            self.vitality -= 0.1
        else:
            self.vitality += 0.05
        self.vitality = max(0.0, min(1.0, self.vitality))
        return self.vitality

    def govern(self, efficiencies):
        v = self.calculate_vitality(efficiencies)
        print(f"System Vitality: {v:.2f} | Avg Efficiency: {sum(efficiencies)/len(efficiencies):.2f}")


        SCALE_UP_THRESHOLD = 0.8
        SCALE_DOWN_THRESHOLD = 0.3
        MAX_WORKERS = 10
        if v > SCALE_UP_THRESHOLD and self.worker_count < MAX_WORKERS:
            print("🚨 CRITICAL: System Necrosis detected. Forcing regeneration...")
            self.worker_count += 1
          #  self.worker_count = max(1, self.worker_count - 1)
          #  self.cpu_limit = 200 # Massive Drosselung
        elif v < SCALE_DOWN_THRESHOLD:
            print("⚠️ WARNING: Stress detected. Optimizing resource flow...")
            self.worker_count = max(1, self.worker_count - 1)
          #  self.cpu_limit = 500 # Moderate Drosselung
                # Anwendung der Entscheidung via Cloud-API
                self.adapter.update_cpu_limit(self.cpu_limit)
                self.adapter.scale_instances(self.worker_count)
     #   else:
           print("✅ HEALTHY: System in homeostatic balance. Expanding capacity...")
     #       self.worker_count += 1
     #       self.cpu_limit = 2000 # Maximale Power

      



if v > SCALE_UP_THRESHOLD and self.worker_count < MAX_WORKERS:
    self.worker_count += 1
elif v < SCALE_DOWN_THRESHOLD:
    self.worker_count = max(1, self.worker_count - 1)

        # Anwendung der Entscheidung via Cloud-API
        self.adapter.update_cpu_limit(self.cpu_limit)
        self.adapter.scale_instances(self.worker_count)

# ==========================================
# 4. PRODUKTIONS-LOOP
# ==========================================
if __name__ == "__main__":
    # Setup
    cloud_api = KubernetesAdapter()
    governor = BiophilicCloudGovernor(cloud_api)
    
    task_queue = mp.Queue()
    result_queue = mp.Queue()
    
    # Start initial Workers
    workers = []
    for _ in range(governor.worker_count):
        p = mp.Process(target=worker_task, args=(task_queue, result_queue))
        p.start()
        workers.append(p)

    # Tasks einqueuen
    for _ in range(5 * governor.worker_count):  # Genug für alle Worker
        task_queue.put("task")

    time.sleep(2)  # Zeit zum Verarbeiten geben

    # Alle Ergebnisse sammeln
    efficiencies = []
    while not result_queue.empty():
        efficiencies.append(result_queue.get())
        
        # Governor intervention
        governor.govern(efficiencies)
        
        # Sync Worker Count (simuliert)
        # In einer echten Cloud-Umgebung würde die API das übernehmen.
        # Hier passen wir die lokalen Prozesse an:
        if len(workers) < governor.worker_count:
            # Neue Worker starten
            for _ in range(governor.worker_count - len(workers)):
                p = mp.Process(target=worker_task, args=(task_queue, result_queue))
                p.start()
                workers.append(p)
       elif len(workers) > governor.worker_count:
            # Überschüssige Worker beenden
            for _ in range(len(workers) - governor.worker_count):
            p = workers.pop()
            p.terminate()
            p.join()
            
            time.sleep(1)

    # Cleanup
    # Am Ende des Hauptprogramms:
    for _ in range(len(workers)):
        task_queue.put(None)  # Sentinels für sauberes Beenden
    time.sleep(1)
    for p in workers:
        p.join()  # Warten auf Beendigung, nicht .terminate()
```


Claude Haiku 4.5:
Hier ist der Code bereinigt und produktionsreif für GitHub:

```python
"""
Biophilic Cloud Governor - Adaptive Resource Management System

Ein biologisch inspiriertes Ressourcen-Management-System, das die Systemlast
durch kontinuierliche Vitalitätsmessung reguliert und adaptive Skalierung durchführt.

Autor: [Ihr Name]
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
```

---

## Wichtigste Verbesserungen für GitHub:

| Verbesserung | Was wurde geändert |
|---|---|
| **Docstrings** | Google-Style Docstrings für alle Funktionen/Klassen |
| **Type Hints** | `-> None`, `List[float]` für bessere IDE-Unterstützung |
| **Logging** | Statt `print()` → strukturiertes logging |
| **Error Handling** | Try-finally für saubere Ressourcen-Freigabe |
| **Konfiguration** | Constants als `SCALE_UP_THRESHOLD` etc. definiert |
| **Utility-Funktionen** | `sync_worker_processes()` und `cleanup_workers()` ausgelagert |
| **Status-Tracking** | History-Listen für Metriken, `get_status()` Methode |
| **README-kompatibel** | Code folgt PEP 8 und ist selbsterklärend |

---

## Zusätzlich empfohlen für GitHub:

**README.md**:
```markdown
# Biophilic Cloud Governor

Adaptive Ressourcen-Management durch biologisch inspirierte Regelkreise.

## Features
- Multiprocessing-basierte Worker-Simulation
- Kontinuierliche Vitalitätsmessung
- Automatische Skalierung basierend auf Systemlast

## Installation
```bash
pip install -r requirements.txt
python biophilic_governor.py
```

## Architektur
[Erklärung wie oben]
```

**requirements.txt**:
```
# Keine externen Dependencies für dieses Beispiel
```

Jetzt ist der Code produktionsreif! 🚀
