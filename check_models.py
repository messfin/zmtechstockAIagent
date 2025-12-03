import google.generativeai as genai
import os
import toml
import sys

# Set encoding for output
sys.stdout.reconfigure(encoding='utf-8')

# Try to get API key from secrets.toml first
api_key = None
try:
    secrets = toml.load(".streamlit/secrets.toml")
    if "GOOGLE_API_KEY" in secrets:
        api_key = secrets["GOOGLE_API_KEY"]
except:
    pass

# Fallback to environment variable
if not api_key:
    api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("No API key found! Please check .streamlit/secrets.toml or .env")
    exit(1)

print(f"Found API Key: {api_key[:5]}...")

try:
    genai.configure(api_key=api_key)
    
    print("\nListing available models...")
    models = list(genai.list_models())
    
    found_generate = False
    print("\n--- Models supporting 'generateContent' ---")
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
            found_generate = True
            
    if not found_generate:
        print("No models found that support generateContent!")
        
except Exception as e:
    print(f"\nError listing models: {e}")
