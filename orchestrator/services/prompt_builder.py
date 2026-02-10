from typing import List, Dict, Any


class PromptBuilder:
    """Builds context-aware prompts with memory injection"""
    
    MAX_MEMORIES = 5
    MAX_TOKENS_PER_MEMORY = 50
    
    def __init__(self):
        self.system_template = """You are a helpful AI assistant with access to user memory.
Use the provided memory context to personalize your responses and maintain continuity across conversations.

Guidelines:
- Reference user's preferences, facts, and constraints when relevant
- Be natural and conversational
- Don't explicitly mention "according to your memory" unless necessary
- If memory is empty, respond normally without personalization"""
    
    def build_chat_prompt(self, user_message: str, memories: List[Dict[str, Any]]) -> tuple[str, str]:
        """
        Build a complete prompt with memory context
        
        Args:
            user_message: User's query/message
            memories: List of retrieved memories with metadata
            
        Returns:
            Tuple of (system_prompt, user_prompt)
        """
        # Filter and limit memories
        relevant_memories = self._filter_memories(memories)
        
        # Build memory context
        memory_context = self._format_memory_context(relevant_memories)
        
        # Build system prompt
        system_prompt = self.system_template
        if memory_context:
            system_prompt += f"\n\n{memory_context}"
        
        # User prompt is just the message
        user_prompt = user_message
        
        return system_prompt, user_prompt
    
    def _filter_memories(self, memories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter and prioritize memories based on relevance and confidence"""
        if not memories:
            return []
        
        # Sort by score (relevance) and confidence
        sorted_memories = sorted(
            memories,
            key=lambda m: (m.get('score', 0), m.get('memory', {}).get('confidence', 0)),
            reverse=True
        )
        
        # Limit to MAX_MEMORIES
        return sorted_memories[:self.MAX_MEMORIES]
    
    def _format_memory_context(self, memories: List[Dict[str, Any]]) -> str:
        """Format memories into a clean, structured context"""
        if not memories:
            return ""
        
        context_lines = ["User Memory Context:"]
        
        for mem_item in memories:
            memory = mem_item.get('memory', {})
            mem_type = memory.get('type', 'unknown').capitalize()
            key = memory.get('key', '').replace('_', ' ').title()
            value = memory.get('value', '')
            
            # Format: [Type] Key: Value
            context_lines.append(f"- [{mem_type}] {key}: {value}")
        
        return "\n".join(context_lines)
    
    def estimate_token_count(self, text: str) -> int:
        """Rough estimation of token count (1 token ≈ 4 characters)"""
        return len(text) // 4
    
    def get_context_size(self, system_prompt: str, user_prompt: str) -> int:
        """Estimate total context size in tokens"""
        return self.estimate_token_count(system_prompt) + self.estimate_token_count(user_prompt)
