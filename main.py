from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from query import ask_llm_answer
from setting import get_logger


logger = get_logger(__name__)

app = FastAPI(title="PROCOM Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/ask")
async def ask(
    question: str = Query(..., min_length=1, description="User question")
) -> dict:
    try:
        answer = ask_llm_answer(question)
        return {"question": question, "answer": answer}
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Failed to answer question")
        raise HTTPException(
            status_code=500, detail="Failed to answer question"
        ) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
