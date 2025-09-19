from api.giga_chat import GigaChatAPI
from api.proxy_api import ProxyAPI
from processors.excel_parser import parse_excel
from processors.csv_parser import parse_csv
from processors.pdf_parser import parse_pdf
from utils.pdf_generator import generate_pdf_report


class AnalysisService:
    def __init__(self):
        self.giga_api = GigaChatAPI()
        self.proxy_api = ProxyAPI()

    def analyze_file(self, file_path):
        # Определение типа файла
        ext = file_path.split('.')[-1].lower()

        # Парсинг файла
        if ext == 'xlsx':
            data = parse_excel(file_path)
        elif ext == 'csv':
            data = parse_csv(file_path)
        elif ext == 'pdf':
            data = parse_pdf(file_path)
        else:
            raise ValueError("Неподдерживаемый формат файла")

        # Анализ через обе нейросети
        giga_result = self.giga_api.send_analysis_request(data)
        proxy_result = self.proxy_api.send_analysis_request(data)

        # Генерация PDF-отчета с двумя результатами
        report_path = generate_pdf_report(giga_result, proxy_result)

        return {
            "giga_result": giga_result,
            "proxy_result": proxy_result,
            "report_path": report_path
        }