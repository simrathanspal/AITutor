import logging
from abc import ABC, abstractmethod
from typing import Any, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WebScraper(ABC):
    """Abstract base class for web scrapers"""

    def __init__(self, base_url: str, user_agent: Optional[str] = None):
        self.base_url = base_url
        self.user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        self.session = self._create_session()
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def _create_session(self) -> requests.Session:
        """Create a requests session with headers and retry logic"""
        session = requests.Session()
        session.headers.update({"User-Agent": self.user_agent})

        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        return session

    def get_page_content(self, url: str) -> Optional[str]:
        """Get HTML content from a URL"""
        try:
            self.logger.info(f"Fetching {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None

    @abstractmethod
    def extract_data(self, html_content: str, url: str) -> Any:
        """Extract data from HTML content"""
        pass