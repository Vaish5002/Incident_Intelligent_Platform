"""
Test script to check Groq API key
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from groq import Groq
from backend.ai.config import settings

print("=" * 60)
print("Testing Groq API Key")
print("=" * 60)

if not settings.GROQ_API_KEY:
    print("❌ Error: GROQ_API_KEY is not set in backend/.env")
    sys.exit(1)

print(f"API Key: {settings.GROQ_API_KEY[:10]}...{settings.GROQ_API_KEY[-10:] if len(settings.GROQ_API_KEY) > 10 else ''}")
print(f"Model: {settings.GROQ_MODEL}")
print()

try:
    # Configure with API key
    client = Groq(api_key=settings.GROQ_API_KEY)
    print("✅ Groq client initialized")
    
    # Try a simple chat completion
    print("\nAttempting to generate a simple chat completion...")
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Hello, is this key active? Keep response to one sentence.",
            }
        ],
        model=settings.GROQ_MODEL,
        max_tokens=50,
    )
    print("\n✅ Success!")
    print(f"Response: {completion.choices[0].message.content}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nThis could mean:")
    print("1. API key is invalid")
    print("2. API key doesn't have proper permissions")
    print("3. You need to get a key from: https://console.groq.com/")
    print("\nNote: Groq API keys typically start with 'gsk_'")
    print(f"Your key starts with: {settings.GROQ_API_KEY[:10]}")
