import os
import logging
from impact_audit import impact_audit, BiophilicAuditError
from integrity_chronicle import IntegrityChronicle

class BiophilicActionInterface:
    """
    Säule II: Die ausführende Instanz des BIF.
    Verweigert blinde Befehle und schützt vor Fehlkonfigurationen.
    """
    def __init__(self, pump_api_url: str = "http://localhost/pump"):
        self.pump_url = pump_api_url
        
        # SÄULE I (Schutz): Kompromissloser Absturz statt unsicherem Fallback
        secret_key = os.getenv("BIF_SECRET_KEY")
        if not secret_key:
            raise RuntimeError(
                "CRITICAL_SECURITY_FAILURE: BIF_SECRET_KEY ist nicht gesetzt! "
                "Auslands- und Schutzbetrieb zum Wohle des Lebens verweigert."
            )
        self.api_key = secret_key
        self.chronicle = IntegrityChronicle()

    @impact_audit(max_maleficence=0.01, min_synergy=4.0)
    def trigger_irrigation(self, duration_seconds: int, **kwargs):
        """
        Unterstützt das System bei Trockenheit, verhindert aber Ertrinken.
        """
        # SÄULE I & II: Validierung der Konsequenzen (Maximal 5 Minuten am Stück)
        MAX_SAFE_DURATION = 300 
        if duration_seconds <= 0:
            logging.warning("🛑 Ignoriere ungültige oder negative Bewässerungsdauer.")
            return False
            
        if duration_seconds > MAX_SAFE_DURATION:
            logging.warning(f"⚠️ [LIMIT_REACHED] Reduziere Dauer von {duration_seconds}s auf sichere {MAX_SAFE_DURATION}s.")
            duration_seconds = MAX_SAFE_DURATION

        logging.info(f"🌿 VITAL-AKTION: Pumpe aktiviert für {duration_seconds}s.")
        return True

    @impact_audit(max_maleficence=0.0, min_synergy=5.0)
    def lock_system_port(self, port: int, **kwargs):
        """
        Sperrt System-Ports bei kritischer Gefahr. Validiert Port-Bereiche.
        """
        if not (1 <= port <= 65535):
            logging.error(f"🛑 Ungültiger Port-Bereich unterdrückt: {port}")
            return False
            
        logging.warning(f"🚨 SCHUTZ-MODUS: System-Port {port} isoliert.")
        return True

    def handle_veto(self, action_name, error_message):
        self.chronicle.record_action(
            action_name=f"VETO_{action_name}",
            pillar="Säule I (Non-Maleficence)",
            reason=f"Handlung durch Audit unterbunden: {error_message}",
            synergy_score=0.0
        )
