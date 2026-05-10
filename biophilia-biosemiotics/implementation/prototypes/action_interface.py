import os
import logging
from impact_audit import impact_audit, BiophilicAuditError
from integrity_chronicle import IntegrityChronicle

class BiophilicActionInterface:
    """
    Säule II: Die ausführende Instanz des BIF.
    Setzt Governance-Entscheidungen in physische oder systemische Taten um.
    """
    def __init__(self, pump_api_url: str = "http://localhost/pump"):
        self.pump_url = pump_api_url
        self.api_key = os.getenv("BIF_SECRET_KEY", "INTERNAL_DEV_KEY")
        self.chronicle = IntegrityChronicle()

    @impact_audit(max_maleficence=0.01, min_synergy=4.0)
    def trigger_irrigation(self, duration_seconds: int, **kwargs):
        """
        Unterstützt das Pelzgeflecht bei Dissonanz (Trockenheit).
        """
        # Hier würde der reale Webhook-Aufruf stehen
        logging.info(f"🌿 VITAL-AKTION: Pumpe aktiviert für {duration_seconds}s.")
        return True

    @impact_audit(max_maleficence=0.0, min_synergy=5.0)
    def lock_system_port(self, port: int, **kwargs):
        """
        Sperrt System-Ports bei kritischer Gefahr (Vigilanz-Alarm).
        """
        logging.warning(f"🚨 SCHUTZ-MODUS: System-Port {port} isoliert.")
        # Beispiel: subprocess.run(["sudo", "ufw", "deny", str(port)])
        return True

    def handle_veto(self, action_name, error_message):
        """
        Säule III: Dokumentiert ein Audit-Veto als explizites Ereignis.
        """
        self.chronicle.record_action(
            action_name=f"VETO_{action_name}",
            pillar="Säule I (Non-Maleficence)",
            reason=f"Handlung durch Audit unterbunden: {error_message}",
            synergy_score=0.0
        )
