from fastapi.testclient import TestClient

import src.main as main_module


client = TestClient(main_module.app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ask_endpoint(monkeypatch) -> None:
    def fake_ask_llm_answer(question: str, history=None):
        assert question == "What is PROCOM?"
        assert history == []
        return "PROCOM is the flagship event of FAST NUCES Karachi."

    monkeypatch.setattr(main_module, "ask_llm_answer", fake_ask_llm_answer)

    response = client.post(
        "/ask",
        json={"question": "What is PROCOM?", "history": []},
    )

    assert response.status_code == 200
    assert response.json() == {
        "question": "What is PROCOM?",
        "answer": "PROCOM is the flagship event of FAST NUCES Karachi.",
    }


def test_update_knowledge_endpoint(monkeypatch) -> None:
    called = {}

    def fake_ingest_documents(path: str) -> bool:
        called["path"] = path
        return True

    monkeypatch.setattr(main_module, "ingest_documents", fake_ingest_documents)

    response = client.post("/update-knowledge")

    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "Knowledge base updated successfully.",
    }
    assert called["path"] == "knowledge"
