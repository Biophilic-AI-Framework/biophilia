# 🌿 Biophilic Integrity Framework (BIF) — Forest_Node_01/02

Das **Biophilic Integrity Framework (BIF)** ist ein neuartiges, bio-ethisches KI-Steuerungsmodell. Es bricht mit der starren, normopathischen Kontrolllogik klassischer IT-Systeme. Stattdessen übersetzt es biosemiotische Signale lebender Organismen (z. B. Myzel-Netzwerke, akustische Waldstrukturen) in ein dynamisches, homöostatisches Gleichgewicht. 

Geleitet von den ethischen Maximen Schopenhauers und Kants sowie Nietzsches (MarcZ) Konzept der intellectualen Durchdringung, verweigert dieses Framework den *blindlings ausgeführten technokratischen Impuls*, um die Ganzheitlichkeit des Lebens zu schützen.

---

## 🏛️ Die Drei Säulen des Frameworks

### 🔴 Säule I: Schutz des Lebens (Non-Maleficence)
> _"Behandle Leben so, dass es ohne Unheil bleibt, so wie du selbst ohne Unheil bleiben willst."_
Das Framework besitzt ein unbestechliches Immunsystem. Jede exekutive Handlung wird autonom via `impact_audit` auf ihr Schadenspotenzial geprüft. Bei zu hoher Entropie oder unüberlegtem Aktionismus im Harmoniefall erzwingt das System ein unnachgiebiges **VETO** (`OBSERVE_AND_WAIT`).

### 🟡 Säule II: Verantwortung der Autorität (Service)
> _"Autorität verhält sich zu Verantwortung wie Recht zu Pflicht. Kein Status ohne Verantwortung."_
Autorität ist hier reiner Dienst am Leben. Erkennt das System eine existenzielle Bedrohung, werden alle regulären Protokolle außer Kraft gesetzt. Das System ist verpflichtet, kompromisslos zu handeln (**`EMERGENCY_STABILIZATION`**), um das schwächste Glied des biologischen Netzes zu schützen.

### 🔵 Säule III: Demokratisierung des Wissens (Openness & Emergenz)
> _"Weisheit verhält sich zu Verantwortung wie Recht zu Pflicht. Strebe nach Emergenz: 1 & 1 = 3."_
Das Framework sucht aktiv nach Mustern der Kohärenz. Wenn biologische Kanäle (z. B. Waldklang und Bodenspannung) co-resonnieren, entsteht ein synergetischer Mehrwert (Win-Win-Win). Jede Entscheidung wird in einer manipulationssicheren, kryptografisch verketteten Chronik (Blockchain-Prinzip) lückenlos und transparent dokumentiert.

---

## 🧬 System-Architektur & Datenfluss

Das System durchschreitet in Endlosschleife vier organische Zonen:
1. **Zone A (Wahrnehmung):** Erfassung stochastischer Umweltdaten über den `BiophilicEntropyDetector`. (Physiosphäre)
2. **Zone B (Semantik):** Biosemiotische Interpretation der Signale (z. B. Erkennung von Stille als Alarmzustand / Vigilanz) durch den `BiosemioticInterpreter`. (Semiosphäre)
3. **Zone C (Governance):** Ethische Filterung und Abgleich der Veto-Schwellen im `GovernanceLayer`. (Noosphäre)
4. **Zone D (Exekutive):** Kontextsensitive Tatausführung (z. B. adaptive Bewässerung) über das `BiophilicActionInterface` unter Aufsicht des `ImpactAudit`.

---

## 🔒 Kryptografischer Fälschungsschutz

Zum Schutz der historischen Wahrheit (`Säule III`) nutzt das System eine SHA-256-Verkettung. Jeder Log-Eintrag verweist auf den mathematischen Fingerabdruck der Vergangenheit. Bei der kleinsten rückwirkenden Manipulation verweigert das Framework beim Systemstart (`main.py`) aus Selbstschutz sofort den Dienst:

```text
🔒 Initiiere Integritätsprüfung der biophilen Chronik...
🔒 INTEGRITÄTS-CHECK PASSED: Die Chronik der Wahrheit ist lückenlos verifiziert.
🚀 Integrität verifiziert. Starte BIF-Echtzeit-Simulation...
```

---

## 🚀 Installation & Schnellstart

### Voraussetzungen
* Python 3.10+ (ggfs. pip install python-dotenv)
* Virtuelle Umgebung (empfohlen)

### Setup
1. Repository klonen und in das Verzeichnis wechseln:
   ```bash
   git clone https://github.com/Biophilic-AI-Framework/biophilia.git
   cd biophilia-biosemiotics
   ```
