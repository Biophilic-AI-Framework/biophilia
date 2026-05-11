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
        """
        Säule I: Erkennt Mangel UND toxische Überaktivität.
        """
        # FALL 1: KRITISCHER MANGEL
        if voltage < self.thresholds["mycelium_v_drop"]:
            return BioSignal(BioState.CRITICAL, intensity=1.0 - voltage, source="Mycelium")
        
        # FALL 2: TOXISCHE ÜBERAKTIVITÄT (Dein 8.5 Testwert-Problem)
        elif voltage > self.thresholds["mycelium_v_max_harmony"]:
            # Alles über 1.5V wird als Schock/Stress gewertet
            return BioSignal(BioState.CRITICAL, intensity=min(voltage / 10, 1.0), source="Mycelium_Overload")
        
        # FALL 3: GESUNDE HARMONIE
        elif 0.4 < voltage <= self.thresholds["mycelium_v_max_harmony"]:
            return BioSignal(BioState.HARMONY, intensity=voltage/1.5, source="Mycelium")
            
        # FALL 4: RUHEPHASE
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
