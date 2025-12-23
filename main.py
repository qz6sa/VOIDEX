"""
VOIDEX - Web Penetration Testing Toolkit
Main CLI Interface

Developer: Sanad.CodeX
EDUCATIONAL PURPOSE ONLY
"""

import argparse
import sys
import os
from colorama import init

# Initialize colorama
init(autoreset=True)

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from core import Logger, Config


def print_disclaimer():
    """Print legal disclaimer."""
    disclaimer = """
    ╔════════════════════════════════════════════════════════════════╗
    ║                  VOIDEX - Penetration Testing Tool             ║
    ║                    Developer: Sanad.CodeX                      ║
    ╠════════════════════════════════════════════════════════════════╣
    ║                     LEGAL DISCLAIMER                           ║
    ╠════════════════════════════════════════════════════════════════╣
    ║                                                                ║
    ║  This tool is provided for EDUCATIONAL PURPOSES ONLY.          ║
    ║                                                                ║
    ║  Usage of VOIDEX for attacking targets without prior mutual   ║
    ║  consent is ILLEGAL. It is the end user's responsibility to   ║
    ║  obey all applicable local, state, and federal laws.           ║
    ║                                                                ║
    ║  Developers assume NO LIABILITY and are NOT responsible for    ║
    ║  any misuse or damage caused by this program.                  ║
    ║                                                                ║
    ║  By using this tool, you agree to use it only on systems you   ║
    ║  own or have explicit permission to test.                      ║
    ║                                                                ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    print(disclaimer)


def create_parser():
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description='VOIDEX - Web Penetration Testing Toolkit\nDeveloper: Sanad.CodeX',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s sqli --url http://example.com/page?id=1
  %(prog)s xss --url http://example.com/login --forms
  %(prog)s subdomain --domain example.com --verify
  %(prog)s dirbrute --url http://example.com --extensions .php,.html
  %(prog)s login --url http://example.com/login --username admin --passwords passwords.txt
        """
    )
    
    parser.add_argument('-c', '--config', type=str, default='config.yaml',
                       help='Path to configuration file')
    parser.add_argument('-o', '--output', type=str,
                       help='Output file for results')
    parser.add_argument('--no-banner', action='store_true',
                       help='Suppress banner display')
    
    subparsers = parser.add_subparsers(dest='tool', help='Tool to use')
    
    # SQL Injection Scanner
    sqli_parser = subparsers.add_parser('sqli', help='SQL Injection Scanner')
    sqli_parser.add_argument('--url', required=True, help='Target URL with parameters')
    
    # XSS Scanner
    xss_parser = subparsers.add_parser('xss', help='XSS Scanner')
    xss_parser.add_argument('--url', required=True, help='Target URL')
    xss_parser.add_argument('--forms', action='store_true', help='Test forms')
    xss_parser.add_argument('--no-forms', dest='forms', action='store_false',
                           help='Do not test forms')
    xss_parser.set_defaults(forms=True)
    
    # Subdomain Finder
    subdomain_parser = subparsers.add_parser('subdomain', help='Subdomain Finder')
    subdomain_parser.add_argument('--domain', required=True, help='Target domain')
    subdomain_parser.add_argument('--wordlist', type=str,
                                  help='Custom subdomain wordlist')
    subdomain_parser.add_argument('--verify', action='store_true',
                                  help='Verify subdomains with HTTP')
    subdomain_parser.add_argument('--no-verify', dest='verify', action='store_false',
                                  help='Skip HTTP verification')
    subdomain_parser.set_defaults(verify=True)
    
    # Directory Bruteforce
    dirbrute_parser = subparsers.add_parser('dirbrute', help='Directory Bruteforce')
    dirbrute_parser.add_argument('--url', required=True, help='Target URL')
    dirbrute_parser.add_argument('--wordlist', type=str,
                                help='Custom directory wordlist')
    dirbrute_parser.add_argument('--extensions', type=str,
                                help='File extensions to test (comma-separated)')
    
    # Login Bruteforce
    login_parser = subparsers.add_parser('login', help='Login Bruteforce')
    login_parser.add_argument('--url', required=True, help='Target login URL')
    login_parser.add_argument('--username', type=str,
                             help='Single username to test')
    login_parser.add_argument('--password', type=str,
                             help='Single password to test')
    login_parser.add_argument('--usernames', type=str,
                             help='Username wordlist file')
    login_parser.add_argument('--passwords', type=str,
                             help='Password wordlist file')
    login_parser.add_argument('--delay', type=float,
                             help='Delay between attempts (seconds)')
    
    return parser


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Show disclaimer
    if not args.no_banner:
        print_disclaimer()
        logger = Logger()
        logger.banner()
    
    # Check if tool is specified
    if not args.tool:
        parser.print_help()
        sys.exit(1)
    
    # Load configuration
    config = args.config if hasattr(args, 'config') else 'config.yaml'
    
    try:
        # Import and run the selected tool
        if args.tool == 'sqli':
            from tools.sql_injection import run
            run(args, config)
        
        elif args.tool == 'xss':
            from tools.xss_scanner import run
            run(args, config)
        
        elif args.tool == 'subdomain':
            from tools.subdomain_finder import run
            run(args, config)
        
        elif args.tool == 'dirbrute':
            from tools.dir_bruteforce import run
            run(args, config)
        
        elif args.tool == 'login':
            from tools.login_bruteforce import run
            run(args, config)
        
        else:
            print(f"Unknown tool: {args.tool}")
            parser.print_help()
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
        sys.exit(0)
    
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
