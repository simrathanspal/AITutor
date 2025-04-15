import logging
from abc import ABC, abstractmethod
from typing import Any

logger = logging.getLogger(__name__)


class DataExporter(ABC):
    """Abstract base class for data exporters"""

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    @abstractmethod
    def export(self, data: Any, filename: str) -> None:
        """Export data to a file"""
        pass