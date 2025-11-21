import time
import logging
from typing import List, Dict, Any

from bs4 import BeautifulSoup

from src.scrapers.base import WebScraper
from src.models.schema import TutorialLink, CodeExample, TutorialContent, TutorialCourse

logger = logging.getLogger(__name__)


class W3SchoolsScraper(WebScraper):
    """Scraper for W3Schools tutorials"""

    def __init__(self, start_url: str, delay: float = 1.0):
        base_url = "https://www.w3schools.com"
        super().__init__(base_url)
        self.start_url = start_url
        self.delay = delay  # Delay between requests to avoid overloading the server

    def extract_sidebar_menu(self, html_content: str) -> List[TutorialLink]:
        """Extract sidebar menu items"""
        soup = BeautifulSoup(html_content, 'html.parser')
        sidebar_items = []

        sidebar = soup.select_one('#sidenav')
        if sidebar:
            links = sidebar.find_all('a')
            for link in links:
                href = link.get('href')
                if href and '.asp' in href:
                    full_url = href if href.startswith('http') else f"{self.base_url}/nodejs/{href}"
                    sidebar_items.append(TutorialLink(
                        title=link.text.strip(),
                        url=full_url
                    ))

        return sidebar_items

    def extract_tutorial_content(self, html_content: str, url: str) -> TutorialContent:
        """Extract tutorial content"""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract title
        title_element = soup.select_one('h1.learnpage-h1')
        title = title_element.text.strip() if title_element else "No Title Found"

        # Extract main content
        main_content = soup.select_one('#main')
        content = main_content.text.strip() if main_content else "No Content Found"

        # Extract code examples
        code_examples = []
        code_blocks = soup.select('.w3-example .w3-code')
        for code_block in code_blocks:
            language = "javascript"  # Default language
            if "pythonHigh" in code_block.get('class', []):
                language = "python"
            elif "sqlHigh" in code_block.get('class', []):
                language = "sql"

            code_examples.append(CodeExample(
                language=language,
                code=code_block.text.strip()
            ))

        # Find next tutorial link
        next_link_element = soup.select_one('.w3-right.w3-btn')
        next_link = None
        if next_link_element and next_link_element.get('href'):
            href = next_link_element.get('href')
            next_link = href if href.startswith('http') else f"{self.base_url}/nodejs/{href}"

        return TutorialContent(
            title=title,
            url=url,
            content=content,
            code_examples=code_examples,
            next_link=next_link
        )

    def extract_data(self, html_content: str, url: str) -> TutorialContent:
        """Implementation of abstract method to extract data"""
        return self.extract_tutorial_content(html_content, url)

    def extract_metadata(self, html_content: str) -> Dict[str, Any]:
        """Extract metadata from the course pages"""
        soup = BeautifulSoup(html_content, 'html.parser')
        metadata = {}

        # Extract meta tags
        meta_tags = soup.find_all('meta')
        for tag in meta_tags:
            if tag.get('name') and tag.get('content'):
                metadata[tag.get('name')] = tag.get('content')

        # Extract course information
        course_info = soup.select_one('.w3-panel.w3-info')
        if course_info:
            metadata['course_info'] = course_info.text.strip()

        return metadata

    def scrape_course(self) -> TutorialCourse:
        """Scrape the entire course"""
        logger.info(f"Starting to scrape: {self.start_url}")

        # Get the main page content
        main_page_html = self.get_page_content(self.start_url)
        if not main_page_html:
            raise ValueError("Failed to fetch the starting page")

        # Extract sidebar menu
        sidebar_items = self.extract_sidebar_menu(main_page_html)
        logger.info(f"Found {len(sidebar_items)} tutorial pages in the sidebar")

        # Extract metadata
        metadata = self.extract_metadata(main_page_html)

        # Create course data structure
        course_data = TutorialCourse(
            title="W3Schools Tutorial",
            source_url=self.start_url,
            modules=sidebar_items,
            tutorials=[],
            metadata=metadata
        )

        # Extract content from each tutorial page
        for item in sidebar_items:
            logger.info(f"Scraping: {item.title} - {item.url}")

            page_html = self.get_page_content(item.url)
            if page_html:
                tutorial_data = self.extract_tutorial_content(page_html, item.url)
                course_data.tutorials.append(tutorial_data)

                # Be nice to the server
                time.sleep(self.delay)
            else:
                logger.warning(f"Skipping {item.url} due to fetch error")

        return course_data
