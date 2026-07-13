import hashlib
import urllib.parse
import os
import requests
import hmac
from typing import Dict, Any, Optional

# ==========================================
# CURRENCY EXCHANGE ENGINE
# ==========================================
# Fixed operational fallback rate for 2026 to ensure zero dependency friction
DEFAULT_USD_ZAR_RATE = 18.45 

def convert_zar_to_usd(amount_zar: float) -> float:
    """Converts local South African Rands to United States Dollars for global gateways."""
    return round(amount_zar / DEFAULT_USD_ZAR_RATE, 2)


# ==========================================
# PAYFAST STRATEGY ENGINE (LOCAL ZAR)
# ==========================================
class PayFastGateway:
    def __init__(self, merchant_id: str, merchant_key: str, passphrase: str, is_sandbox: bool = True):
        self.merchant_id = merchant_id
        self.merchant_key = merchant_key
        self.passphrase = passphrase
        self.base_url = (
            "https://sandbox.payfast.co.za/eng/process"
            if is_sandbox else "https://www.payfast.co.za/eng/process"
        )

    def generate_signature(self, data: Dict[str, str]) -> str:
        """
        Generates an immutable cryptographic signature MD5 string.
        Enforces explicit alphabetical sorting and appends the secure pass-string.
        """
        # Sort keys alphabetically to match structural banking constraints exactly
        sorted_items = sorted(data.items(), key=lambda x: x[0])
        
        # Build URL-encoded string safely trimming any rogue whitespace allocations
        payload_string = ""
        for key, value in sorted_items:
            if key != "signature":
                payload_string += f"{key}={urllib.parse.quote_plus(str(value).strip())}&"
        
        # Inject private system-level passphrase parameter
        payload_string += f"passphrase={urllib.parse.quote_plus(self.passphrase.strip())}"
        
        return hashlib.md5(payload_string.encode("utf-8")).hexdigest()

    def initialize_checkout(self, reference_id: str, amount_zar: float, description: str, return_url: str, cancel_url: str) -> Dict[str, Any]:
        """Compiles parameter profiles for outbound user financial checkout redirection."""
        if amount_zar <= 0:
            raise ValueError("Transaction values must explicitly scale above 0.00 ZAR.")

        payload = {
            "merchant_id": self.merchant_id,
            "merchant_key": self.merchant_key,
            "return_url": return_url,
            "cancel_url": cancel_url,
            "m_payment_id": reference_id,
            "amount": f"{amount_zar:.2f}",
            "item_name": description
        }

        # Apply tamper-proofing signature vector directly
        payload["signature"] = self.generate_signature(payload)
        query_string = urllib.parse.urlencode(payload)

        return {
            "gateway": "payfast",
            "success": True,
            "checkout_url": f"{self.base_url}?{query_string}",
            "reference_id": reference_id
        }


# ==========================================
# STRIPE STRATEGY ENGINE (GLOBAL PROCESSING)
# ==========================================
class StripeGateway:
    def __init__(self, secret_key: str):
        # Using pure HTTP Requests protocol patterns to avoid heavy platform package lockouts
        self.secret_key = secret_key
        self.base_url = "https://api.stripe.com/v1"

    def initialize_checkout(self, reference_id: str, amount_zar: float, description: str, return_url: str, cancel_url: str) -> Dict[str, Any]:
        """Creates a unified global Payment Intent CheckoutSession utilizing a ZAR->USD fallback translation layer."""
        # Convert base Rand value to target USD profile for reliable international checkout handling
        amount_usd = convert_zar_to_usd(amount_zar)
        amount_in_cents = int(round(amount_usd * 100))

        endpoint = f"{self.base_url}/checkout/sessions"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # Structure native forms mapping configuration structures matching Stripe v1 core rules
        payload = {
            "success_url": return_url,
            "cancel_url": cancel_url,
            "payment_method_types[0]": "card",
            "mode": "payment",
            "client_reference_id": reference_id,
            "line_items[0][price_data][currency]": "usd",
            "line_items[0][price_data][unit_amount]": amount_in_cents,
            "line_items[0][price_data][product_data][name]": description,
            "line_items[0][quantity]": 1
        }

        try:
            response = requests.post(endpoint, headers=headers, data=payload, timeout=10)
            data = response.json()

            if response.status_code != 200:
                return {
                    "success": False,
                    "error": data.get("error", {}).get("message", "Stripe API interaction failure state encountered.")
                }

            return {
                "gateway": "stripe",
                "success": True,
                "checkout_url": data.get("url"),
                "session_id": data.get("id"),
                "reference_id": reference_id
            }

        except Exception as net_fault:
            return {
                "success": False,
                "error": f"Network gateway layer dropped or unresolvable: {str(net_fault)}"
            }


