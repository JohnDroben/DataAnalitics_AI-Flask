import os
import requests
from dotenv import load_dotenv


class GigaChatAPI:
    def __init__(self):
        load_dotenv()
        self.token = os.getenv('GIGACHAT_TOKEN')
        self.base_url = "https://api.gigachat.ru/v1/chat/completions"

    def send_analysis_request(self, data):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "GigaChat",
            "messages": [
                {
                    "role": "user",
                    "content": f"Проанализируй следующие данные:\n{data}"
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }

        response = requests.post(self.base_url, headers=headers, json=payload)
        return self._process_response(response)

    def _process_response(self, response):
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            raise Exception(f"GIGAChat error: {response.text}")