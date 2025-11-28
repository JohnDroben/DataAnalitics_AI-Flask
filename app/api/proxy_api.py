import os
import requests
from dotenv import load_dotenv
from ..utils.logger import logger


class ProxyAPI:
    def __init__(self):
        logger.info("Initializing ProxyAPI")
        load_dotenv()
        self.api_key = os.getenv('PROXY_API_KEY')
        logger.debug(f"  API Key loaded: {bool(self.api_key)}")
        if not self.api_key:
            logger.warning("  ⚠️ PROXY_API_KEY not found in environment variables!")
        self.base_url = "https://api.proxy.ai/analyze"
        logger.info(f"  Base URL: {self.base_url}")

    def send_analysis_request(self, data):
        logger.info(f"Sending analysis request to ProxyAPI (data size: {len(data)} chars)")
        
        if not self.api_key:
            error_msg = "No API key available"
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "query": f"Проанализируй следующие данные:\n{data}"
        }

        logger.debug(f"Request URL: {self.base_url}")
        logger.debug(f"Payload size: {len(str(payload))} chars")
        
        try:
            logger.info("Sending POST request to ProxyAPI...")
            # Временно отключаем проверку SSL-сертификата. Внимание: это небезопасно!
            response = requests.post(self.base_url, headers=headers, json=payload, verify=False, timeout=30)
            logger.info(f"Response status: {response.status_code}")
            return self._process_response(response)
        except requests.Timeout:
            error_msg = "ProxyAPI request timeout"
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)
        except Exception as e:
            logger.error(f"❌ Request failed: {type(e).__name__}: {e}", exc_info=True)
            raise

    def _process_response(self, response):
        logger.debug(f"Processing response: status={response.status_code}")
        if response.status_code == 200:
            logger.info("✅ ProxyAPI response received successfully")
            result = response.json()['result']
            logger.debug(f"Response content length: {len(str(result))} chars")
            return result
        else:
            error_msg = f"ProxyAPI error: {response.text}"
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)