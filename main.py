from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

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

class HistoryMessage(BaseModel):
    role: str = Field(..., description="user or assistant")
    content: str = Field(..., description="message content")


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User question")
    history: List[HistoryMessage] = Field(
        ..., description="Prior messages, most recent last; only last 5 are used"
    )


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



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)