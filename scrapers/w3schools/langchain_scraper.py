"""
W3Schools Node.js Scraper using LangChain.
Scrapes Node.js tutorials from W3Schools website.
"""

import os
import sys
import json
import time
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from loguru import logger

# LangChain imports
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Add parent directory to path to import BaseScraper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base import BaseScraper


class W3SchoolsNodeJsLangChainScraper(BaseScraper):
    """
    Scraper for W3Schools Node.js tutorials using LangChain.
    """
    
    def __init__(self, output_dir: str = "data/raw", metadata: Dict[str, Any] = None, limit: int = None):
        """
        Initialize the W3Schools Node.js LangChain scraper.
        
        Args:
            output_dir: Directory to save scraped data
            metadata: Additional metadata to include with scraped content
            limit: Maximum number of tutorials to scrape (None for all)
        """
        super().__init__(
            name="w3schools_nodejs_langchain",
            base_url="https://www.w3schools.com/nodejs/",
            output_dir=output_dir,
            metadata=metadata or {"subject": "Node.js", "platform": "W3Schools"}
        )
        self.limit = limit
        
    def get_tutorial_links(self) -> List[Dict[str, str]]:
        """
        Extract all Node.js tutorial links from the W3Schools sidebar.
        
        Returns:
            List of dictionaries with tutorial titles and URLs
        """
        try:
            start_url = self.base_url + "default.asp"
            logger.info(f"Fetching main page: {start_url}")
            
            response = requests.get(start_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            tutorial_links = []
            sidebar = soup.select_one('#sidenav')
            if sidebar:
                links = sidebar.find_all('a')
                for link in links:
                    href = link.get('href')
                    if href and '.asp' in href:
                        full_url = href if href.startswith('http') else f"{self.base_url}{href}"
                        tutorial_links.append({
                            "title": link.text.strip(),
                            "url": full_url
                        })
            else:
                logger.warning("Sidebar not found on W3Schools Node.js page")
            
            logger.info(f"Found {len(tutorial_links)} tutorial links")
            return tutorial_links
            
        except Exception as e:
            logger.error(f"Error getting tutorial links: {str(e)}")
            return []
    
    def scrape_tutorial_page(self, link: Dict[str, str]) -> Dict[str, Any]:
        """
        Scrape a single tutorial page using LangChain and BeautifulSoup.
        
        Args:
            link: Dictionary with tutorial title and URL
            
        Returns:
            Dictionary with the scraped content
        """
        try:
            logger.info(f"Processing: {link['title']} - {link['url']}")
            
            # Use LangChain's WebBaseLoader to load the page
            loader = WebBaseLoader(link['url'])
            docs = loader.load()
            
            if not docs:
                logger.warning(f"No content loaded for {link['url']}")
                return self.enrich_item({
                    "title": link['title'],
                    "url": link['url'],
                    "content": "",
                    "code_examples": [],
                    "notes": [],
                    "next_link": None,
                    "topic": "Node.js",
                    "subtopic": self._extract_subtopic(link['title'], link['url'])
                })
            
            # Get metadata from LangChain
            metadata = docs[0].metadata
            
            # Use BeautifulSoup for targeted extraction of specific elements
            response = requests.get(link['url'])
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract title
            title_element = soup.select_one('h1.learnpage-h1') or soup.select_one('h1')
            title = title_element.text.strip() if title_element else link['title']
            
            # Extract code examples
            code_examples = []
            code_blocks = soup.select('.w3-example .w3-code')
            for code_block in code_blocks:
                language = "javascript"  # Default for Node.js
                if "pythonHigh" in code_block.get('class', []):
                    language = "python"
                elif "sqlHigh" in code_block.get('class', []):
                    language = "sql"
                    
                code_examples.append({
                    "language": language,
                    "code": code_block.text.strip()
                })
            
            # Find next tutorial link
            next_link_element = soup.select_one('.w3-right.w3-btn')
            next_link = None
            if next_link_element and next_link_element.get('href'):
                href = next_link_element.get('href')
                next_link = href if href.startswith('http') else f"{self.base_url}{href}"
            
            # Extract any notes
            notes = []
            for note in soup.select('.w3-panel.w3-note'):
                notes.append(note.text.strip())
            
            # Process content with LangChain
            # Use the text_splitter to break content into manageable chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=100
            )
            
            # Split the document
            splits = text_splitter.split_documents(docs)
            
            # Extract the main content
            content = "\n\n".join([split.page_content for split in splits])
            
            # Extract subtopic
            subtopic = self._extract_subtopic(title, link['url'])
            
            # Store all extracted data
            tutorial_data = {
                "title": title,
                "url": link['url'],
                "content": content,
                "code_examples": code_examples,
                "notes": notes,
                "next_link": next_link,
                "topic": "Node.js",
                "subtopic": subtopic,
                "langchain_metadata": {
                    "title": metadata.get('title', ''),
                    "description": metadata.get('description', ''),
                    "language": metadata.get('language', '')
                }
            }
            
            return self.enrich_item(tutorial_data)
            
        except Exception as e:
            logger.error(f"Error scraping tutorial page {link['url']}: {str(e)}")
            return self.enrich_item({
                "title": link['title'],
                "url": link['url'],
                "content": f"Error scraping page: {str(e)}",
                "code_examples": [],
                "notes": [],
                "next_link": None,
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
        import re
        
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
        Scrape Node.js tutorials from W3Schools using LangChain.
        
        Returns:
            List of dictionaries containing scraped tutorials
        """
        # Get all tutorial links
        tutorial_links = self.get_tutorial_links()
        
        # Apply limit if set
        if self.limit is not None:
            tutorial_links = tutorial_links[:self.limit]
            logger.info(f"Limiting to {self.limit} tutorials")
        
        # Scrape each tutorial
        tutorials = []
        for i, link in enumerate(tutorial_links):
            logger.info(f"Processing tutorial {i+1}/{len(tutorial_links)}")
            tutorial_data = self.scrape_tutorial_page(link)
            tutorials.append(tutorial_data)
            
            # Be nice to the server
            time.sleep(1)
        
        logger.success(f"Scraping completed. Scraped {len(tutorials)} tutorials")
        return tutorials


if __name__ == "__main__":
    # Example usage
    scraper = W3SchoolsNodeJsLangChainScraper(limit=5)  # Limit to 5 tutorials for testing
    results = scraper.scrape()
    output_path = scraper.save_results(results)
    print(f"Scraped {len(results)} tutorials and saved to {output_path}")