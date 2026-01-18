"""
W3Schools Node.js Scraper using Scrapy.
Scrapes Node.js tutorials from W3Schools website.
"""

import scrapy
import json
import os
import re
from datetime import datetime
from loguru import logger
from typing import Dict, Any, List
from scrapy.crawler import CrawlerProcess


class W3SchoolsNodeJsSpider(scrapy.Spider):
    """
    Scrapy spider for W3Schools Node.js tutorials.
    """
    name = 'w3schools_nodejs'
    start_urls = ['https://www.w3schools.com/nodejs/default.asp']
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'DOWNLOAD_DELAY': 1,  # Be respectful with the website
    }
    
    def __init__(self, output_dir: str = "data/raw", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.results = []
    
    def parse(self, response):
        """
        Parse the W3Schools Node.js main page to find all tutorial links.
        """
        # Extract links from the sidebar
        sidebar_links = response.css('.w3-sidebar a[href^="node"]')
        
        for link in sidebar_links:
            href = link.attrib['href']
            url = response.urljoin(href)
            
            # Follow the link to the tutorial page
            yield scrapy.Request(url=url, callback=self.parse_tutorial)
    
    def parse_tutorial(self, response):
        """
        Parse a single Node.js tutorial page.
        """
        # Extract title
        title = response.css('h1::text').get().strip()
        
        # Extract main content
        main_content = response.css('#main').get()
        content_text = ' '.join(response.css('#main ::text').getall())
        
        # Extract code examples
        code_examples = []
        for code_block in response.css('div.w3-example, div.w3-code'):
            code_text = code_block.css('::text').getall()
            code_text = ' '.join(code_text).strip()
            if code_text:
                code_examples.append(code_text)
        
        # Extract subtopic
        subtopic = self._extract_subtopic(title, response.url)
        
        # Create and enrich result item
        item = {
            "title": title,
            "url": response.url,
            "content": content_text,
            "code_examples": code_examples,
            "topic": "Node.js",
            "subtopic": subtopic,
            "source": "w3schools_nodejs_scrapy",
            "source_url": "https://www.w3schools.com/nodejs/",
            "scraped_at": datetime.now().isoformat(),
            "subject": "Node.js", 
            "platform": "W3Schools"
        }
        
        self.results.append(item)
        
        logger.info(f"Scraped: {title}")
    
    def _extract_subtopic(self, title: str, url: str) -> str:
        """
        Extract the subtopic from the title or URL.
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
    
    def closed(self, reason):
        """
        Called when the spider is closed.
        """
        # Save the results to a JSON file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"w3schools_nodejs_scrapy_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        
        logger.success(f"Saved {len(self.results)} Node.js tutorials to {filepath}")


def run_spider(output_dir: str = "data/raw"):
    """
    Helper function to run the spider.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    process = CrawlerProcess()
    process.crawl(W3SchoolsNodeJsSpider, output_dir=output_dir)
    process.start()
    
    return os.path.join(output_dir, f"w3schools_nodejs_scrapy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")


# Run the spider if the script is executed directly
if __name__ == '__main__':
    output_path = run_spider()
    print(f"Spider completed. Results saved to {output_path}")