from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    response: str = Field(..., description="AI assistant's response")
    memories_used: int = Field(..., description="Number of memories used in context")
    latency_ms: int = Field(..., description="Total response time in milliseconds")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata (retrieval_ms, llm_ms, extraction_ms)"
    )


class MemoryRetrievalResponse(BaseModel):
    """Response model for memory retrieval"""
    memories: List[Dict[str, Any]] = Field(..., description="Retrieved memories")
    count: int = Field(..., description="Number of memories retrieved")
    latency_ms: int = Field(..., description="Retrieval time in milliseconds")


class MemoryExtractionResponse(BaseModel):
    """Response model for memory extraction"""
    extracted_count: int = Field(..., description="Number of memories extracted")
    memories: List[Dict[str, Any]] = Field(..., description="Extracted memories")
    latency_ms: int = Field(..., description="Extraction time in milliseconds")


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="Service status")
    version: str = Field(..., description="API version")
    components: Dict[str, str] = Field(
        default_factory=dict,
        description="Status of individual components"
    )


class MetricsResponse(BaseModel):
    """Response model for metrics endpoint"""
    total_requests: int = Field(..., description="Total number of requests")
    avg_latency_ms: float = Field(..., description="Average latency in milliseconds")
    avg_memory_retrieval_ms: float = Field(..., description="Average memory retrieval time")
    avg_llm_inference_ms: float = Field(..., description="Average LLM inference time")
    total_memories_stored: int = Field(..., description="Total memories in storage")
