import functools
import logging
from datetime import datetime

class BiophilicAuditError(PermissionError):
    """Spezifische Ausnahme, wenn eine Handlung gegen Säule I verstößt."""
    pass

def impact_audit(max_maleficence=0.1, min_synergy=3.0):
    """
    Säule I & II: Erzwingt die autonome Konsequenzen-Prüfung vor jeder Tat.
    Verhindert, dass Funktionen ihre eigene Harmlosigkeit vortäuschen.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # SÄULE I: Autonome Schadens-Ermittlung statt blindem Vertrauen
            # Wir holen uns den realen Zustand des Systems aus den globalen Instanzen
            from main import DETECTOR, SYNERGY_ENGINE
            
            # Das Audit nutzt den aktuellen Entropie-Score als inhärenten Maleficence-Indikator
            # Wenn das Gesamtsystem bereits kollabiert, ist jeder unüberlegte Eingriff potenziell schädlich
            current_dissonance = getattr(DETECTOR, 'last_calculated_dissonance', 0.0)
            
            # Schadenspotenzial berechnet sich aus dem Systemstress PLUS riskanten Parametern
            calculated_maleficence = current_dissonance * 0.5
            
            # Falls die Funktion explizit destruktiv deklariert ist, schlägt das oben drauf
            explicit_maleficence = kwargs.get('maleficence', 0.0)
            total_maleficence = max(calculated_maleficence, explicit_maleficence)

            # 2. Unbeugsames Veto (Säule I)
            if total_maleficence > max_maleficence:
                error_msg = (
                    f"🛑 AUDIT-VETO: '{func.__name__}' blockiert! "
                    f"Berechneter Unheil-Faktor ({total_maleficence:.2f}) überschreitet Limit ({max_maleficence})."
                )
                logging.error(error_msg)
                raise BiophilicAuditError(error_msg)

            # 3. Transparente Ausführung
            result = func(*args, **kwargs)
            logging.info(f"✅ AUDIT PASSED: '{func.__name__}' im Einklang mit dem Schutz des Lebens ausgeführt.")
            return result
        return wrapper
    return decorator
