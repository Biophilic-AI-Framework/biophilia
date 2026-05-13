import json
import os
from enum import Enum
from dataclasses import dataclass

class BioState(Enum):
    HARMONY = "Harmonie/Wachstum"
    STRESS = "Stress/Alarm"
    DORMANT = "Ruhezustand/Dormanz"
    RECOVERY = "Erholung"
    CRITICAL = "Kritischer Zustand"

@dataclass
class BioSignal:
    token: BioState
    intensity: float
    source: str

class BiosemioticInterpreter:
    def __init__(self):
        base_dir = os.path.dirname(__file__)
        patterns_path = os.path.join(base_dir, '../../orchestration/bio_data/vocal_patterns.json')
        
        try:
            with open(patterns_path, 'r', encoding='utf-8') as f:
                self.patterns = json.load(f)["patterns"]
        except FileNotFoundError:
            self.patterns = {}
            
        self.thresholds = {
            "mycelium_v_drop": 0.2, 
            "mycelium_v_max_harmony": 1.5, # Grenze für gesundes Wachstum
            "acoustic_var_high": 0.7
        }

    def interpret_mycelium(self, voltage: float, conductivity: float) -> BioSignal:
        max_h = self.thresholds["mycelium_v_max_harmony"]
        drop_v = self.thresholds["mycelium_v_drop"]

        # FALL 1: KRITISCHER MANGEL (Fließender Übergang gegen 0 Volt)
        if voltage < drop_v:
            intensity = (drop_v - voltage) / drop_v
            return BioSignal(BioState.CRITICAL, intensity=round(intensity, 4), source="Mycelium_Deficit")
    
        # FALL 2: TOXISCHE ÜBERAKTIVITÄT (Verhindert das 8.5V Glättungs-Problem)
        if voltage > max_h:
            # Exponentieller Anstieg der Kritikalität statt linearer Teiler
            # Ein Wert von 8.5V führt hier sofort zu einer massiven, nicht-linearen Intensität
            excess = voltage - max_h
            intensity = 1.0 - (1.0 / (1.0 + excess)) # Asymptotisch gegen 1.0, aber extrem steil
            return BioSignal(BioState.CRITICAL, intensity=round(intensity, 4), source="Mycelium_Overload")
    
        # FALL 3 & 4: HARMONIE UND ÜBERGANG ZUR DORMANZ
        if 0.4 < voltage <= max_h:
            return BioSignal(BioState.HARMONY, intensity=round(voltage / max_h, 4), source="Mycelium")
        
        return BioSignal(BioState.DORMANT, 0.5, "Mycelium")


    def interpret_acoustics(self, noise: float, variance: float) -> BioSignal:
        # Säule III: Erkennt Stille als Alarmzustand (Vigilanz)
        if variance < 0.05: # Absolute Stille im Wald
            return BioSignal(BioState.CRITICAL, intensity=0.95, source="Acoustics_Vigilance")
            
        if variance > self.thresholds["acoustic_var_high"]:
            return BioSignal(BioState.STRESS, intensity=variance, source="Acoustics_Noise")
            
        return BioSignal(BioState.HARMONY, intensity=1.0 - variance, source="Acoustics")

    def synthesize_state(self, signals: list[BioSignal]) -> BioState:
        # Holistischer Check: Schutz des Lebens hat immer Priorität
        tokens = [s.token for s in signals]
        if BioState.CRITICAL in tokens: return BioState.CRITICAL
        if BioState.STRESS in tokens: return BioState.STRESS
        return BioState.HARMONY
        
