from abc import ABC, abstractmethod
import re
from chonkie import SemanticChunker

class BaseChunker(ABC):
    @abstractmethod
    def chunk(self, text: str):
        pass


class SemanticTextChunker(BaseChunker):
    def __init__(
        self,
        embedding_model: str = "minishlab/potion-base-32M",
        threshold: float = 0.7,
        chunk_size: int = 2048,
        skip_window: int = 1
    ):
        self.chunker = SemanticChunker(
            embedding_model=embedding_model,
            threshold=threshold,
            chunk_size=chunk_size,
            skip_window=skip_window
        )
    
    def chunk(self, text: str):
        return [chunk.text for chunk in self.chunker.chunk(text)]


class FAQChunker(BaseChunker):
    def __init__(self):
        self.section_pattern = re.compile(r"^(\d+)\.\s+(.*)")
        self.question_pattern = re.compile(r"^(\d+\.\d+)\.\s+(.*)")
    
    def chunk(self, text: str):
        chunks = []
        current_section, current_question = None, None
        current_answer = []

        for line in map(str.strip, text.splitlines()):
            if not line:
                continue

            if self.section_pattern.match(line) and not self.question_pattern.match(line):
                current_section = self.section_pattern.match(line).group(2)
                continue

            if self.question_pattern.match(line):
                if current_question:
                    parts = [
                        f"{current_section}." if current_section else None,
                        f"{current_question}.",
                        " ".join(current_answer)
                    ]
                    chunks.append(" ".join(x for x in parts if x))
                current_question = self.question_pattern.match(line).group(2)
                current_answer = []
                continue

            current_answer.append(line)

        if current_question:
            parts = [
                f"{current_section}." if current_section else None,
                f"{current_question}.",
                " ".join(current_answer)
            ]
            chunks.append(" ".join(x for x in parts if x))
        return chunks


class ChunkerFactory:
    @staticmethod
    def create_chunker(chunker_type: str, **kwargs):
        chunkers = {
            "semantic": SemanticTextChunker,
            "faq": FAQChunker,
        }
        
        if chunker_type not in chunkers:
            raise ValueError(f"Unknown chunker type: {chunker_type}. Available: {list(chunkers.keys())}")
        
        return chunkers[chunker_type](**kwargs)