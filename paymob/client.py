from typing import Dict, List, Optional
import requests
import hmac
import hashlib
from .dataclasses import *
from .stracture import SingletonMeta



class PaymobIntentionClient:
    BASE_URL = "https://accept.paymob.com"
    
    def __init__(self, secret_key, public_key, hmac_key=None):
        self.secret_key = secret_key
        self.public_key = public_key
        self.hmac_key = hmac_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {self.secret_key}"
        }

    def create_intention(
        self,
        intention:Intention
    ) -> Union[PaymentIntention,Errors]:
        """Create payment intention"""
        payload = intention.model_dump()
        print(payload)
        response = requests.post(
            f"{self.BASE_URL}/v1/intention/",
            json=payload,
            headers=self.headers
        )
        json_data = response.json()
        # print(response,response.text)
        # response.raise_for_status()
        if response.ok :
            return PaymentIntention(
                **json_data
            )
        return Errors(errors=json_data)

    def get_payment_url(self, client_secret: str) -> str:
        """Generate payment page URL"""
        return f"{self.BASE_URL}/unifiedcheckout/?publicKey={self.public_key}&clientSecret={client_secret}"


    # HMAC validation remains the same as before
    def validate_hmac(self, data: Dict) -> bool:
        """Validate HMAC signature from callback"""
        received_hmac = data.get('hmac')
        if not received_hmac or not self.hmac_key:
            return False

        hmac_order = [
            'amount_cents',
            'created_at',
            'currency',
            'error_occurred',
            'has_parent_transaction',
            'id',
            'integration_id',
            'is_3d_secure',
            'is_auth',
            'is_capture',
            'is_refunded',
            'is_standalone_payment',
            'is_voided',
            'order',
            'owner',
            'pending',
            'source_data_pan',
            'source_data_sub_type',
            'source_data_type',
            'success'
        ]

        hmac_str = ''.join(
            str(data.get(key, '')) if not isinstance(data.get(key, ''), dict)
            else str(data.get(key, {}).get('id', ''))
            for key in hmac_order
        )

        digest = hmac.new(
            self.hmac_key.encode('utf-8'),
            hmac_str.encode('utf-8'),
            hashlib.sha512
        ).hexdigest()

        return hmac.compare_digest(digest, received_hmac)
