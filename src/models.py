from typing import List

from pydantic import BaseModel, Field


class HistoryMessage(BaseModel):
    role: str = Field(..., description="user or assistant")
    content: str = Field(..., description="message content")


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User question")
    history: List[HistoryMessage] = Field(
        default_factory=list,
        description="Prior messages, most recent last; only last 5 are used",
    )
