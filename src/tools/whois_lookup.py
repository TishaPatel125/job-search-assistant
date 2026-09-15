import logging
import whois
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

logger = logging.getLogger(__name__)

class WhoisResult(BaseModel):
    domain: str
    registrant_org: Optional[str] = None
    registration_date: Optional[str] = None
    expiration_date: Optional[str] = None
    registrar: Optional[str] = None
    country: Optional[str] = None
    error: Optional[str] = None

def lookup(domain: str) -> WhoisResult:
    """Perform a WHOIS lookup on a domain."""
    logger.debug(f'Tool call: whois_lookup("{domain}")')
    try:
        w = whois.whois(domain)
        
        # Handle dates that might be lists
        creation = w.creation_date
        if isinstance(creation, list):
            creation = creation[0]
        expiration = w.expiration_date
        if isinstance(expiration, list):
            expiration = expiration[0]
        
        result = WhoisResult(
            domain=domain,
            registrant_org=w.org if hasattr(w, 'org') else None,
            registration_date=str(creation) if creation else None,
            expiration_date=str(expiration) if expiration else None,
            registrar=w.registrar if hasattr(w, 'registrar') else None,
            country=w.country if hasattr(w, 'country') else None
        )
        logger.debug(f'WHOIS: registered {result.registration_date}, registrar: {result.registrar}')
        return result
    except Exception as e:
        logger.error(f'WHOIS lookup failed for {domain}: {e}')
        return WhoisResult(domain=domain, error=str(e))