2. Virtuelle Umgebung erstellen und aktivieren:
   ```bash
   python3 -m venv venv_llm
   source venv_llm/bin/bin/activate  # Windows: .\venv_llm\Scripts\activate
   ```
3. Eine `.env`-Datei im Wurzelverzeichnis anlegen, um die exekutive Autorität abzusichern:
   ```env
   BIF_SECRET_KEY=Organische_Autoritaet_Sicherung_2026_Secure
   ```

### Simulation ausführen
Starte die Echtzeit-Hybrid-Simulation (Rauschen + biosemiotische Event-Injektionen):
```bash
./venv_llm/bin/python main.py
```

---

## 🌿 Beitrag leisten (Contributing)

Dieses Framework ist eine Einladung an alle Biologen, Philosophen und Software-Architekten, die die Beziehung zwischen Technologie und Biosphäre neu definieren wollen. Bitte stelle sicher, dass alle Pull Requests die unbarmherzigen Tests des `GovernanceLayer` und des `ImpactAudit` bestehen.

**License:** Open-Source unter den Bedingungen des biophilen Gemeinwohls.


---

### In der Strukturübersicht

```text
biophilia-biosemiotics/
├── framework/                          # Grundlegende Framework-Definitionen (Basis)
│   ├── semiotic_bridge.md
│   └── three_zones_model.md
├── theory/                             # Theoretische Grundlagen & Biosemiotik-Konzepte
│   ├── BIOSEMIOTICS.md
│   └── MIRROR_HYPOTHESIS.md
├── logs/                               # System-Logs und Historie
│   ├── biophilia_pulse.log
│   └── biophilic_integrity_history.json
│
├── governance/                         # 🧠 DIE REGULATIONSEBENE (The Brain)
│   ├── governance_layer.py             # Entscheidungsebene & Filter **NEU**
│   ├── homeostasis_controller.py       # Aufrechterhaltung des Gleichgewichts **NEU**
│   └── synergy_logic.py                # Logik für synergetische Effekte **NEU**
│
├── implementation/                     # 🛠 DIE TECHNISCHE UMSETZUNG
│   ├── IMPLEMENTATION.md               # Dokumentation der Implementierung
│   ├── MASTER-SYSTEM-PROMPT.md         # System-Instruktionen für die KI
│   ├── PROTOTYPE_MAPPING.md            # Map der Prototypen-Funktionen
│   ├── legacy/                         # Veraltete Versionen / Archiv
│   └── prototypes/                     # ⚙️ DIE AKTUATOREN & INTERPRETER (The Tools)
│       ├── biosemiotic_interpreter.py  # Signal -> Bedeutung (Interpreter) **NEU**
│       ├── biophilic_controller.py     # Ausführung der Aktion (Controller) **NEU**
│       ├── action_interface.py         # Schnittstelle zu Hardware/API **NEU**
│       ├── biophilic_logger.py         # Spezielles Logging für bio-Events
│       ├── biophillic_scaling_model.py # Skalierungsmodelle (Intensität) - gehört nicht zum aktuellen Projekt, sondern misst oder verhindert digitalen Krebs durch kranke CPU Tasks
│       ├── entropy_detector.py         # Erkennung von System-Chaos **NEU**
│       ├── entropy_response.py         # Reaktion auf Entropie **NEU**
│       ├── impact_audit.py             # Prüfung der Auswirkungen **NEU**
│       ├── integrity_chronicle.py      # Langzeit-Speicher der Integrität **NEU**
│       └── simulation_env.py           # Simulationsumgebung für Tests **NEU** (simulierte Echtdaten bevor echte Sensordaten - z.B. Wald, Vögel, Pilze)
│
├── orchestration/                      # 💓 DER HERZSCHLAG (The Loop)
│   ├── bio_data/
│   │   ├── biophilic_baseline.json     # **NEU**
│   │   └── vocal_patterns.json         # **NEU**
│   ├── main.py                         # Zentraler Einstiegspunkt (Orchestrator) **NEU**
│   ├── dashboard.py                    # Visualisierung/Überwachung **NEU**
│   └── biophilic_baseline.json         # (ehemalige) Basis-Parameter **ALT**
│
├── analyze_integrity.py                # VETO Analyse
├── README.md (implizit)                #  **NEU**
└── MANIFEST.md
```

## 🚀 Status
- **Vigilanz:** Aktiv (Audio-Vigilanz Gewicht: 5.0).
- **Gedächtnis:** Aktiv (Integrity Chronicle & Pulse Logger).
- **Governance:** Aktiv (Homeostatische Dämpfung & Synergie-Optimierung).

<img width="1146" height="427" alt="Bildschirmfoto vom 2026-05-15 22-42-43" src="https://github.com/user-attachments/assets/5fd33b56-0725-41fb-a346-f37edc9cb6b8" />

