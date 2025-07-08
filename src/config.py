from dotenv import load_dotenv
import os

load_dotenv()

APILAYER_API_KEY = os.getenv("APILAYER_API_KEY")
SENTIMENT_API_URL = os.getenv("SENTIMENT_API_URL")
IP_API_URL = os.getenv("IP_API_URL")

AI_KEY = os.getenv("AI_KEY")
AI_URL = os.getenv("AI_URL")
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
