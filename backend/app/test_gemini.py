#testing if Gemini API call works

import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found. Check your .env file.")

genai.configure(api_key=api_key)

try:
    # try a newer model
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content("Say hello from Gemini 2.5 Flash!")
    print("✅ Gemini API response:", response.text)
except Exception as e:
    print("❌ API call failed:", e)
