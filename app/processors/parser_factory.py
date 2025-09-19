from abc import ABC, abstractmethod

class FileParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> str:
        pass

class ExcelParser(FileParser):
    def parse(self, file_path: str) -> str:
        # реализация
        pass

class CSVParser(FileParser):
    def parse(self, file_path: str) -> str:
        # реализация
        pass

class PDFParser(FileParser):
    def parse(self, file_path: str) -> str:
        # реализация
        pass

def get_parser(file_type: str) -> FileParser:
    parsers = {
        'xlsx': ExcelParser(),
        'csv': CSVParser(),
        'pdf': PDFParser()
    }
    return parsers.get(file_type.lower(), ExcelParser())