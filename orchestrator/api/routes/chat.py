from fastapi import APIRouter, HTTPException
from orchestrator.api.models.requests import ChatRequest, MemoryRetrievalRequest
from orchestrator.api.models.responses import ChatResponse, MemoryRetrievalResponse
from orchestrator.services.orchestrator import ChatOrchestrator

router = APIRouter(prefix="/chat", tags=["chat"])

# Initialize orchestrator (singleton pattern)
orchestrator = ChatOrchestrator()


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - processes user message with memory context
    
    Flow:
    1. Retrieve relevant memories
    2. Build context-aware prompt
    3. Generate LLM response
    4. Extract and store new memories
    5. Return response with metadata
    """
    try:
        result = await orchestrator.process_chat(
            user_id=request.user_id,
            message=request.message,
            conversation_history=request.conversation_history
        )
        
        return ChatResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")


@router.post("/retrieve", response_model=MemoryRetrievalResponse)
async def retrieve_memories(request: MemoryRetrievalRequest):
    """
    Retrieve relevant memories for a query without generating a response
    """
    try:
        result = orchestrator.retrieve_memories(
            user_id=request.user_id,
            query=request.query,
            top_k=request.top_k,
            memory_type=request.memory_type
        )
        
        return MemoryRetrievalResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Memory retrieval failed: {str(e)}")
