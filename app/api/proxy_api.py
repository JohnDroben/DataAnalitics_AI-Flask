import os
import requests
from dotenv import load_dotenv


class ProxyAPI:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('PROXY_API_KEY')
        self.base_url = "https://api.proxy.ai/analyze"

    def send_analysis_request(self, data):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "query": f"Проанализируй следующие данные:\n{data}"
        }

        response = requests.post(self.base_url, headers=headers, json=payload)
        return self._process_response(response)

    def _process_response(self, response):
        if response.status_code == 200:
            return response.json()['result']
        else:
            raise Exception(f"ProxyAPI error: {response.text}")