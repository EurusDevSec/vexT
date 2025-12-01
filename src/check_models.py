import google.generativeai as genai
import os

GOOGLE_API_KEY = "AIzaSyDk_NRHbZtcy4LSe0veWvBcbqi6NiO90Rs"
genai.configure(api_key=GOOGLE_API_KEY)

print("Listing available models:")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"Error listing models: {e}")
