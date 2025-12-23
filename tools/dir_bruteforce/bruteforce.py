"""
Directory Bruteforce Tool
Developer: Sanad.CodeX
VOIDEX - Web Penetration Testing Toolkit
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core import HTTPClient, Logger, Validator
import asyncio
import aiohttp
from typing import List, Set
from tqdm import tqdm
from urllib.parse import urljoin


class DirectoryBruteforce:
    """Directory and file bruteforce tool."""
    
    def __init__(self, logger: Logger, http_client: HTTPClient):
        self.logger = logger
        self.http_client = http_client
        self.found_paths = []
    
    def _load_wordlist(self, wordlist_path: str = None) -> List[str]:
        """Load directory/file wordlist."""
        if wordlist_path and os.path.exists(wordlist_path):
            with open(wordlist_path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        
        # Default wordlist
        default_wordlist = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'wordlists',
            'directories.txt'
        )
        
        if os.path.exists(default_wordlist):
            with open(default_wordlist, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]
        
        # Fallback minimal wordlist
        return [
            'admin', 'login', 'administrator', 'user', 'dashboard',
            'panel', 'config', 'backup', 'test', 'dev', 'staging',
            'api', 'v1', 'v2', 'docs', 'documentation', 'help',
            'uploads', 'files', 'images', 'img', 'css', 'js',
            'assets', 'static', 'media', 'download', 'downloads',
            'backup.zip', 'backup.sql', 'config.php', 'config.json',
            '.git', '.env', '.htaccess', 'robots.txt', 'sitemap.xml',
            'phpinfo.php', 'info.php', 'test.php', 'shell.php',
            'wp-admin', 'wp-content', 'wp-includes', 'wordpress',
            'phpmyadmin', 'pma', 'mysql', 'database', 'db',
            'cgi-bin', 'scripts', 'bin', 'tmp', 'temp'
        ]
    
    async def _check_path(self, session: aiohttp.ClientSession, 
                         base_url: str, path: str) -> dict:
        """Check if a path exists."""
        url = urljoin(base_url, path)
        
        try:
            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=10),
                ssl=False,
                allow_redirects=False
            ) as response:
                return {
                    'path': path,
                    'url': url,
                    'status': response.status,
                    'size': len(await response.read()),
                    'found': True
                }
        except Exception:
            return {'path': path, 'found': False}
    
    async def _bruteforce_async(self, base_url: str, wordlist: List[str],
                               valid_statuses: List[int] = None,
                               max_concurrent: int = 50) -> List[dict]:
        """Async directory bruteforcing."""
        if valid_statuses is None:
            valid_statuses = [200, 201, 204, 301, 302, 307, 401, 403]
        
        found = []
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def check_with_semaphore(path):
            async with semaphore:
                connector = aiohttp.TCPConnector(ssl=False)
                async with aiohttp.ClientSession(connector=connector) as session:
                    result = await self._check_path(session, base_url, path)
                    if result['found'] and result['status'] in valid_statuses:
                        return result
                    return None
        
        tasks = [check_with_semaphore(path) for path in wordlist]
        
        with tqdm(total=len(tasks), desc="Bruteforcing", 
                 bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}') as pbar:
            for coro in asyncio.as_completed(tasks):
                result = await coro
                if result:
                    found.append(result)
                    status_color = self._get_status_color(result['status'])
                    self.logger.success(
                        f"[{result['status']}] {result['url']} ({result['size']} bytes)"
                    )
                pbar.update(1)
        
        return found
    
    def _get_status_color(self, status: int) -> str:
        """Get color for HTTP status code."""
        if 200 <= status < 300:
            return 'green'
        elif 300 <= status < 400:
            return 'yellow'
        elif status == 401 or status == 403:
            return 'cyan'
        else:
            return 'red'
    
    def scan(self, url: str, wordlist_path: str = None,
            extensions: List[str] = None,
            valid_statuses: List[int] = None) -> dict:
        """Bruteforce directories and files."""
        self.logger.section("DIRECTORY BRUTEFORCE")
        self.logger.info(f"Target: {url}")
        
        if not Validator.is_valid_url(url):
            self.logger.error("Invalid URL format")
            return {'found': [], 'count': 0}
        
        # Normalize URL
        url = Validator.normalize_url(url)
        if not url.endswith('/'):
            url += '/'
        
        # Load wordlist
        wordlist = self._load_wordlist(wordlist_path)
        self.logger.info(f"Loaded {len(wordlist)} paths")
        
        # Add extensions if specified
        if extensions:
            extended_wordlist = []
            for word in wordlist:
                extended_wordlist.append(word)
                for ext in extensions:
                    if not word.endswith(ext):
                        extended_wordlist.append(f"{word}{ext}")
            wordlist = extended_wordlist
            self.logger.info(f"Extended to {len(wordlist)} paths with extensions")
        
        # Perform bruteforce
        self.logger.info("Starting directory bruteforce...")
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            found = loop.run_until_complete(
                self._bruteforce_async(url, wordlist, valid_statuses, max_concurrent=50)
            )
            loop.close()
        except Exception as e:
            self.logger.error(f"Error during bruteforce: {str(e)}")
            return {'found': [], 'count': 0}
        
        # Sort by status code
        found.sort(key=lambda x: x['status'])
        
        result = {
            'found': found,
            'count': len(found),
            'url': url
        }
        
        if found:
            self.logger.success(f"Found {len(found)} paths")
        else:
            self.logger.info("No paths found")
        
        return result


def run(args, config):
    """Run directory bruteforce."""
    from core import Config
    
    cfg = Config(config if config else 'config.yaml')
    logger = Logger("Dir Bruteforce", args.output if hasattr(args, 'output') else None)
    http_client = HTTPClient(
        timeout=cfg.get('timeout'),
        verify_ssl=cfg.get('verify_ssl'),
        user_agents=cfg.get('user_agents')
    )
    
    bruteforcer = DirectoryBruteforce(logger, http_client)
    
    wordlist = getattr(args, 'wordlist', None)
    extensions = getattr(args, 'extensions', None)
    if extensions:
        extensions = extensions.split(',')
    
    result = bruteforcer.scan(args.url, wordlist, extensions)
    
    # Save results if output file specified
    if hasattr(args, 'output') and args.output and result['found']:
        import json
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=4)
        logger.success(f"Results saved to {args.output}")
    
    http_client.close()
    return result
