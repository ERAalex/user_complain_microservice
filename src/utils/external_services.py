import requests
from requests.exceptions import RequestException
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

    def analyze_sentiment(self, text: str) -> str:
        try:
            headers = {"apikey": self.sentiment_api_key}
            payload = text.encode("utf-8")

            response = requests.post(self.sentiment_api_url, headers=headers, data=payload)
            response.raise_for_status()
            data = response.json()
            sentiment = data.get("sentiment", "unknown")

            return sentiment if sentiment in ["positive", "neutral", "negative"] else "unknown"
        except RequestException as e:
            print(f"[Sentiment API Error] {e}")
            return "unknown"
        except Exception as e:
            print(f"[Internal Error] {e}")
            raise

    def detect_country_by_ip(self, client_ip: str) -> str:
        try:
            url = self.ip_api_url + client_ip
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            return data.get("country", "unknown")
        except RequestException as e:
            print(f"[IP API Error] {e}")
            return "unknown"
        except Exception as e:
            print(f"[Internal Error] {e}")
            raise

    def categorize_complaint(self, complaint: str) -> str:
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

            response = requests.post(self.ai_url, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            response_data = response.json()

            category = response_data['choices'][0]['message']['content'].strip().lower()
            return category if category in ["техническая", "оплата", "другое"] else "другое"
        except (RequestException, KeyError, IndexError, TypeError) as e:
            print(f"[AI Categorization Error] {e}")
            return "другое"

    def categorize_complaint_open_ai(self, complaint: str) -> str:
        try:
            prompt = (
                f'Определи категорию жалобы: "{complaint}". '
                f'Варианты: техническая, оплата, другое. Ответ только одним словом.'
            )

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                timeout=10
            )

            category = response.choices[0].message['content'].strip().lower()

            return category if category in ["техническая", "оплата", "другое"] else "другое"

        except (OpenAIError, KeyError, IndexError, TypeError) as e:
            print(f"[OpenAI Categorization Error] {e}")
            return "другое"
