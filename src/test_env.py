from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("GEMINI_API_KEY")
print("Key loaded:" , key[:8], "...") # prints first 8 chars only — never print the full key