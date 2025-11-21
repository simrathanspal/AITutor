#!/usr/bin/env python
"""
Main entry point for the web scrapers application.
"""
import argparse
import logging
import sys

from src.scrapers.w3schools import W3SchoolsScraper
from src.app import ScraperApplication

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('scrapers.log')
    ]
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Web scrapers for tutorial websites')
    parser.add_argument(
        '--url',
        type=str,
        default="https://www.w3schools.com/nodejs/nodejs_intro.asp",
        help='Starting URL for the scrapers'
    )
    parser.add_argument(
        '--output',
        type=str,
        default="data/raw",
        help='Output directory for scraped data'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between requests in seconds'
    )
    return parser.parse_args()


def main():
    """Main function to run the scrapers"""
    try:
        args = parse_arguments()

        # Log startup information
        logger.info("Starting Web Scraper")
        logger.info(f"URL: {args.url}")
        logger.info(f"Output directory: {args.output}")
        logger.info(f"Request delay: {args.delay} seconds")

        # Create the scrapers
        w3schools_scraper = W3SchoolsScraper(args.url, delay=args.delay)

        # Create the application
        app = ScraperApplication(w3schools_scraper)

        # Run the application
        data = app.run(args.output)

        # Access and print metadata
        logger.info("\nMetadata from the course:")
        for key, value in data["metadata"].items():
            logger.info(f"  {key}: {value}")

        logger.info("\nScraping and export completed!")
        return 0
    except Exception as e:
        logger.error(f"Error in main: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())