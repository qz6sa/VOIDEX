"""
Input Validator for VOIDEX
Developer: Sanad.CodeX
"""

import re
from urllib.parse import urlparse


class Validator:
    """Validates user inputs and URLs."""
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Validate if string is a valid URL."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def is_valid_domain(domain: str) -> bool:
        """Validate if string is a valid domain."""
        pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        return bool(re.match(pattern, domain))
    
    @staticmethod
    def normalize_url(url: str) -> str:
        """Normalize URL by adding scheme if missing."""
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        return url.rstrip('/')
    
    @staticmethod
    def is_valid_file(filepath: str) -> bool:
        """Check if file exists and is readable."""
        import os
        return os.path.isfile(filepath)
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe file operations."""
        return re.sub(r'[^\w\-_\. ]', '_', filename)
