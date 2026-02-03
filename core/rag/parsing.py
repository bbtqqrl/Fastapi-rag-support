from io import BytesIO
from pypdf import PdfReader
from abc import ABC, abstractmethod

class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_bytes: bytes) -> str:
        pass

class PDFParser(BaseParser):
    def parse(self, file_bytes: bytes) -> str:
        reader = PdfReader(BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    
class TextParser(BaseParser):
    def parse(self, file_bytes: bytes) -> str:
        return file_bytes.decode("utf-8", errors="ignore")
    
PARSERS = {
    "pdf": PDFParser,
    "txt": TextParser,
}

def create_parser(extension: str) -> BaseParser:
    extension = extension.lower()
    if extension not in PARSERS:
        raise ValueError(f"Unsupported file type: {extension}")
    return PARSERS[extension]()
