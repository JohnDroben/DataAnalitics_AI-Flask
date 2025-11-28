import os
import requests
import base64
import uuid
from dotenv import load_dotenv
from ..utils.logger import logger


class GigaChatAPI:
    def __init__(self):
        logger.info("Initializing GigaChatAPI")
        load_dotenv()
        self.auth_token = os.getenv('GIGACHAT_TOKEN')
        logger.debug(f"  Token loaded: {bool(self.auth_token)}")
        if not self.auth_token:
            logger.warning("  ⚠️ GIGACHAT_TOKEN not found in environment variables!")
        self.access_token = None
        # Allow overriding base URL via env var; default to official GigaChat endpoint
        self.base_url = os.getenv('GIGACHAT_BASE_URL', 'https://gigachat.devices.sberbank.ru/api/v1')
        logger.info(f"  Base URL: {self.base_url}")
        self._get_access_token()

    def _get_access_token(self):
        """Получить access token для GigaChat API"""
        logger.info("Attempting to get access token...")
        # First, if the official `gigachat` python package is installed, try to use it to get a token
        try:
            from gigachat import GigaChat
            if self.auth_token:
                logger.debug("gigachat library detected — attempting to get token via library")
                try:
                    giga = GigaChat(credentials=self.auth_token, verify_ssl_certs=False)
                    # Some SDKs expose `get_token()` to exchange credentials for access token
                    if hasattr(giga, 'get_token'):
                        token_resp = giga.get_token()
                        # token_resp may be dict-like
                        if isinstance(token_resp, dict):
                            self.access_token = token_resp.get('access_token')
                        else:
                            # try attribute
                            self.access_token = getattr(token_resp, 'access_token', None)
                        if self.access_token:
                            logger.info("✅ Access token obtained via gigachat library")
                            return
                except Exception as e:
                    logger.debug(f"gigachat library token exchange failed: {e}")
        except Exception:
            logger.debug("gigachat library not available for token exchange")

        # Fallback: if a pre-obtained token is provided in GIGACHAT_TOKEN, use it
        if self.auth_token:
            logger.info("Using provided GIGACHAT_TOKEN as access token fallback")
            self.access_token = self.auth_token
            return

        # As a last resort, try the OAuth endpoint if configured (keep for compatibility)
        auth_url = os.getenv('GIGACHAT_OAUTH_URL', 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth')
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "RqUID": str(uuid.uuid4())
        }
        try:
            logger.debug(f"Sending OAuth request to: {auth_url}")
            payload = "scope=GIGACHAT_API_PERS"
            response = requests.post(auth_url, headers=headers, data=payload, verify=False, timeout=10)
            logger.debug(f"OAuth response status: {response.status_code}")
            logger.debug(f"OAuth response: {response.text[:200]}")
            if response.status_code == 200:
                token_data = response.json()
                self.access_token = token_data.get('access_token')
                if self.access_token:
                    logger.info("✅ Access token obtained via OAuth endpoint")
                    return
            logger.warning(f"OAuth fallback failed with status {response.status_code}: {response.text[:500]}")
        except Exception as e:
            logger.warning(f"OAuth fallback failed: {e}")

    def send_analysis_request(self, data, session_id=None):
        logger.info(f"Sending analysis request to GigaChat (data size: {len(data)} chars) session_id={session_id}")
        
        if not self.access_token:
            logger.info("No access token, attempting to obtain...")
            self._get_access_token()
        
        if not self.access_token:
            error_msg = "No access token available"
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)
            
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "RqUID": str(uuid.uuid4())
        }
        if session_id is not None:
            headers["X-Session-ID"] = session_id

        # Пробуем разные модели
        models = ["GigaChat", "GigaChat-Pro", "GigaChat-3.5"]
        
        payload = {
            "model": "GigaChat",
            "messages": [
                {
                    "role": "system",
                    "content": "Ты - профессиональный аналитик данных. Твоя задача - анализировать табличные данные и предоставлять краткие, информативные выводы."
                },
                {
                    "role": "user",
                    "content": f"Проанализируй следующие данные:\n{data}"
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }

        url = f"{self.base_url}/chat/completions"
        logger.debug(f"Request URL: {url}")
        logger.debug(f"Payload size: {len(str(payload))} chars")
        logger.debug(f"Headers: Authorization={bool(headers.get('Authorization'))}, RqUID={headers.get('RqUID')}")
        
        try:
            logger.info("Sending POST request to GigaChat API...")
            # Временно отключаем проверку SSL-сертификата. Внимание: это небезопасно!
            response = requests.post(url, headers=headers, json=payload, verify=False, timeout=30)
            logger.info(f"Response status: {response.status_code}")
            logger.debug(f"Response headers: {dict(response.headers)}")
            
            # Логируем часть ответа для отладки
            if response.status_code != 200:
                logger.debug(f"Response body (first 500 chars): {response.text[:500]}")
            
            return self._process_response(response)
        except requests.Timeout:
            error_msg = "GigaChat API request timeout"
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)
        except Exception as e:
            logger.error(f"❌ Request failed: {type(e).__name__}: {e}", exc_info=True)
            raise

    def _process_response(self, response):
        logger.debug(f"Processing response: status={response.status_code}")
        if response.status_code == 200:
            logger.info("✅ GigaChat response received successfully")
            result = response.json()['choices'][0]['message']['content']
            logger.debug(f"Response content length: {len(str(result))} chars")
            return result
        else:
            error_msg = f"GIGAChat error: {response.text}"
            logger.error(f"❌ {error_msg}")
            raise Exception(error_msg)