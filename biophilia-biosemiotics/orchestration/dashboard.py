import time
import os

class BiophilicDashboard:
    """
    Säule III: Visualisierung der Resonanz.
    Stellt die Verbindung zwischen der Semiosphäre und dem Architekten her.
    """
    def __init__(self, node_name="Forest_Node_01"):
        self.node_name = node_name

    def display_status(self, dissonance, status, response, synergies):
        """
        Präsentiert den aktuellen Puls des Systems in einer klaren Hierarchie.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"============================================================")
        print(f"🌿 BIF INTEGRITY DASHBOARD | Node: {self.node_name}")
        print(f"Zeit: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"============================================================")
        
        # 1. Dissonanz-Barometer
        meter = "█" * int(dissonance * 20) + "░" * (20 - int(dissonance * 20))
        print(f"Status:     [{meter}] {status} ({dissonance:.4f})")
        
        # 2. Aktive Governance
        print(f"Ebene:      {response['level']}")
        print(f"Handlung:   {response['action']}")
        
        # 3. Synergie-Ebene (Thriving)
        if synergies:
            print(f"------------------------------------------------------------")
            print(f"✨ AKTIVE SYNERGIEN:")
            for s in synergies:
                print(f"   > {s['pattern']}: {s['impact']}")
        
        # 4. Begründung (Säule II)
        print(f"------------------------------------------------------------")
        print(f"Grund: {response['description'][:120]}")
        print(f"============================================================\n")

# --- INTEGRATION ---
# Das Dashboard wird in der main.py aufgerufen, um das 'print' Gewirr zu ersetzen.
