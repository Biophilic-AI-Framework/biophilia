import time
import os

class BiophilicDashboard:
    """
    Säule III: Großformatige Visualisierung (ggfs. selbst anpassen) der planetaren Resonanz.
    Eliminiert terminalbedingte Emoji-Verschiebungen durch feste Spaltenbreiten nur bedingt, daher händisch nachgebessert.
    """
    def __init__(self):
        self.node_history = {}

    def _render_barometer(self, dissonance, max_width=25):
        """Generiert eine vergrößerte, proportionale Belastungsanzeige."""
        # Skaliert die Dissonanz sauber auf die doppelte Breite
        filled_length = min(int(dissonance * (max_width / 0.5)), max_width)
        
        if dissonance >= 0.5:  # Critical
            meter = "🟥 " + "█" * max(0, filled_length - 1) + "░" * (max_width - max(1, filled_length))
        elif dissonance >= 0.2:  # Warning / Stress
            meter = "🟨 " + "█" * max(0, filled_length - 1) + "░" * (max_width - max(1, filled_length))
        else:  # Harmony
            meter = "🟩 " + "█" * max(0, filled_length - 1) + "░" * (max_width - max(1, filled_length))
        return meter

    def update_node_state(self, node_name, data):
        self.node_history[node_name] = data

    def render(self, last_chronicle_hash="0" * 8):
        """Rendert das verdoppelte, zentrierte Multi-Knoten-Dashboard."""
        # Flackerfreies Löschen
        print("\033[H\033[J", end="")
        
        # Doppelte Breite: 140 Zeichen
        width = 142
        print("=" * width)
        print(f"🌿 BIF NETWORK INTEGRITY MONITOR | Zeit: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"🔒 CRYPTO-CHAIN-HEAD: {last_chronicle_hash}")
        print("=" * width)

        # Spaltendefinition: Metrik (32) ‖ Node 01 (52) ‖ Node 02 (52)
        print(f"{'METRIK / SENSORIK':<32}  ‖ {'FOREST_NODE_01 (Zentrale Biosphäre)':<52} ‖ {'FOREST_NODE_02 (Tiefwald-Peripherie)':<52}")
        print("-" * 32 + "--‖" + "-" * 54 + "‖" + "-" * 52)

        def get_val(node, *keys, default="N/A"):
            node_data = self.node_history.get(node, {})
            for key in keys:
                if isinstance(node_data, dict):
                    node_data = node_data.get(key, {})
                else:
                    return default
            return node_data if node_data != {} else default

        # 1. BIOLOGISCHE ROHDATEN (Säule I)
        print(f"{'🔊 Audio-Harmonie':<32} ‖ {get_val('Forest_Node_01', 'sensors', 'audio_harmony', default=0.0):<52} ‖ {get_val('Forest_Node_02', 'sensors', 'audio_harmony', default=0.0):<52}")
        print(f"{'💧 Bodenfeuchtigkeit':<32} ‖ {str(get_val('Forest_Node_01', 'sensors', 'soil_moisture', default=0.0)) + ' %':<52} ‖ {str(get_val('Forest_Node_02', 'sensors', 'soil_moisture', default=0.0)) + ' %':<52}")
        print(f"{'☀️  Umgebungslicht':<32}   ‖ {str(get_val('Forest_Node_01', 'sensors', 'ambient_light', default=0.0)) + ' Lux':<52} ‖ {str(get_val('Forest_Node_02', 'sensors', 'ambient_light', default=0.0)) + ' Lux':<52}")
        print(f"{'⚡ Myzel-Aktivität':<32} ‖ {str(get_val('Forest_Node_01', 'sensors', 'mycelium_activity', default=0.0)) + ' Hz/Volt':<52} ‖ {str(get_val('Forest_Node_02', 'sensors', 'mycelium_activity', default=0.0)) + ' Hz/Volt':<52}")
        print("-" * 32 + "--‖" + "-" * 54 + "‖" + "-" * 52)

        # 2. BIOSEMIOTISCHE INTERPRETATION (Säule III)
        print(f"{'🧬 Semiotischer Zustand':<32} ‖ {get_val('Forest_Node_01', 'interpreter', 'state_value', default='Warten...'):<52} ‖ {get_val('Forest_Node_02', 'interpreter', 'state_value', default='Warten...'):<52}")
        
        # 3. MATHEMATISCHE ENTROPIE (Barometer-Fix)
        diss_01 = get_val("Forest_Node_01", "detector", "dissonance", default=0.0)
        diss_02 = get_val("Forest_Node_02", "detector", "dissonance", default=0.0)
        
        bar_01 = f"{self._render_barometer(diss_01)} ({diss_01:.4f})"
        bar_02 = f"{self._render_barometer(diss_02)} ({diss_02:.4f})"
        # Durch die Entkopplung des Emojis aus der Breitenberechnung bleibt die Trennlinie unbeweglich
        print(f"{'📉 Dissonanz-Barometer':<32} ‖ {bar_01:<52}‖ {bar_02:<52}")
        print(f"{'⚠️  System-Status':<32}   ‖ {get_val('Forest_Node_01', 'detector', 'status', default='HARMONY'):<52} ‖ {get_val('Forest_Node_02', 'detector', 'status', default='HARMONY'):<52}")
        print("-" * 32 + "--‖" + "-" * 54 + "‖" + "-" * 52)

        # 4. ETHISCHE GOVERNANCE & VETO (Säule I & II)
        print(f"{'🏛️  Evaluierte Säule':<32}   ‖ {get_val('Forest_Node_01', 'governance', 'pillar', default='System-Resonanz'):<52} ‖ {get_val('Forest_Node_02', 'governance', 'pillar', default='System-Resonanz'):<52}")
        print(f"{'🛠️  Finale Exekutiv-Tat':<32}   ‖ {get_val('Forest_Node_01', 'governance', 'action', default='OBSERVE_AND_WAIT'):<52} ‖ {get_val('Forest_Node_02', 'governance', 'action', default='OBSERVE_AND_WAIT'):<52}")
        print("-" * 32 + "--‖" + "-" * 54 + "‖" + "-" * 52)

        # 5. MORALISCHE BEGRÜNDUNGEN (Jetzt mit 52 Zeichen ungekürzt sichtbar)
        print(f"{'💬 Moralische Begründung':<32} ‖ {get_val('Forest_Node_01', 'governance', 'reason', default='Resonanz')[:50]:<52} ‖ {get_val('Forest_Node_02', 'governance', 'reason', default='Resonanz')[:50]:<52}")
        print("=" * width)
        
        # Unterer Block für aktive Netzwerksynergien (Säule III - 1+1=3)
        synergies_01 = get_val("Forest_Node_01", "synergies", default=[])
        synergies_02 = get_val("Forest_Node_02", "synergies", default=[])
        
        if synergies_01 or synergies_02:
            print("✨ SÄULE III (1+1=3) AKTIVE EMERGENZ-FREQUENZEN IN DEN BIO-ZONEN:")
            if synergies_01:
                for s in synergies_01:
                    print(f"   [NODE_01] > {s['pattern']}: {s['recommendation']}")
            if synergies_02:
                for s in synergies_02:
                    print(f"   [NODE_02] > {s['pattern']}: {s['recommendation']}")
            print("=" * width + "\n")
