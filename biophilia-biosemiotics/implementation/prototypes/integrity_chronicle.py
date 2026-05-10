import datetime
import json
import os

class IntegrityChronicle:
    def __init__(self, filename="biophilic_integrity_history.json"):
        # Speichert das Log im orchestration-Ordner für leichten Zugriff
        self.filename = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../orchestration', filename))

    def record_action(self, action_name: str, pillar: str, reason: str, synergy_score: float):
        """
        Säule III: Dokumentiert Handlungen im Kontext der biophilen Integrität.
        """
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "node": "Forest_Node_01",
            "action": action_name,
            "pillar_reference": pillar,
            "justification": reason,
            "synergy_index": synergy_score,
            "integrity_verified": True
        }

        history = []
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                try:
                    history = json.load(f)
                except json.JSONDecodeError: history = []

        history.append(entry)

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
            
        print(f"📖 Chronik: [{action_name}] -> {reason[:50]}...")
