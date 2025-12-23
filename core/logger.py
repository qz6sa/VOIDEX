"""
Logger Module with Colorama for VOIDEX
Developer: Sanad.CodeX
"""

from colorama import Fore, Style, init
from datetime import datetime
import os

# Initialize colorama
init(autoreset=True)


class Logger:
    """Colored logger for VOIDEX toolkit."""
    
    def __init__(self, name: str = "VOIDEX", log_file: str = None):
        self.name = name
        self.log_file = log_file
        self.verbose = True
    
    def _write_to_file(self, message: str):
        """Write log message to file."""
        if self.log_file:
            try:
                with open(self.log_file, 'a', encoding='utf-8') as f:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"[{timestamp}] {message}\n")
            except Exception:
                pass
    
    def info(self, message: str):
        """Log info message."""
        formatted = f"{Fore.CYAN}[*]{Style.RESET_ALL} {message}"
        print(formatted)
        self._write_to_file(f"[INFO] {message}")
    
    def success(self, message: str):
        """Log success message."""
        formatted = f"{Fore.GREEN}[+]{Style.RESET_ALL} {message}"
        print(formatted)
        self._write_to_file(f"[SUCCESS] {message}")
    
    def warning(self, message: str):
        """Log warning message."""
        formatted = f"{Fore.YELLOW}[!]{Style.RESET_ALL} {message}"
        print(formatted)
        self._write_to_file(f"[WARNING] {message}")
    
    def error(self, message: str):
        """Log error message."""
        formatted = f"{Fore.RED}[-]{Style.RESET_ALL} {message}"
        print(formatted)
        self._write_to_file(f"[ERROR] {message}")
    
    def debug(self, message: str):
        """Log debug message."""
        if self.verbose:
            formatted = f"{Fore.MAGENTA}[DEBUG]{Style.RESET_ALL} {message}"
            print(formatted)
            self._write_to_file(f"[DEBUG] {message}")
    
    def vuln(self, message: str):
        """Log vulnerability found."""
        formatted = f"{Fore.RED}{Style.BRIGHT}[VULN]{Style.RESET_ALL} {message}"
        print(formatted)
        self._write_to_file(f"[VULNERABILITY] {message}")
    
    def banner(self):
        """Display VOIDEX banner."""
        banner = f"""
{Fore.CYAN}{Style.BRIGHT}
╦  ╦╔═╗╦╔╦╗╔═╗═╗ ╦
╚╗╔╝║ ║║ ║║║╣ ╔╩╦╝
 ╚╝ ╚═╝╩═╩╝╚═╝╩ ╚═
{Style.RESET_ALL}
{Fore.WHITE}Web Penetration Testing Toolkit{Style.RESET_ALL}
{Fore.GREEN}Developer: Sanad.CodeX{Style.RESET_ALL}
{Fore.YELLOW}Version 1.0.0 | Educational Purpose Only{Style.RESET_ALL}
{Fore.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}
"""
        print(banner)
    
    def section(self, title: str):
        """Print section header."""
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{title.center(60)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{Style.BRIGHT}{'='*60}{Style.RESET_ALL}\n")