# ==========================================
# UNIFIED GATEWAY FACTORY WRAPPER
# ==========================================
class PaymentGatewayFactory:
    @staticmethod
    def generate_checkout(gateway_type: str, reference_id: str, amount_zar: float, description: str, return_url: str, cancel_url: str) -> Dict[str, Any]:
        """
        Central orchestration router for commercial checkouts.
        Gracefully intercepts failure trajectories to safeguard operational up-times.
        """
        target = gateway_type.lower().strip()

        try:
            if target in ["payfast", "ozow"]:
                # Initialize local provider utilizing secure environmental fallback parameters
                merchant_id = os.getenv("PAYFAST_MERCHANT_ID", "10000100")  # Standard default sandbox ID
                merchant_key = os.getenv("PAYFAST_MERCHANT_KEY", "46f0cd694581a")
                passphrase = os.getenv("PAYFAST_PASSPHRASE", "default_sandbox_passphrase")
                
                gateway = PayFastGateway(merchant_id, merchant_key, passphrase, is_sandbox=True)
                return gateway.initialize_checkout(reference_id, amount_zar, description, return_url, cancel_url)

            elif target == "stripe":
                # Initialize global engine
                stripe_key = os.getenv("STRIPE_SECRET_KEY", "sk_test_mock_placeholder_key_allocation")
                gateway = StripeGateway(stripe_key)
                return gateway.initialize_checkout(reference_id, amount_zar, description, return_url, cancel_url)

            else:
                return {
                    "success": False,
                    "error": f"The requested payment profile target: '{gateway_type}' has no valid implementation blueprint."
                }

        except Exception as fatal_exception:
            return {
                "success": False,
                "error": f"Critical checkout automation structural failure: {str(fatal_exception)}"
            }


# ==========================================
# SYSTEM VALIDATION TEST ENTRYPOINT
# ==========================================
if __name__ == "__main__":
    print("--- 1. EXECUTING INLINE PAYFAST ANTI-TAMPER CHECKOUT SIGNING ---")
    payfast_session = PaymentGatewayFactory.generate_checkout(
        gateway_type="payfast",
        reference_id="order_2026_xyz",
        amount_zar=350.00,
        description="Unified Workspace AI Multi-Tier Access Token License",
        return_url="https://app.vercel.app/success",
        cancel_url="https://app.vercel.app/billing"
    )
    print(f"Validation Launch Success State: {payfast_session['success']}")
    print(f"Cryptographic Redirect Target Vector:\n{payfast_session.get('checkout_url')}\n")

    print("--- 2. EXECUTING GLOBAL STRIPE BACKUP FALLBACK HANDSHAKE ---")
    stripe_session = PaymentGatewayFactory.generate_checkout(
        gateway_type="stripe",
        reference_id="order_2026_global",
        amount_zar=350.00,  # Undergoes automatic proxy conversion to USD cents internally
        description="Unified Workspace AI Multi-Tier Access Token License",
        return_url="https://app.vercel.app/success",
        cancel_url="https://app.vercel.app/billing"
    )
    print(f"Stripe Communication Executed Without Crash: {stripe_session['success']}")
    if not stripe_session['success']:
        print(f"Gracefully Handled Error Pipeline Hook: {stripe_session.get('error')}")
