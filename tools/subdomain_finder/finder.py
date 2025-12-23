"""
Subdomain Finder Tool
Developer: Sanad.CodeX
VOIDEX - Web Penetration Testing Toolkit
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core import HTTPClient, Logger, Validator
import dns.resolver
import asyncio
import aiohttp
from typing import List, Set
from tqdm import tqdm
import time


class SubdomainFinder:
    """Subdomain enumeration tool using DNS and HTTP probing."""
    
    def __init__(self, logger: Logger, http_client: HTTPClient):
        self.logger = logger
        self.http_client = http_client
        self.found_subdomains = set()
        self.resolver = dns.resolver.Resolver()
        self.resolver.timeout = 2
        self.resolver.lifetime = 2
    
    def _load_wordlist(self, wordlist_path: str = None) -> List[str]:
        """Load subdomain wordlist."""
        if wordlist_path and os.path.exists(wordlist_path):
            with open(wordlist_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        
        # Default wordlist
        default_wordlist = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'wordlists',
            'subdomains.txt'
        )
        
        if os.path.exists(default_wordlist):
            with open(default_wordlist, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        
        # Fallback minimal wordlist
        return [
            'www', 'mail', 'ftp', 'localhost', 'webmail', 'smtp', 'pop',
            'ns1', 'ns2', 'webdisk', 'ns', 'admin', 'blog', 'dev', 'test',
            'staging', 'api', 'app', 'mobile', 'm', 'shop', 'store',
            'news', 'forum', 'help', 'support', 'portal', 'client',
            'vpn', 'remote', 'secure', 'server', 'host', 'backup'
        ]
    
    def _check_dns(self, subdomain: str, domain: str) -> bool:
        """Check if subdomain exists via DNS lookup."""
        full_domain = f"{subdomain}.{domain}"
        try:
            answers = self.resolver.resolve(full_domain, 'A')
            if answers:
                ips = [str(rdata) for rdata in answers]
                return True, ips[0] if ips else None
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, 
                dns.resolver.NoNameservers, dns.exception.Timeout):
            pass
        except Exception:
            pass
        
        return False, None
    
    async def _check_http(self, session: aiohttp.ClientSession, 
                         subdomain: str, domain: str) -> tuple:
        """Check if subdomain responds to HTTP/HTTPS."""
        full_domain = f"{subdomain}.{domain}"
        
        for protocol in ['https', 'http']:
            url = f"{protocol}://{full_domain}"
            try:
                async with session.get(
                    url,
                    timeout=aiohttp.ClientTimeout(total=5),
                    ssl=False,
                    allow_redirects=True
                ) as response:
                    if response.status < 500:
                        return True, url, response.status
            except Exception:
                continue
        
        return False, None, None
    
    async def _scan_subdomains_async(self, domain: str, wordlist: List[str], 
                                    max_concurrent: int = 50) -> Set[str]:
        """Async subdomain scanning."""
        found = set()
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def check_subdomain(subdomain: str):
            async with semaphore:
                # DNS check first (faster)
                dns_exists, ip = self._check_dns(subdomain, domain)
                if dns_exists:
                    full_domain = f"{subdomain}.{domain}"
                    found.add(full_domain)
                    return True, full_domain, ip
                return False, None, None
        
        # Create tasks for all subdomains
        tasks = [check_subdomain(sub) for sub in wordlist]
        
        # Use tqdm for progress
        with tqdm(total=len(tasks), desc="Scanning", 
                 bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
            for coro in asyncio.as_completed(tasks):
                result = await coro
                if result[0]:
                    self.logger.success(f"Found: {result[1]} ({result[2]})")
                pbar.update(1)
        
        return found
    
    def scan(self, domain: str, wordlist_path: str = None, 
             verify_http: bool = True) -> dict:
        """Scan for subdomains of a domain."""
        self.logger.section("SUBDOMAIN FINDER")
        self.logger.info(f"Target: {domain}")
        
        if not Validator.is_valid_domain(domain):
            self.logger.error("Invalid domain format")
            return {'found': [], 'count': 0}
        
        # Load wordlist
        wordlist = self._load_wordlist(wordlist_path)
        self.logger.info(f"Loaded {len(wordlist)} subdomain names")
        
        # Perform DNS-based scanning
        self.logger.info("Starting DNS enumeration...")
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            found = loop.run_until_complete(
                self._scan_subdomains_async(domain, wordlist, max_concurrent=50)
            )
            loop.close()
        except Exception as e:
            self.logger.error(f"Error during scanning: {str(e)}")
            return {'found': [], 'count': 0}
        
        # Verify with HTTP if requested
        if verify_http and found:
            self.logger.info("Verifying subdomains with HTTP probes...")
            verified = self._verify_http_sync(list(found))
            
            result = {
                'found': list(found),
                'verified': verified,
                'count': len(found),
                'domain': domain
            }
        else:
            result = {
                'found': list(found),
                'count': len(found),
                'domain': domain
            }
        
        if found:
            self.logger.success(f"Found {len(found)} subdomains")
        else:
            self.logger.info("No subdomains found")
        
        return result
    
    def _verify_http_sync(self, subdomains: List[str]) -> List[dict]:
        """Verify subdomains via HTTP (synchronous)."""
        verified = []
        
        with tqdm(total=len(subdomains), desc="HTTP Verify", 
                 bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
            for subdomain in subdomains:
                for protocol in ['https', 'http']:
                    url = f"{protocol}://{subdomain}"
                    response = self.http_client.get(url)
                    if response and response.status_code < 500:
                        verified.append({
                            'subdomain': subdomain,
                            'url': url,
                            'status': response.status_code
                        })
                        break
                pbar.update(1)
        
        return verified


def run(args, config):
    """Run subdomain finder."""
    from core import Config
    
    cfg = Config(config if config else 'config.yaml')
    logger = Logger("Subdomain Finder", args.output if hasattr(args, 'output') else None)
    http_client = HTTPClient(
        timeout=cfg.get('timeout'),
        verify_ssl=cfg.get('verify_ssl'),
        user_agents=cfg.get('user_agents')
    )
    
    finder = SubdomainFinder(logger, http_client)
    
    wordlist = getattr(args, 'wordlist', None)
    verify_http = getattr(args, 'verify', True)
    
    result = finder.scan(args.domain, wordlist, verify_http)
    
    # Save results if output file specified
    if hasattr(args, 'output') and args.output and result['found']:
        import json
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=4)
        logger.success(f"Results saved to {args.output}")
    
    http_client.close()
    return result
