import os
import json
from typing import Optional
from openai import OpenAI
from google import genai
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """Unified LLM client supporting OpenAI and Gemini"""
    
    def __init__(self):
        self.openai_client = self._init_openai()
        self.gemini_key = self._init_gemini()
        
    def _init_openai(self) -> Optional[OpenAI]:
        """Initialize OpenAI client if API key is available"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or "your_actual_api_key_here" in api_key or "sk-proj" not in api_key:
            return None
        return OpenAI(api_key=api_key)
    
    def _init_gemini(self) -> Optional[str]:
        """Get Gemini API key if available"""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or "your_gemini_key_here" in api_key:
            return None
        return api_key
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> str:
        """
        Generate response using available LLM provider
        
        Args:
            prompt: User prompt/query
            system_prompt: Optional system instructions
            temperature: Sampling temperature (0.0 - 1.0)
            
        Returns:
            Generated response text
        """
        # Try OpenAI first
        if self.openai_client:
            try:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})
                messages.append({"role": "user", "content": prompt})
                
                response = self.openai_client.chat.completions.create(
                    model="gpt-4o-mini",
                    temperature=temperature,
                    messages=messages
                )
                return response.choices[0].message.content
            except Exception as e:
                print(f"[LLMClient] OpenAI failed: {e}")
        
        # Try Gemini as fallback
        if self.gemini_key:
            try:
                client = genai.Client(api_key=self.gemini_key)
                full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
                
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=full_prompt
                )
                return response.text
            except Exception as e:
                print(f"[LLMClient] Gemini failed: {e}")
        
        # Fallback response if no LLM available
        return "I apologize, but I'm currently unable to process your request. Please try again later."
    
    def is_available(self) -> bool:
        """Check if any LLM provider is available"""
        return self.openai_client is not None or self.gemini_key is not None
