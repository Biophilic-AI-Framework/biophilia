import time
from biophilia.semiotics import BiosemioticInterpreter
from biophilia.audit import ImpactAudit
from biophilia.actions import BiophilicActionInterface
from biophilia.integrity import IntegrityChronicle

class BiophilicCore:
    def __init__(self):
        self.interpreter = BiosemioticInterpreter()
        self.audit = ImpactAudit()
        self.actions = BiophilicActionInterface()
        self.chronicle = IntegrityChronicle()
        # Homeostase-Speicher
        self.system_stability = 1.0 

    def run_symbiotic_cycle(self):
        """
        Der Herzschlag des Systems: Fühlt, Denkt, Handelt, Erinnert.
        """
        while True:
            # 1. Wahrnehmung (Zone A -> B)
            raw_data = self.sense_environment()
            signs = self.interpreter.translate(raw_data)
            
            # 2. Symbiotische Entscheidungslogik (Gemma Layer 2)
            for sign in signs:
                # 3. Core-Alignment & Audit (Gemma Layer 1)
                if self.audit.validate(sign, goal="Stability"):
                    
                    # 4. Nuancierte Reaktion (Gemma Layer 4)
                    intensity = self.calculate_nuance(sign)
                    success = self.actions.execute(sign, intensity)
                    
                    # 5. Homeostatische Rückkopplung (Gemma Layer 3)
                    self.update_stability(success, sign)
                    
                    # 6. Integritäts-Chronik (Säule III)
                    self.chronicle.record_action(sign, success)

            time.sleep(10) # Der Rhythmus des Lebens

    def calculate_nuance(self, sign):
        # Verhindert binäres Schalten (Layer 4)
        return 0.5 if "LOW_STRESS" in sign else 1.0

    def update_stability(self, success, sign):
        # Reguliert das System zurück ins Gleichgewicht (Layer 3)
        self.system_stability += 0.05 if success else -0.1
        print(f"Homeostase-Level: {self.system_stability:.2f}")

# --- START DES FRAMEWORKS ---
if __name__ == "__main__":
    biophilia = BiophilicCore()
    biophilia.run_symbiotic_cycle()
