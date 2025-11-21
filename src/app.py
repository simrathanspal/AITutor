import os
import logging
from typing import Dict, Any, Optional

from src.scrapers.base import WebScraper
from src.scrapers.w3schools import W3SchoolsScraper
from src.exporters.json_exporter import JsonExporter
from src.exporters.csv_exporter import CsvExporter

logger = logging.getLogger(__name__)


class ScraperApplication:
    """Main application that coordinates scraping and exporting"""

    def __init__(self, scraper: WebScraper):
        self.scraper = scraper
        self.json_exporter = JsonExporter()
        self.csv_exporter = CsvExporter()

    def run(self, output_dir: str = "data") -> Dict[str, Any]:
        """Run the scrapers and export the data"""
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Run the scrapers
        if isinstance(self.scraper, W3SchoolsScraper):
            try:
                logger.info(f"Starting scrapers application with output directory: {output_dir}")
                course_data = self.scraper.scrape_course()

                # Export full course data to JSON
                json_filename = os.path.join(output_dir, "tutorial_course.json")
                self.json_exporter.export(course_data, json_filename)

                # Export modules to CSV
                modules_filename = os.path.join(output_dir, "tutorial_modules.csv")
                self.csv_exporter.export(course_data.modules, modules_filename)

                # Export tutorial titles and URLs to CSV
                tutorial_info = [
                    {"title": t.title, "url": t.url} for t in course_data.tutorials
                ]
                tutorials_filename = os.path.join(output_dir, "tutorial_info.csv")
                self.csv_exporter.export(tutorial_info, tutorials_filename, ["title", "url"])

                logger.info("Scraping and exporting completed successfully")
                return course_data.dict()
            except Exception as e:
                logger.error(f"Error in scrapers application: {e}")
                raise
        else:
            logger.error("Unsupported scrapers type")
            raise ValueError("Unsupported scrapers type")