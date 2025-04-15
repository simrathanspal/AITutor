"""
Base Scraper module for AI Tutor ingestion pipeline.
Provides an abstract base class for all scrapers.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
import os
from datetime import datetime
from loguru import logger

class BaseScraper(ABC):
    """
    Abstract base class for all scrapers in the AI Tutor ingestion pipeline.
    All specific scrapers should inherit from this class and implement the required methods.
    """
    
    def __init__(self, 
                 name: str, 
                 base_url: str, 
                 output_dir: str = "data/raw",
                 metadata: Optional[Dict[str, Any]] = None):
        """
        Initialize the base scraper.
        
        Args:
            name: Name of the scraper
            base_url: Base URL for the scraper
            output_dir: Directory to save scraped data
            metadata: Additional metadata to include with scraped content
        """
        self.name = name
        self.base_url = base_url
        self.output_dir = output_dir
        self.metadata = metadata or {}
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        logger.info(f"Initialized {self.name} scraper for {self.base_url}")
    
    @abstractmethod
    def scrape(self) -> List[Dict[str, Any]]:
        """
        Main method to scrape content. Must be implemented by subclasses.
        
        Returns:
            List of dictionaries containing scraped content with metadata
        """
        pass
    
    def save_results(self, results: List[Dict[str, Any]], format: str = "json") -> str:
        """
        Save the scraped results to disk.
        
        Args:
            results: List of dictionaries containing scraped content
            format: Format to save data in (json, csv, etc.)
            
        Returns:
            Path to the saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.name}_{timestamp}.{format}"
        filepath = os.path.join(self.output_dir, filename)
        
        if format == "json":
            import json
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
        else:
            raise NotImplementedError(f"Format {format} not implemented yet")
        
        logger.info(f"Saved {len(results)} items to {filepath}")
        return filepath
    
    def enrich_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich a scraped item with additional metadata.
        
        Args:
            item: Dictionary containing scraped content
            
        Returns:
            Enriched item with metadata
        """
        # Add common metadata
        enriched = item.copy()
        enriched.update({
            "source": self.name,
            "source_url": self.base_url,
            "scraped_at": datetime.now().isoformat(),
            **self.metadata
        })
        return enriched