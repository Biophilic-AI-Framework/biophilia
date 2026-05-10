import logging
import os
import time

class BiophilicLogger:
    """
    Säule III: Dokumentiert den biosemiotischen Datenfluss zwischen den Zonen.
    Ermöglicht die Analyse der Resonanz über Zeiträume hinweg.
    """
    def __init__(self, log_name="biophilia_pulse.log"):
        # Verortung im neuen /logs/ Verzeichnis
        log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logs'))
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        self.log_path = os.path.join(log_dir, log_name)
        
        # Konfiguration des Python-Loggers
        self.logger = logging.getLogger("BiophilicLogger")
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            file_handler = logging.FileHandler(self.log_path)
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def log_pulse(self, zone, message, data=None):
        """
        Protokolliert einen 'Puls' des Systems.
        Zone A: Sensing | Zone B: Interpretation | Zone C: Governance
        """
        payload = f"[{zone}] {message}"
        if data:
            payload += f" | Data: {data}"
        
        self.logger.info(payload)
        # Optional: Auch auf die Konsole ausgeben für Echtzeit-Feedback
        # print(f"📡 {payload}")

# --- INTEGRATION IN DIE main.py ---
# Der Logger wird in der run_biophilic_loop initialisiert:
# pulse_logger = BiophilicLogger()
# pulse_logger.log_pulse("Zone A", "Rohdaten empfangen", current_sensor_data)
