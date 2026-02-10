import os
import json
import requests
from typing import Optional
from dotenv import load_dotenv

# Try to import OpenAI and Gemini, but don't fail if not available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("[LLMClient] OpenAI not available (install with: pip install openai)")

try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("[LLMClient] Gemini not available (install with: pip install google-genai)")

load_dotenv()


class LLMClient:
    """Unified LLM client supporting OpenAI, Gemini, Ollama, and Local fallback"""
    
    def __init__(self):
        self.openai_client = self._init_openai()
        self.gemini_key = self._init_gemini()
        self.ollama_url = self._init_ollama()
        self.use_local_fallback = os.getenv("USE_LOCAL_FALLBACK", "true").lower() == "true"
        
    def _init_openai(self) -> Optional[object]:
        """Initialize OpenAI client if API key is available"""
        if not OPENAI_AVAILABLE:
            return None
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or "your_actual_api_key_here" in api_key or api_key.strip() == "":
            return None
        try:
            return OpenAI(api_key=api_key)
        except:
            return None
    
    def _init_gemini(self) -> Optional[str]:
        """Get Gemini API key if available"""
        if not GEMINI_AVAILABLE:
            return None
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or "your_gemini_key_here" in api_key or api_key.strip() == "":
            return None
        return api_key
    
    def _init_ollama(self) -> Optional[str]:
        """Check if Ollama is available locally"""
        ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        try:
            response = requests.get(f"{ollama_url}/api/tags", timeout=2)
            if response.status_code == 200:
                print(f"[LLMClient] Ollama detected at {ollama_url}")
                return ollama_url
        except:
            pass
        return None
    
    def _generate_with_ollama(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> Optional[str]:
        """Generate response using Ollama"""
        if not self.ollama_url:
            return None
        
        try:
            model = os.getenv("OLLAMA_MODEL", "llama2")
            full_prompt = f"{system_prompt}\n\nUser: {prompt}\n\nAssistant:" if system_prompt else prompt
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": full_prompt,
                    "temperature": temperature,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
        except Exception as e:
            print(f"[LLMClient] Ollama failed: {e}")
        
        return None
    
    def _generate_local_fallback(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Generate a simple rule-based response when no LLM is available"""
        prompt_lower = prompt.lower()
        
        # Extract potential name
        name = None
        if "i'm " in prompt_lower or "i am " in prompt_lower:
            words = prompt.split()
            for i, word in enumerate(words):
                if word.lower() in ["i'm", "i am", "im"]:
                    if i + 1 < len(words):
                        name = words[i + 1].strip(".,!?")
                        break
        
        # Extract potential location
        location = None
        if "from " in prompt_lower or "in " in prompt_lower or "live in" in prompt_lower:
            words = prompt.split()
            for i, word in enumerate(words):
                if word.lower() in ["from", "in"]:
                    if i + 1 < len(words):
                        location = words[i + 1].strip(".,!?")
                        break
        
        # Build response
        greeting = f"Hello{' ' + name if name else ''}! "
        
        if name and location:
            return f"{greeting}Nice to meet you! It's great to connect with someone from {location}. How can I help you today?"
        elif name:
            return f"{greeting}Nice to meet you! How can I assist you today?"
        elif location:
            return f"{greeting}It's great to connect with someone from {location}. How can I help you?"
        elif "hello" in prompt_lower or "hi" in prompt_lower:
            return "Hello! I'm your AI assistant with memory capabilities. How can I help you today?"
        elif "?" in prompt:
            return "That's an interesting question! I'm currently running in local mode without an external LLM. I can still help you manage and retrieve memories from our conversations."
        else:
            return "Thank you for your message! I'm currently running in local mode. I can help you store and retrieve information from our conversations. What would you like to know?"
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, temperature: float = 0.7) -> str:
        """
        Generate response using available LLM provider
        
        Priority order:
        1. OpenAI (if configured)
        2. Gemini (if configured)
        3. Ollama (if running locally)
        4. Local fallback (rule-based)
        
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
                print("[LLMClient] Using OpenAI")
                return response.choices[0].message.content
            except Exception as e:
                print(f"[LLMClient] OpenAI failed: {e}")
        
        # Try Gemini as fallback
        if self.gemini_key and GEMINI_AVAILABLE:
            try:
                client = genai.Client(api_key=self.gemini_key)
                full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
                
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=full_prompt
                )
                print("[LLMClient] Using Gemini")
                return response.text
            except Exception as e:
                print(f"[LLMClient] Gemini failed: {e}")
        
        # Try Ollama
        ollama_response = self._generate_with_ollama(prompt, system_prompt, temperature)
        if ollama_response:
            print("[LLMClient] Using Ollama")
            return ollama_response
        
        # Use local fallback
        if self.use_local_fallback:
            print("[LLMClient] Using local fallback (rule-based)")
            return self._generate_local_fallback(prompt, system_prompt)
        
        return "I apologize, but I'm currently unable to process your request. Please configure an LLM provider (OpenAI, Gemini, or Ollama)."
    
    def is_available(self) -> bool:
        """Check if any LLM provider is available"""
        return (self.openai_client is not None or 
                self.gemini_key is not None or 
                self.ollama_url is not None or
                self.use_local_fallback)
