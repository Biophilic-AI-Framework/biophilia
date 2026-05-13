import json
import os
import datetime
import hashlib

class IntegrityChronicle:
    def __init__(self, filename="biophilic_integrity_history.json"):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logs'))
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        self.filename = os.path.join(base_dir, filename)

    def _calculate_hash(self, entry_dict):
        """Erzeugt einen eindeutigen SHA-256 Hash über die Daten des Eintrags."""
        # sort_keys=True ist essenziell, damit die JSON-Struktur immer exakt gleich serialisiert wird
        entry_string = json.dumps(entry_dict, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(entry_string.encode('utf-8')).hexdigest()

    def record_action(self, action_name, pillar, reason, synergy_score):
        """
        Säule III: Bewahrt die unmanipulierbare Wahrheit der Entscheidungskette.
        Verkettet Einträge kryptografisch über Hashes (Blockchain-Prinzip).
        """
        # 1. Vorhandene Historie laden
        history = []
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                try: 
                    history = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError): 
                    history = []

        # 2. Den Hash des direkt vorherigen Eintrags ermitteln
        # Falls die Chronik leer ist (Erstart), nutzen wir einen "Genesis-Hash"
        previous_hash = history[-1]["current_hash"] if len(history) > 0 else "0" * 64

        # 3. Den neuen Eintrag vorbereiten (Zunächst ohne den eigenen Hash)
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "node": "Forest_Node_01",
            "action": action_name,
            "pillar": pillar,
            "reason": reason,
            "synergy_index": float(synergy_score),
            "previous_hash": previous_hash
        }
        
        # 4. Den kryptografischen Fingerabdruck für DIESEN Eintrag berechnen und anfügen
        entry["current_hash"] = self._calculate_hash(entry)

        # 5. In die Historie einfügen und wegschreiben
        history.append(entry)

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
            
        reason_str = str(reason)[:70] if isinstance(reason, dict) else str(reason)[:70]
        print(f"📖 Chronik: [{action_name}] (Hash: {entry['current_hash'][:8]}...) -> {reason_str}...")

    def verify_integrity(self):
        """
        Validiert die gesamte Kette. Gibt True zurück, wenn die Chronik integer ist, 
        andernfalls False bei Manipulationen.
        """
        if not os.path.exists(self.filename):
            return True # Eine leere, nicht existente Chronik ist nicht manipuliert
            
        with open(self.filename, "r", encoding="utf-8") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                print("🚨 CRITICAL: Chronik-Datei ist strukturell korrupt!")
                return False

        for i in range(len(history)):
            current = history[i]
            
            # Rekonstruiere den Eintrag ohne das Hash-Feld für die Gegenprüfung
            check_entry = current.copy()
            claimed_hash = check_entry.pop("current_hash", None)
            
            # Berechne den Hash neu
            actual_hash = self._calculate_hash(check_entry)
            
            if claimed_hash != actual_hash:
                print(f"🚨 MANIPULATION ERKANNT: Eintrag bei Index {i} wurde modifiziert!")
                return False
                
            if i > 0:
                previous = history[i-1]
                if current["previous_hash"] != previous["current_hash"]:
                    print(f"🚨 KETTENBRUCH ERKANNT: Verbindung zwischen Eintrag {i-1} und {i} manipuliert!")
                    return False
                    
        print("🔒 INTEGRITÄTS-CHECK PASSED: Die Chronik der Wahrheit ist lückenlos verifiziert.")
        return True
