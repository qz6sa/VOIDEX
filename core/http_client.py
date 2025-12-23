"""
HTTP Client with async support for VOIDEX
Developer: Sanad.CodeX
"""

import requests
import aiohttp
import asyncio
from typing import Dict, Optional, List
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import random


class HTTPClient:
    """HTTP client with retry logic and async support."""
    
    def __init__(self, timeout: int = 10, verify_ssl: bool = False, 
                 user_agents: List[str] = None, retry_count: int = 3):
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.user_agents = user_agents or [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        ]
        self.retry_count = retry_count
        self.session = self._create_session()
        
        # Disable SSL warnings
        if not verify_ssl:
            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    def _create_session(self) -> requests.Session:
        """Create requests session with retry logic."""
        session = requests.Session()
        retry = Retry(
            total=self.retry_count,
            backoff_factor=0.3,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    
    def _get_headers(self, headers: Optional[Dict] = None) -> Dict:
        """Get headers with random user agent."""
        default_headers = {
            'User-Agent': random.choice(self.user_agents)
        }
        if headers:
            default_headers.update(headers)
        return default_headers
    
    def get(self, url: str, headers: Optional[Dict] = None, 
            params: Optional[Dict] = None) -> Optional[requests.Response]:
        """Perform GET request."""
        try:
            response = self.session.get(
                url,
                headers=self._get_headers(headers),
                params=params,
                timeout=self.timeout,
                verify=self.verify_ssl,
                allow_redirects=True
            )
            return response
        except Exception as e:
            return None
    
    def post(self, url: str, data: Optional[Dict] = None, 
             headers: Optional[Dict] = None) -> Optional[requests.Response]:
        """Perform POST request."""
        try:
            response = self.session.post(
                url,
                headers=self._get_headers(headers),
                data=data,
                timeout=self.timeout,
                verify=self.verify_ssl,
                allow_redirects=True
            )
            return response
        except Exception:
            return None
    
    async def async_get(self, session: aiohttp.ClientSession, url: str,
                       headers: Optional[Dict] = None) -> Dict:
        """Perform async GET request."""
        try:
            async with session.get(
                url,
                headers=self._get_headers(headers),
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                ssl=self.verify_ssl
            ) as response:
                return {
                    'url': url,
                    'status': response.status,
                    'text': await response.text(),
                    'headers': dict(response.headers)
                }
        except Exception as e:
            return {
                'url': url,
                'status': 0,
                'error': str(e)
            }
    
    async def async_post(self, session: aiohttp.ClientSession, url: str,
                        data: Optional[Dict] = None,
                        headers: Optional[Dict] = None) -> Dict:
        """Perform async POST request."""
        try:
            async with session.post(
                url,
                data=data,
                headers=self._get_headers(headers),
                timeout=aiohttp.ClientTimeout(total=self.timeout),
                ssl=self.verify_ssl
            ) as response:
                return {
                    'url': url,
                    'status': response.status,
                    'text': await response.text(),
                    'headers': dict(response.headers)
                }
        except Exception as e:
            return {
                'url': url,
                'status': 0,
                'error': str(e)
            }
    
    def close(self):
        """Close the session."""
        self.session.close()
