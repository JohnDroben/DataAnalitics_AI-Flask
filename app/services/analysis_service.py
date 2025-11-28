from ..api.giga_chat import GigaChatAPI
from ..api.proxy_api import ProxyAPI
from ..processors.parser_factory import get_parser
from ..utils.pdf_generator import generate_txt_report
from ..utils.logger import logger
import pandas as pd
import os
from dotenv import load_dotenv
from typing import Optional

# Try to import official gigachat client (used in working bot)
try:
    from gigachat import GigaChat
    from gigachat.models import Chat, Messages
    _HAS_GIGACHAT_LIB = True
except Exception:
    _HAS_GIGACHAT_LIB = False


class AnalysisService:
    def __init__(self):
        logger.info("Initializing AnalysisService")
        try:
            logger.info("  - Initializing GigaChat API...")
            self.giga_api = GigaChatAPI()
            logger.info("  ✅ GigaChat API initialized")
        except Exception as e:
            logger.error(f"  ❌ Failed to initialize GigaChat API: {e}")
            self.giga_api = None
            
        try:
            logger.info("  - Initializing Proxy API...")
            self.proxy_api = ProxyAPI()
            logger.info("  ✅ Proxy API initialized")
        except Exception as e:
            logger.error(f"  ❌ Failed to initialize Proxy API: {e}")
            self.proxy_api = None
        
        # Try to initialize official gigachat library client (prefer it)
        self.gigachat_client = None
        if _HAS_GIGACHAT_LIB:
            try:
                load_dotenv()
                # Prefer explicit GIGACHAT_CREDENTIALS, but fall back to GIGACHAT_TOKEN
                creds = os.getenv('GIGACHAT_CREDENTIALS') or os.getenv('GIGACHAT_TOKEN')
                used_var = 'GIGACHAT_CREDENTIALS' if os.getenv('GIGACHAT_CREDENTIALS') else ('GIGACHAT_TOKEN' if os.getenv('GIGACHAT_TOKEN') else None)
                if creds:
                    logger.info(f"  - Initializing gigachat library client (using {used_var})...")
                    # verify_ssl_certs kept False to match bot behavior (dev only)
                    self.gigachat_client = GigaChat(credentials=creds, verify_ssl_certs=False)
                    logger.info("  ✅ gigachat library client initialized")
                else:
                    logger.debug("  No GIGACHAT_CREDENTIALS found for gigachat library client")
            except Exception as e:
                logger.error(f"  ❌ Failed to initialize gigachat library client: {e}")

    def analyze_file(self, file_path, session_id=None):
        logger.info(f"Starting file analysis for: {file_path}")
        logger.info(f"  File exists: {os.path.exists(file_path)}")
        logger.info(f"  File size: {os.path.getsize(file_path) if os.path.exists(file_path) else 'N/A'} bytes")
        
        # Определение типа файла
        ext = file_path.split('.')[-1].lower()
        logger.info(f"  File extension: .{ext}")

        # Парсинг файла
        try:
            logger.info(f"  🔍 Getting parser for extension: .{ext}")
            parser = get_parser(ext)
            logger.info(f"  ✅ Parser obtained: {parser.__class__.__name__}")
            
            logger.info("  📄 Parsing file...")
            data = parser.parse(file_path)
            logger.info(f"  ✅ File parsed successfully")
            logger.info(f"     Data type: {type(data).__name__}")
            
            if isinstance(data, pd.DataFrame):
                logger.info(f"     Rows: {len(data)}")
                logger.info(f"     Columns: {list(data.columns)}")
            else:
                logger.info(f"     Data length: {len(str(data)) if isinstance(data, str) else 'N/A'}")
                
        except ValueError as e:
            logger.error(f"  ❌ ValueError during parsing: {e}", exc_info=True)
            raise e
        except Exception as e:
            logger.error(f"  ❌ Unexpected error during parsing: {type(e).__name__}: {e}", exc_info=True)
            raise e

        # Подготовка данных для анализа
        if isinstance(data, pd.DataFrame):
            data_for_api = data.to_string()
            logger.info(f"  📊 Data converted to string for API (length: {len(data_for_api)} chars)")
        else:
            data_for_api = str(data)
            logger.info(f"  📊 Data prepared for API (length: {len(data_for_api)} chars)")

        # Анализ через GigaChat (предпочтительно через официальную библиотеку)
        giga_result = None
        if self.gigachat_client:
            try:
                logger.info("  🤖 Sending request to GigaChat via library client...")
                giga_result = self._call_gigachat_lib(data_for_api, session_id=session_id)
                logger.info(f"  ✅ GigaChat (lib) analysis complete (result length: {len(str(giga_result))} chars)")
            except Exception as e:
                logger.error(f"  ❌ GigaChat library error: {type(e).__name__}: {e}", exc_info=True)
                giga_result = f"Error: {str(e)}"
        elif self.giga_api:
            try:
                logger.info("  🤖 Sending request to GigaChat API (wrapper)...")
                giga_result = self.giga_api.send_analysis_request(data_for_api, session_id=session_id)
                logger.info(f"  ✅ GigaChat analysis complete (result length: {len(str(giga_result))} chars)")
            except Exception as e:
                logger.error(f"  ❌ GigaChat API error: {type(e).__name__}: {e}", exc_info=True)
                giga_result = f"Error: {str(e)}"
        else:
            logger.warning("  ⚠️ GigaChat API not initialized, skipping")
            giga_result = "GigaChat API not available"

        # Анализ через Proxy API
        proxy_result = None
        if self.proxy_api:
            try:
                logger.info("  🤖 Sending request to Proxy API...")
                proxy_result = self.proxy_api.send_analysis_request(data_for_api)
                logger.info(f"  ✅ Proxy API analysis complete (result length: {len(str(proxy_result))} chars)")
            except Exception as e:
                logger.error(f"  ❌ Proxy API error: {type(e).__name__}: {e}", exc_info=True)
                proxy_result = f"Error: {str(e)}"
        else:
            logger.warning("  ⚠️ Proxy API not initialized, skipping")
            proxy_result = "Proxy API not available"

        # Генерация отчета
        try:
            logger.info("  📝 Generating report...")
            report_path = generate_txt_report(giga_result, proxy_result)
            logger.info(f"  ✅ Report generated at: {report_path}")
        except Exception as e:
            logger.error(f"  ❌ Failed to generate report: {e}", exc_info=True)
            report_path = None

        logger.info("✅ File analysis completed successfully")
        return {
            "giga_result": giga_result,
            "proxy_result": proxy_result,
            "report_path": report_path,
            "data": data
        }

    def analyze_table_first_rows(self, data, rows_count=15, session_id=None):
        """
        Анализирует первые N строк таблицы через нейросети.
        
        Args:
            data: DataFrame или список словарей/строк с данными таблицы
            rows_count: количество строк для анализа (по умолчанию 15)
            
        Returns:
            dict с результатами анализа от GigaChat и Proxy API
        """
        logger.info(f"Starting table analysis with first {rows_count} rows")
        logger.debug(f"  Data type: {type(data).__name__}")
        
        # Преобразуем данные в DataFrame если нужно
        if isinstance(data, list):
            try:
                df = pd.DataFrame(data)
                logger.debug(f"  Converted list to DataFrame")
            except Exception as e:
                logger.error(f"  ❌ Failed to convert list to DataFrame: {e}")
                raise ValueError(f"Cannot convert data to DataFrame: {e}")
        elif isinstance(data, pd.DataFrame):
            df = data
        else:
            logger.error(f"  ❌ Unsupported data type: {type(data).__name__}")
            raise ValueError(f"Unsupported data type. Expected DataFrame or list, got {type(data).__name__}")
        
        logger.debug(f"  Total rows in DataFrame: {len(df)}")
        logger.debug(f"  Columns: {list(df.columns)}")
        
        # Берем первые N строк
        first_rows = df.head(rows_count)
        logger.info(f"  Selected first {len(first_rows)} rows for analysis")
        
        # Преобразуем в строку для отправки в API
        table_data_str = first_rows.to_string(index=False)
        logger.debug(f"  Table data converted to string (length: {len(table_data_str)} chars)")
        
        # Формируем системный промпт
        system_prompt = f"""Ты - аналитическая система с большим опытом. Твоя задача - анализировать табличные данные, делать выводы и находить аномалии или интересные тенденции.

Вот первые {rows_count} строк таблицы:

{table_data_str}

Проанализируй эти данные, выдели ключевые особенности, найди закономерности, аномалии и интересные тенденции. Предоставь краткий, но информативный анализ."""
        
        logger.debug(f"  System prompt created (length: {len(system_prompt)} chars)")
        logger.info("  Sending requests to neural networks...")
        
        results = {
            "giga_result": None,
            "proxy_result": None,
            "errors": {}
        }
        
        # Анализ через GigaChat (предпочтительно через библиотеку)
        if self.gigachat_client:
            try:
                logger.info("  🤖 Sending request to GigaChat via library client...")
                results["giga_result"] = self._call_gigachat_lib(system_prompt, session_id=session_id)
                logger.info(f"  ✅ GigaChat (lib) analysis complete (result length: {len(str(results['giga_result']))} chars)")
            except Exception as e:
                logger.error(f"  ❌ GigaChat library error: {type(e).__name__}: {e}", exc_info=True)
                results["giga_result"] = None
                results["errors"]["giga_chat"] = str(e)
        elif self.giga_api:
            try:
                logger.info("  🤖 Sending request to GigaChat API (wrapper)...")
                results["giga_result"] = self.giga_api.send_analysis_request(system_prompt, session_id=session_id)
                logger.info(f"  ✅ GigaChat analysis complete (result length: {len(str(results['giga_result']))} chars)")
            except Exception as e:
                logger.error(f"  ❌ GigaChat API error: {type(e).__name__}: {e}", exc_info=True)
                results["giga_result"] = None
                results["errors"]["giga_chat"] = str(e)
        else:
            logger.warning("  ⚠️ GigaChat API not initialized")
            results["errors"]["giga_chat"] = "GigaChat API not initialized"

        # Анализ через Proxy API
        if self.proxy_api:
            try:
                logger.info("  🤖 Sending request to Proxy API...")
                results["proxy_result"] = self.proxy_api.send_analysis_request(system_prompt)
                logger.info(f"  ✅ Proxy API analysis complete (result length: {len(str(results['proxy_result']))} chars)")
            except Exception as e:
                logger.error(f"  ❌ Proxy API error: {type(e).__name__}: {e}", exc_info=True)
                results["proxy_result"] = None
                results["errors"]["proxy_api"] = str(e)
        else:
            logger.warning("  ⚠️ Proxy API not initialized")
            results["errors"]["proxy_api"] = "Proxy API not initialized"
        
        logger.info("✅ Table analysis completed")
        return results

    def _call_gigachat_lib(self, prompt: str, session_id: Optional[str] = None):
        """Вызов GigaChat через официальный пакет `gigachat` (синхронный).

        При наличии `session_id` пытаемся установить его в клиентской context (если библиотека поддерживает).
        """
        if not _HAS_GIGACHAT_LIB or not self.gigachat_client:
            raise Exception("gigachat library client not available")

        # Если библиотека поддерживает context.session_id_cvar, попробуем установить
        if session_id:
            try:
                ctx = getattr(self.gigachat_client, "context", None)
                if ctx and hasattr(ctx, "session_id_cvar"):
                    try:
                        ctx.session_id_cvar.set(session_id)
                        logger.debug(f"Set gigachat client context.session_id_cvar to {session_id}")
                    except Exception:
                        logger.debug("Unable to set session_id on gigachat client context.session_id_cvar")

                # Также попытаемся установить через модульный контекст как в документации
                try:
                    import gigachat.context as _gctx
                    if hasattr(_gctx, 'session_id_cvar'):
                        try:
                            _gctx.session_id_cvar.set(session_id)
                            logger.debug(f"Set gigachat.context.session_id_cvar to {session_id}")
                        except Exception:
                            logger.debug("Unable to set session_id on gigachat.context.session_id_cvar")
                except Exception:
                    logger.debug("gigachat.context not available to set session_id")
            except Exception:
                logger.debug("gigachat client has no context/session_id_cvar attribute")

        # Build simple chat with system + user messages
        try:
            messages = [
                Messages(role="system", content="Ты - профессиональный аналитик данных. Твоя задача - анализировать табличные данные и предоставлять краткие, информативные выводы."),
                Messages(role="user", content=f"Проанализируй следующие данные:\n{prompt}")
            ]

            chat = Chat(messages=messages, temperature=0.7, max_tokens=1000)
            resp = self.gigachat_client.chat(chat)
            # Expect similar structure as in bot: resp.choices[0].message.content
            try:
                return resp.choices[0].message.content
            except Exception:
                # Fallback: try to convert to string
                return str(resp)
        except Exception as e:
            logger.error(f"Error calling gigachat lib: {e}", exc_info=True)
            raise