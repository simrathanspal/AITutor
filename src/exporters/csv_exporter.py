import csv
import logging
from typing import List, Dict, Any

from pydantic import BaseModel
from src.exporters.base import DataExporter

logger = logging.getLogger(__name__)


class CsvExporter(DataExporter):
    """CSV data exporter"""

    def export(self, data: List[Dict], filename: str, fields: List[str] = None) -> None:
        """Export data to CSV file"""
        if not data:
            self.logger.warning("No data to export")
            return

        try:
            # Determine fields if not provided
            if not fields and data:
                if isinstance(data[0], BaseModel):
                    fields = list(data[0].dict().keys())
                else:
                    fields = list(data[0].keys())

            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()

                for item in data:
                    if isinstance(item, BaseModel):
                        writer.writerow(item.dict())
                    else:
                        writer.writerow(item)

            self.logger.info(f"Data exported to {filename}")
        except Exception as e:
            self.logger.error(f"Error exporting data to {filename}: {e}")
            raise