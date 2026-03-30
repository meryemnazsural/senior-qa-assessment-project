from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests
import urllib3

from src.config.settings import settings


@dataclass
class PetstoreClient:
    base_url: str

    def __post_init__(self) -> None:
        self.session = requests.Session()
        self.session.verify = settings.verify_ssl
        if not settings.verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def create_pet(self, payload: dict[str, Any]) -> requests.Response:
        return self.session.post(f"{self.base_url}/pet", json=payload, timeout=30)

    def get_pet(self, pet_id: int) -> requests.Response:
        return self.session.get(f"{self.base_url}/pet/{pet_id}", timeout=30)

    def update_pet(self, payload: dict[str, Any]) -> requests.Response:
        return self.session.put(f"{self.base_url}/pet", json=payload, timeout=30)

    def delete_pet(self, pet_id: int) -> requests.Response:
        return self.session.delete(f"{self.base_url}/pet/{pet_id}", timeout=30)
