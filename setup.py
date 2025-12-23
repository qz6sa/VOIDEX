#!/usr/bin/env python3
"""
VOIDEX - Quick Start Script
Developer: Sanad.CodeX
"""

import subprocess
import sys
import os

def main():
    print("""
╦  ╦╔═╗╦╔╦╗╔═╗═╗ ╦
╚╗╔╝║ ║║ ║║║╣ ╔╩╦╝
 ╚╝ ╚═╝╩═╩╝╚═╝╩ ╚═
    
VOIDEX Quick Start
Developer: Sanad.CodeX
    """)
    
    print("[*] Checking Python version...")
    if sys.version_info < (3, 8):
        print("[!] Python 3.8+ is required!")
        sys.exit(1)
    print("[+] Python version OK")
    
    print("\n[*] Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("[+] Dependencies installed successfully")
    except Exception as e:
        print(f"[-] Error installing dependencies: {e}")
        sys.exit(1)
    
    print("\n[+] Setup complete! You can now use VOIDEX:")
    print("\n    python main.py --help")
    print("    python main.py sqli --url http://example.com/page?id=1")
    print("    python main.py xss --url http://example.com/search")
    print("    python main.py subdomain --domain example.com")
    print("    python main.py dirbrute --url http://example.com")
    print("    python main.py login --url http://example.com/login")
    print("\n[!] Remember: Use only on authorized targets!")

if __name__ == "__main__":
    main()
