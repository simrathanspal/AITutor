"""
W3Schools Node.js Scraper using BeautifulSoup.
Scrapes Node.js tutorials from W3Schools website.
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Any, Optional
import re
from loguru import logger
import os
import sys

# Add parent directory to path to import BaseScraper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base import BaseScraper


class W3SchoolsNodeJsBS4Scraper(BaseScraper):
    """
    Scraper for W3Schools Node.js tutorials using BeautifulSoup.
    """
    
    def __init__(self, output_dir: str = "data/raw", metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize the W3Schools Node.js scraper.
        """
        super().__init__(
            name="w3schools_nodejs_bs4",
            base_url="https://www.w3schools.com/nodejs/",
            output_dir=output_dir,
            metadata=metadata or {"subject": "Node.js", "platform": "W3Schools"}
        )
        self.tutorial_links = []
        
    def get_tutorial_links(self) -> List[str]:
        """
        Extract all Node.js tutorial links from the W3Schools sidebar.
        
        Returns:
            List of tutorial URLs
        """
        try:
            # Get the main Node.js page
            response = requests.get(self.base_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the sidebar with tutorial links (adjust selector based on actual page structure)
            sidebar = soup.select_one('.w3-sidebar')
            if not sidebar:
                logger.warning("Sidebar not found on W3Schools Node.js page")
                return []
                
            # Extract all links from the sidebar that point to Node.js tutorials
            links = []
            for a_tag in sidebar.select('a[href^="node"]'):
                href = a_tag.get('href')
                if href:
                    # Make sure we have the full URL
                    full_url = f"{self.base_url}{href}" if not href.startswith('http') else href
                    links.append(full_url)
            
            logger.info(f"Found {len(links)} tutorial links on W3Schools Node.js page")
            return links
            
        except Exception as e:
            logger.error(f"Error getting tutorial links: {str(e)}")
            return []
    
    def scrape_tutorial_page(self, url: str) -> Dict[str, Any]:
        """
        Scrape a single tutorial page.
        
        Args:
            url: URL of the tutorial page
            
        Returns:
            Dictionary with the scraped content
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title = soup.select_one('h1')
            title_text = title.text.strip() if title else "Unknown Title"
            
            # Extract main content
            main_content = soup.select_one('#main')
            content_text = main_content.text if main_content else ""
            
            # Extract code examples
            code_examples = []
            for code_block in soup.select('div.w3-example, div.w3-code'):
                code_text = code_block.text.strip()
                if code_text:
                    code_examples.append(code_text)
            
            # Create the result item
            item = {
                "title": title_text,
                "url": url,
                "content": content_text,
                "code_examples": code_examples,
                "topic": "Node.js",
                "subtopic": self._extract_subtopic(title_text, url)
            }
            
            return self.enrich_item(item)
            
        except Exception as e:
            logger.error(f"Error scraping tutorial page {url}: {str(e)}")
            return self.enrich_item({
                "title": "Error",
                "url": url,
                "content": f"Error scraping page: {str(e)}",
                "code_examples": [],
                "topic": "Node.js",
                "subtopic": "unknown"
            })
    
    def _extract_subtopic(self, title: str, url: str) -> str:
        """
        Extract the subtopic from the title or URL.
        
        Args:
            title: Page title
            url: Page URL
            
        Returns:
            Subtopic string
        """
        # Try to extract from URL first
        url_match = re.search(r'node_([a-z0-9_]+)\.asp', url)
        if url_match:
            return url_match.group(1).replace('_', ' ')
        
        # Fall back to title
        title_words = title.lower().split()
        if 'node.js' in title.lower() and len(title_words) > 2:
            return ' '.join(title_words[2:])
        
        return "general"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Scrape all Node.js tutorials from W3Schools.
        
        Returns:
            List of dictionaries containing scraped tutorials
        """
        # Get all tutorial links if we haven't already
        if not self.tutorial_links:
            self.tutorial_links = self.get_tutorial_links()
        
        # Scrape each tutorial page
        results = []
        for url in self.tutorial_links:
            logger.info(f"Scraping {url}")
            tutorial_data = self.scrape_tutorial_page(url)
            results.append(tutorial_data)
        
        logger.success(f"Scraped {len(results)} Node.js tutorials from W3Schools")
        return results


if __name__ == "__main__":
    # Example usage
    scraper = W3SchoolsNodeJsBS4Scraper()
    results = scraper.scrape()
    output_path = scraper.save_results(results)
    print(f"Scraped {len(results)} tutorials and saved to {output_path}")