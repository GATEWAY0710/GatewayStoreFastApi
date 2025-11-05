import os
from logging import Logger
from typing import Optional, Dict, Any

import httpx


class PaystackService:
    def __init__(self, logger: Logger):
        self._logger = logger
        self.secret_key = os.getenv("PAYSTACK_SECRET_KEY")
        self.base_url = "https://api.paystack.co"
        if not self.secret_key:
            self._logger.critical("PAYSTACK_SECRET_KEY is not set in the environment.")
            raise ValueError("PAYSTACK_SECRET_KEY is not set.")

    def initialize_transaction(self, email: str, amount_in_kobo: int) -> Optional[Dict[str, Any]]:
        """Initializes a transaction and returns the response data from Paystack."""
        url = f"{self.base_url}/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }
        payload = {"email": email, "amount": amount_in_kobo}

        try:
            with httpx.Client() as client:
                response = client.post(url, json=payload, headers=headers)
                response.raise_for_status()  # Raises an exception for 4xx/5xx responses
                return response.json()
        except httpx.HTTPStatusError as e:
            self._logger.error(f"Paystack API error during initialization: {e.response.status_code} - {e.response.text}")
            return None

    def verify_transaction(self, reference: str) -> Optional[Dict[str, Any]]:
        """Verifies a transaction and returns the response data."""
        url = f"{self.base_url}/transaction/verify/{reference}"
        headers = {"Authorization": f"Bearer {self.secret_key}"}

        try:
            with httpx.Client() as client:
                response = client.get(url, headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            self._logger.error(f"Paystack verification error for reference {reference}: {e.response.status_code} - {e.response.text}")
            return None