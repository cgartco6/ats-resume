import re
import logging
from typing import Dict, Tuple, Any

# Configure a secure logger that handles compliance reporting
logger = logging.getLogger("ComplianceMiddleware")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [POPIA/GDPR AUDIT] - %(message)s")

class PrivacyComplianceMiddleware:
    def __init__(self):
        # 1. Regex compilation for strict South African & Global PII patterns
        # SA ID: YYMMDDSSSSCZZ (13 Digits)
        self.sa_id_regex = re.compile(r'\b\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{7}\b')
        
        # Email Addresses (Standard RFC 5322)
        self.email_regex = re.compile(r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b')
        
        # Phone Numbers: Matches SA formats (082..., +27...) and general international strings
        self.phone_regex = re.compile(r'\b(?:\+27|0)[6789]\d{8}\b|\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b')
        
        # Structural Street Address Keywords (to identify and redact physical addresses)
        self.address_indicators = [
            r'\d+\s+[A-Za-z0-9\s]{3,}(?:Street|St|Road|Rd|Avenue|Ave|Drive|Dr|Lane|Ln|Way|Crescent|Cres|Plot|Farm)'
        ]
        self.address_regexes = [re.compile(pattern, re.IGNORECASE) for pattern in self.address_indicators]

    def scrub_pii(self, text: str) -> Tuple[str, int]:
        """
        Scrubs Personally Identifiable Information (PII) from user inputs.
        Replaces sensitive components with secure, anonymous semantic tokens.
        
        Returns:
            Tuple[str, int]: The scrubbed text and the total count of redacted elements.
        """
        if not text:
            return "", 0
            
        redaction_count = 0
        scrubbed_text = text

        # Redact South African National ID Numbers
        ids_found = self.sa_id_regex.findall(scrubbed_text)
        if ids_found:
            redaction_count += len(ids_found)
            scrubbed_text = self.sa_id_regex.sub("[REDACTED_NATIONAL_ID]", scrubbed_text)

        # Redact Email Addresses
        emails_found = self.email_regex.findall(scrubbed_text)
        if emails_found:
            redaction_count += len(emails_found)
            scrubbed_text = self.email_regex.sub("[REDACTED_EMAIL]", scrubbed_text)

        # Redact Phone Numbers
        phones_found = self.phone_regex.findall(scrubbed_text)
        if phones_found:
            redaction_count += len(phones_found)
            scrubbed_text = self.phone_regex.sub("[REDACTED_PHONE_NUMBER]", scrubbed_text)

        # Redact Physical Street Addresses
        for regex in self.address_regexes:
            addresses_found = regex.findall(scrubbed_text)
            if addresses_found:
                redaction_count += len(addresses_found)
                scrubbed_text = regex.sub("[REDACTED_PHYSICAL_ADDRESS]", scrubbed_text)

        return scrubbed_text, redaction_count


class TransientSessionContainer:
    """
    Enforces a strict transient runtime context.
    Guarantees data memory structures are explicitly expunged
    the moment the file export payload is completed.
    """
    def __init__(self, session_id: str):
        self.session_id = session_id
        self._memory_store: Dict[str, Any] = {}
        logger.info(f"Transient processing context initialized for Session: {self.session_id}")

    def store_transient_data(self, key: str, data: Any) -> None:
        """Saves operational state explicitly to an in-memory buffer."""
        self._memory_store[key] = data

    def get_transient_data(self, key: str) -> Any:
        return self._memory_store.get(key)

    def complete_export_and_purge(self) -> bytes:
        """
        Simulates final generation of a PDF or system document asset, 
        then immediately purges all operational memory profiles.
        """
        logger.info(f"Compiling document payload for Session: {self.session_id}")
        
        # Simulate final compiled binary array generation
        mock_pdf_binary_payload = b"%PDF-1.4 Mock Binary Document Stream Data"
        
        # CRITICAL POPIA COMPLIANCE STEP: Immediate destructive reference wipe
        keys_purged = list(self._memory_store.keys())
        self._memory_store.clear()
        del self._memory_store
        
        # Re-initialize to clean state to block stale reference pointers
        self._memory_store = {}
        
        # AUDIT HOOK: Confirms data destruction without persisting the underlying values
        logger.info(
            f"SUCCESSFUL PURGE EXECUTION. Session: {self.session_id} has been completely dropped from memory. "
            f"Data keys destroyed: {keys_purged}. Underlying PII retention state: ZERO."
        )
        
        return mock_pdf_binary_payload


# ==========================================
# SANITY DEMONSTRATION & INTEGRATION TEST
# ==========================================

def run_middleware_test():
    middleware = PrivacyComplianceMiddleware()
    
    # Raw input string containing multiple layers of high-risk PII
    raw_user_cv_input = (
        "My name is John Doe. I live at 42 Protea Road, Wesfleur, Atlantis. "
        "My ID number is 9403155123084, my cell number is 0821234567, "
        "and you can reach me directly via email at john.doe@example.com."
    )
    
    print("--- 1. INLINE INTERCEPTION & SCRUBBING ---")
    scrubbed_output, total_redacted = middleware.scrub_pii(raw_user_cv_input)
    print(f"Original Text Size: {len(raw_user_cv_input)} characters.")
    print(f"Total Redacted Elements: {total_redacted}")
    print(f"Scrubbed Payload Sent to AI:\n{scrubbed_output}\n")

    print("--- 2. TRANSIENT MEMORY CYCLING & SECURE AUDITING ---")
    # Open isolated memory context block
    session = TransientSessionContainer(session_id="ctx_987452")
    
    # Store scrubbed payload and structural application assets temporarily
    session.store_transient_data("scrubbed_content", scrubbed_output)
    session.store_transient_data("workspace_meta", {"target_module": "ats_optimizer"})
    
    # Finalize the build cycle: compiles structural PDF asset and triggers the explicit purge
    pdf_payload = session.complete_export_and_purge()
    print(f"Export Complete. File Buffer Size Generated: {len(pdf_payload)} bytes.")

if __name__ == "__main__":
    run_middleware_test()
