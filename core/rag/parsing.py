from io import BytesIO
from pypdf import PdfReader

def parse_file(filename: str, file_bytes: bytes) -> str:
    if filename.endswith(".pdf"):
        return _parse_pdf(file_bytes)
    return _parse_text(file_bytes)


def _parse_text(file_bytes: bytes) -> str:
    return file_bytes.decode("utf-8", errors="ignore")


def _parse_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(BytesIO(file_bytes))
    return "\n".join(page.extract_text() or "" for page in reader.pages)
