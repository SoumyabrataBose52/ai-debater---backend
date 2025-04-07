import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_FACT_CHECK_API_KEY=("GOOGLE_FACT_CHECK_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Check your .env file.")
