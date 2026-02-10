import time
import json
import os
from typing import Dict, Any, List
from memory_manager.memory_engine import MemoryEngine
from extractor.extract_memory import extract_memory_from_chat
from orchestrator.services.llm_client import LLMClient
from orchestrator.services.prompt_builder import PromptBuilder


class ChatOrchestrator:
    """
    Main orchestrator that connects all components:
    - Memory retrieval
    - Prompt building
    - LLM inference
    - Memory extraction
    """
    
    def __init__(self):
        self.memory_engine = MemoryEngine()
        self.llm_client = LLMClient()
        self.prompt_builder = PromptBuilder()
        
        # Load memory extraction prompt
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.memory_prompt_path = os.path.join(base_dir, "prompts", "memory_prompt.txt")
        
        # Metrics tracking
        self.metrics = {
            "total_requests": 0,
            "total_retrieval_time": 0.0,
            "total_llm_time": 0.0,
            "total_extraction_time": 0.0
        }
    
    async def process_chat(
        self,
        user_id: str,
        message: str,
        conversation_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Process a chat message through the full pipeline
        
        Args:
            user_id: Unique user identifier
            message: User's message
            conversation_history: Optional conversation history
            
        Returns:
            Dictionary with response, metadata, and timing information
        """
        start_time = time.time()
        timings = {}
        
        # Step 1: Retrieve relevant memories
        retrieval_start = time.time()
        memories = self.memory_engine.retrieve_memories(
            query_text=message,
            top_k=5,
            score_threshold=0.3
        )
        timings['retrieval_ms'] = int((time.time() - retrieval_start) * 1000)
        self.metrics['total_retrieval_time'] += time.time() - retrieval_start
        
        # Step 2: Build prompt with memory context
        prompt_start = time.time()
        system_prompt, user_prompt = self.prompt_builder.build_chat_prompt(message, memories)
        timings['prompt_building_ms'] = int((time.time() - prompt_start) * 1000)
        
        # Step 3: Generate LLM response
        llm_start = time.time()
        full_prompt = f"{system_prompt}\n\nUser: {user_prompt}\n\nAssistant:"
        response = self.llm_client.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.7
        )
        timings['llm_ms'] = int((time.time() - llm_start) * 1000)
        self.metrics['total_llm_time'] += time.time() - llm_start
        
        # Step 4: Extract and store new memories (background task)
        extraction_start = time.time()
        self._extract_and_store_memories(user_id, message, response, conversation_history)
        timings['extraction_ms'] = int((time.time() - extraction_start) * 1000)
        self.metrics['total_extraction_time'] += time.time() - extraction_start
        
        # Update metrics
        self.metrics['total_requests'] += 1
        
        # Calculate total latency
        total_latency_ms = int((time.time() - start_time) * 1000)
        
        return {
            "response": response,
            "memories_used": len(memories),
            "latency_ms": total_latency_ms,
            "metadata": timings
        }
    
    def _extract_and_store_memories(
        self,
        user_id: str,
        user_message: str,
        assistant_response: str,
        conversation_history: List[Dict[str, str]] = None
    ):
        """Extract memories from conversation and store them"""
        try:
            # Build conversation for extraction
            conversation = conversation_history or []
            conversation.append({"role": "user", "content": user_message})
            conversation.append({"role": "assistant", "content": assistant_response})
            
            # Save to temporary file for extraction
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(conversation, f)
                temp_path = f.name
            
            try:
                # Extract memories
                extraction_result = extract_memory_from_chat(temp_path, self.memory_prompt_path)
                
                # Store memories
                if extraction_result and extraction_result.get("memories"):
                    self.memory_engine.store_memories(extraction_result)
                    print(f"[Orchestrator] Stored {len(extraction_result['memories'])} new memories for user {user_id}")
            finally:
                # Clean up temp file
                os.unlink(temp_path)
                
        except Exception as e:
            print(f"[Orchestrator] Memory extraction failed: {e}")
    
    def retrieve_memories(
        self,
        user_id: str,
        query: str,
        top_k: int = 5,
        memory_type: str = None
    ) -> Dict[str, Any]:
        """Retrieve memories for a user query"""
        start_time = time.time()
        
        memories = self.memory_engine.retrieve_memories(
            query_text=query,
            top_k=top_k,
            score_threshold=0.3,
            memory_type=memory_type
        )
        
        latency_ms = int((time.time() - start_time) * 1000)
        
        return {
            "memories": memories,
            "count": len(memories),
            "latency_ms": latency_ms
        }
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current system metrics"""
        total_requests = self.metrics['total_requests']
        
        if total_requests == 0:
            return {
                "total_requests": 0,
                "avg_latency_ms": 0.0,
                "avg_memory_retrieval_ms": 0.0,
                "avg_llm_inference_ms": 0.0,
                "total_memories_stored": len(self.memory_engine.list_all_memories())
            }
        
        return {
            "total_requests": total_requests,
            "avg_latency_ms": round(
                (self.metrics['total_retrieval_time'] + 
                 self.metrics['total_llm_time'] + 
                 self.metrics['total_extraction_time']) / total_requests * 1000,
                2
            ),
            "avg_memory_retrieval_ms": round(
                self.metrics['total_retrieval_time'] / total_requests * 1000,
                2
            ),
            "avg_llm_inference_ms": round(
                self.metrics['total_llm_time'] / total_requests * 1000,
                2
            ),
            "total_memories_stored": len(self.memory_engine.list_all_memories())
        }
    
    def health_check(self) -> Dict[str, str]:
        """Check health of all components"""
        return {
            "memory_engine": "healthy" if self.memory_engine else "unavailable",
            "llm_client": "healthy" if self.llm_client.is_available() else "unavailable",
            "prompt_builder": "healthy" if self.prompt_builder else "unavailable"
        }
