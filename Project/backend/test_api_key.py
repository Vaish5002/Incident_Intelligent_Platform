"""
Test script to check API key and list available models
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import google.generativeai as genai
from backend.ai.config import settings

print("=" * 60)
print("Testing Gemini API Key")
print("=" * 60)

print(f"API Key: {settings.GEMINI_API_KEY[:20]}...{settings.GEMINI_API_KEY[-10:]}")
print()

try:
    # Configure with API key
    genai.configure(api_key=settings.GEMINI_API_KEY)
    print("✅ API key configured")
    
    # Try to list available models
    print("\nAttempting to list available models...")
    models = genai.list_models()
    
    print("\n✅ Available Models:")
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - {model.name}")
            print(f"    Display: {model.display_name}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nThis could mean:")
    print("1. API key is invalid")
    print("2. API key doesn't have proper permissions")
    print("3. You need to get a key from: https://makersuite.google.com/app/apikey")
    print("\nNote: Gemini API keys typically start with 'AIzaSy...'")
    print(f"Your key starts with: {settings.GEMINI_API_KEY[:10]}")
