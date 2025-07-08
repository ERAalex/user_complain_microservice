import httpx
from src.config import SENTIMENT_API_URL, APILAYER_API_KEY, IP_API_URL, AI_URL, AI_KEY, OPEN_AI_KEY
import openai
from openai import OpenAIError


class ExternalServiceClient:
    def __init__(self):
        self.sentiment_api_url = SENTIMENT_API_URL
        self.sentiment_api_key = APILAYER_API_KEY
        self.ip_api_url = IP_API_URL
        self.ai_url = AI_URL
        self.ai_key = AI_KEY
        self.open_ai_key = OPEN_AI_KEY

    async def analyze_sentiment(self, text: str) -> str:
        try:
            headers = {"apikey": self.sentiment_api_key}
            async with httpx.AsyncClient() as client:
                response = await client.post(self.sentiment_api_url, headers=headers, data=text.encode("utf-8"))
                response.raise_for_status()
                data = response.json()
                return data.get("sentiment", "unknown")
        except Exception as e:
            print(f"[Sentiment API Error] {e}")
            return "unknown"

    async def detect_country_by_ip(self, client_ip: str) -> str:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.ip_api_url}{client_ip}")
                response.raise_for_status()
                data = response.json()
                return data.get("country", "unknown")
        except Exception as e:
            print(f"[IP API Error] {e}")
            return "unknown"

    async def categorize_complaint(self, complaint: str) -> str:
        try:
            prompt = (
                f'Определи категорию жалобы: "{complaint}". '
                f'Варианты: техническая, оплата, другое. Ответ только одним словом.'
            )
            headers = {
                'Authorization': f'Bearer {self.ai_key}',
                'Content-Type': 'application/json'
            }
            data = {
                "model": "deepseek/deepseek-chat:free",
                "messages": [{"role": "user", "content": prompt}]
            }

            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(self.ai_url, json=data, headers=headers)
                response.raise_for_status()
                result = response.json()
                category = result['choices'][0]['message']['content'].strip().lower()
                return category if category in ["техническая", "оплата", "другое"] else "другое"
        except Exception as e:
            print(f"[AI Categorization Error] {e}")
            return "другое"

    async def categorize_complaint_open_ai(self, complaint: str) -> str:
        try:
            prompt = (
                f'Определи категорию жалобы: "{complaint}". '
                f'Варианты: техническая, оплата, другое. Ответ только одним словом.'
            )

            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                timeout=10
            )

            category = response.choices[0].message['content'].strip().lower()
            return category if category in ["техническая", "оплата", "другое"] else "другое"
        except Exception as e:
            print(f"[OpenAI Categorization Error] {e}")
            return "другое"
