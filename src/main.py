from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.models import AskRequest
from src.query import ask_llm_answer
from src.setting import get_logger
from src.ingest import ingest_documents


logger = get_logger(__name__)

app = FastAPI(title="PROCOM Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.post("/ask")
async def ask(body: AskRequest):
    try:
        answer = ask_llm_answer(body.question, history=body.history)
        return {"question": body.question, "answer": answer}
    except Exception:
        logger.exception("Failed to answer question")
        return {
            "question": body.question,
            "answer": "Sorry I got too tired while cooking, try again or after some time, meanwhile you can ask your queries on our Contact Us Page: www.procom26.com/contact",
        }


@app.post("/update-knowledge")
async def update_knowledge():
    """Trigger knowledge base update from the knowledge/ folder."""
    try:
        success = ingest_documents("knowledge")
        if success:
            return {"status": "success", "message": "Knowledge base updated successfully."}
        else:
            return {"status": "error", "message": "Failed to ingest documents."}
    except Exception as e:
        logger.exception("Knowledge base update failed")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=3000, reload=True)