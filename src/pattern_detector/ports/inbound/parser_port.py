from abc import ABC, abstractmethod
from typing import List
from ...domain.code_model import RubyFile, CodeModel


class RubyParserPort(ABC):
    @abstractmethod
    def parse_file(self, file_path: str, content: str) -> RubyFile:
        pass

    @abstractmethod
    def parse_code_model(self, paths: List[str]) -> CodeModel:
        pass
