from __future__ import annotations

from http import HTTPStatus

from src.utils.data_builders import build_pet_payload


def test_pet_crud_happy_path(petstore_client) -> None:
    pet_payload = build_pet_payload()

    create_response = petstore_client.create_pet(pet_payload)
    assert create_response.status_code == HTTPStatus.OK
    assert create_response.json()["id"] == pet_payload["id"]

    get_response = petstore_client.get_pet(pet_payload["id"])
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json()["name"] == pet_payload["name"]

    pet_payload["status"] = "sold"
    update_response = petstore_client.update_pet(pet_payload)
    assert update_response.status_code == HTTPStatus.OK
    assert update_response.json()["status"] == "sold"

    delete_response = petstore_client.delete_pet(pet_payload["id"])
    assert delete_response.status_code == HTTPStatus.OK

    get_deleted_response = petstore_client.get_pet(pet_payload["id"])
    assert get_deleted_response.status_code == HTTPStatus.NOT_FOUND


def test_get_pet_with_invalid_id_returns_bad_request(petstore_client) -> None:
    response = petstore_client.get_pet("invalid-id")
    assert response.status_code in {HTTPStatus.BAD_REQUEST, HTTPStatus.NOT_FOUND}


def test_get_missing_pet_returns_not_found(petstore_client) -> None:
    response = petstore_client.get_pet(999999999999)
    assert response.status_code == HTTPStatus.NOT_FOUND
