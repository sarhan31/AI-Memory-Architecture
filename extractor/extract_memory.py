import json
import os
import time
import re
from google import genai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.strip() == "" or "your_actual_api_key_here" in api_key or "sk-proj" not in api_key:
        return None
    return OpenAI(api_key=api_key)

def get_gemini_key():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or "your_gemini_key_here" in api_key:
        return None
    return api_key

def mock_llm_extraction(chat_history, prompt):
    print("\n[Mock LLM] API Key missing or call failed. Using rule-based mock...")
    
    memories = []
    chat_text = json.dumps(chat_history)
    
    # Mock logic based on keywords in the simulated chat
    if "Sarah" in chat_text:
        memories.append({
            "type": "fact",
            "key": "user_name",
            "value": "Sarah",
            "confidence": 0.95,
            "action": "add"
        })
    if "Tokyo" in chat_text:
        memories.append({
            "type": "fact",
            "key": "location",
            "value": "Tokyo",
            "confidence": 0.90,
            "action": "add"
        })
    if "email" in chat_text:
        memories.append({
            "type": "preference",
            "key": "notification_preference",
            "value": "email",
            "confidence": 0.90,
            "action": "add"
        })
    if "after 9 PM" in chat_text:
        memories.append({
            "type": "constraint",
            "key": "no_calls_time_range",
            "value": "after 9 PM",
            "confidence": 0.85,
            "action": "add"
        })
            
    return {"memories": memories}

def extract_with_gemini(chat_history, prompt, api_key):
    """Uses Google Gemini API for extraction with retry logic."""
    print("\n[LLM] Attempting to process chat history with Google Gemini...")
    client = genai.Client(api_key=api_key)
    
    conversation_text = json.dumps(chat_history, indent=2)
    full_prompt = f"{prompt}\n\nHere is the chat history:\n{conversation_text}"
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            # Add a small delay before the first attempt if it's not the first run,
            # to be nice to the rate limiter.
            if attempt > 0:
                 pass 

            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=full_prompt,
                config={
                    'response_mime_type': 'application/json'
                }
            )
            return json.loads(response.text)
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                print(f"[Warning] Gemini Rate Limit hit (Attempt {attempt+1}/{max_retries}).")
                
                # Try to extract wait time
                wait_time = 10  # Default wait
                match = re.search(r"retry in (\d+(\.\d+)?)s", error_str)
                if match:
                    wait_time = float(match.group(1)) + 5 # Add 5s buffer to be safe
                
                if attempt < max_retries - 1:
                    print(f"Waiting {wait_time:.1f}s before retrying...")
                    time.sleep(wait_time)
                else:
                    print("[Error] Max retries exceeded for Gemini.")
            else:
                print(f"[Warning] Gemini call failed: {e}")
                break
    return None

def extract_memory_from_chat(chat_path, prompt_path):
    """
    Reads chat and prompt files, then attempts extraction via:
    1. OpenAI (if configured)
    2. Google Gemini (if configured)
    3. Mock Fallback
    """
    # Read files
    try:
        with open(chat_path, 'r', encoding='utf-8') as f:
            chat_history = json.load(f)
        with open(prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = f.read()
    except Exception as e:
        print(f"Error reading files: {e}")
        return {"memories": []}

    # 1. Try OpenAI
    client = get_openai_client()
    if client:
        print("\n[LLM] Attempting to process chat history with OpenAI...")
        try:
            conversation_text = json.dumps(chat_history, indent=2)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": conversation_text}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"[Warning] OpenAI call failed: {e}")
            # Don't return yet, try next provider
            pass

    # 2. Try Google Gemini (Free Tier available)
    gemini_key = get_gemini_key()
    if gemini_key:
        result = extract_with_gemini(chat_history, system_prompt, gemini_key)
        if result:
            return result

    # 3. Fallback to Mock
    if not client and not gemini_key:
         print("\n[Warning] No valid API keys found (OpenAI or Gemini).")
    
    return mock_llm_extraction(chat_history, system_prompt)
