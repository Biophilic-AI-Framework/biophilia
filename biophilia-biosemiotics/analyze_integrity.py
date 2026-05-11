import json
import os

def analyze_vetos(logfile="logs/biophilic_integrity_history.json"):
    if not os.path.exists(logfile):
        print("Datei nicht gefunden.")
        return

    with open(logfile, "r", encoding="utf-8") as f:
        history = json.load(f)

    print(f"--- 🛡️ BIF VETO-REPORTS (Säule II) ---")
    for entry in history:
        reason = entry.get("reason")
        
        # Wir prüfen nur die neuen, strukturierten Einträge
        if isinstance(reason, dict):
            systemic = reason.get("systemic_analysis", "")
            bio_state = reason.get("biosemiotic_state", "")
            
            # Ein Veto liegt vor, wenn das System 'Harmonie' sagt, aber gehandelt wurde
            if "Harmonie" in systemic and entry["action"] != "ENHANCE_VITALITY":
                print(f"[{entry['timestamp']}] VETO!")
                print(f"  Systemik sagt: {systemic}")
                print(f"  Biologie sagt: {bio_state}")
                print(f"  Gewählte Aktion: {entry['action']}\n")

if __name__ == "__main__":
    analyze_vetos()
