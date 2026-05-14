import os

import pytest
from fastapi.testclient import TestClient

import src.main as main_module


REQUIRED_ENV_VARS = ["GROQ_API_KEY_1", "VOYAGE_API_KEY"]


missing_env_vars = [name for name in REQUIRED_ENV_VARS if not os.getenv(name)]
if missing_env_vars:
    pytest.skip(
        "Missing live API credentials: " + ", ".join(missing_env_vars),
        allow_module_level=True,
    )


client = TestClient(main_module.app)


@pytest.mark.integration
def test_real_chatbot_smoke() -> None:
    update_response = client.post("/update-knowledge")

    assert update_response.status_code == 200
    assert update_response.json()["status"] == "success"

    response = client.post(
        "/ask",
        json={"question": "What is PROCOM?", "history": []},
    )

    assert response.status_code == 200
    body = response.json()

    assert body["question"] == "What is PROCOM?"
    assert isinstance(body["answer"], str)
    assert body["answer"].strip()
    assert "not configured" not in body["answer"].lower()
