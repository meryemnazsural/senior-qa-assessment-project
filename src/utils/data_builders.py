from __future__ import annotations

from time import time


def build_pet_payload(status: str = "available") -> dict:
    pet_id = int(time() * 1000)
    return {
        "id": pet_id,
        "category": {"id": 10, "name": "qa"},
        "name": f"qa-pet-{pet_id}",
        "photoUrls": ["https://example.com/pet.png"],
        "tags": [{"id": 1, "name": "automation"}],
        "status": status,
    }
