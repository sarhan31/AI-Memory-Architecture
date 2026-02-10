from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    user_id: str = Field(..., description="Unique user identifier")
    message: str = Field(..., description="User's message/query")
    conversation_history: Optional[List[Dict[str, str]]] = Field(
        default=None,
        description="Optional conversation history for context"
    )


class MemoryRetrievalRequest(BaseModel):
    """Request model for memory retrieval"""
    user_id: str = Field(..., description="Unique user identifier")
    query: str = Field(..., description="Query to search memories")
    top_k: Optional[int] = Field(default=5, description="Number of memories to retrieve")
    memory_type: Optional[str] = Field(
        default=None,
        description="Filter by memory type: preference, fact, constraint, commitment"
    )


class MemoryExtractionRequest(BaseModel):
    """Request model for memory extraction"""
    user_id: str = Field(..., description="Unique user identifier")
    conversation_history: List[Dict[str, str]] = Field(
        ...,
        description="Conversation history to extract memories from"
    )
