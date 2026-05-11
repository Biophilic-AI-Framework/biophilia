import json
import os
import datetime

class IntegrityChronicle:
    def __init__(self, filename="biophilic_integrity_history.json"):
        # Absoluter Pfad zum /logs Ordner - Bleibt unangetastet
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logs'))
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        self.filename = os.path.join(base_dir, filename)

    def record_action(self, action_name, pillar, reason, synergy_score):
        """
        Säule III: Bewahrt die Integrität der Entscheidungskette.
        'reason' kann nun sowohl ein String als auch ein strukturiertes Dictionary sein.
        """
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "node": "Forest_Node_01",
            "action": action_name,
            "pillar": pillar,
            "reason": reason, # Hier fließt die kombinierte Bio- und System-Logik ein
            "synergy_index": synergy_score
        }
        
        history = []
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                try: 
                    history = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError): 
                    history = []

        history.append(entry)

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
            
        # Saubere Konsolenausgabe, auch wenn 'reason' ein Dict ist
        reason_str = str(reason)[:70] if isinstance(reason, dict) else str(reason)[:70]
        print(f"📖 Chronik: [{action_name}] -> {reason_str}...")
