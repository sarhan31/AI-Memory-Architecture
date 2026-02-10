import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ OPENAI_API_KEY not found in .env file")
else:
    print("✅ API Key found")

client = OpenAI(api_key=api_key)

try:
    response = client.models.list()
    print("✅ OpenAI API is working!")
except Exception as e:
    print("❌ OpenAI API failed:", e)
