import json
import logging
from typing import Any

from pydantic import BaseModel
from src.exporters.base import DataExporter

logger = logging.getLogger(__name__)


class JsonExporter(DataExporter):
    """JSON data exporter"""

    def export(self, data: Any, filename: str) -> None:
        """Export data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                if isinstance(data, BaseModel):
                    json.dump(data.dict(), f, indent=4, ensure_ascii=False)
                else:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            self.logger.info(f"Data exported to {filename}")
        except Exception as e:
            self.logger.error(f"Error exporting data to {filename}: {e}")
            raise