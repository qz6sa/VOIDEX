# VOIDEX - Web Penetration Testing Toolkit

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-Educational-red.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

**Developer:** Sanad.CodeX

VOIDEX is a comprehensive web penetration testing toolkit designed for security professionals and ethical hackers. It includes 5 powerful tools for discovering and testing web application vulnerabilities.

---

## ⚠️ LEGAL DISCLAIMER

**THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY**

Usage of VOIDEX for attacking targets without prior mutual consent is **ILLEGAL**. It is the end user's responsibility to obey all applicable local, state, and federal laws. Developers assume **NO LIABILITY** and are **NOT responsible** for any misuse or damage caused by this program.

By using this tool, you agree to use it only on:
- Systems you own
- Systems you have explicit written permission to test
- Authorized penetration testing environments

## 🚀 Features

### 1. SQL Injection Scanner
- Automated SQL injection vulnerability detection
- Multiple injection techniques (error-based, boolean-based, time-based)
- Comprehensive payload database
- Detection of SQL error messages
- Supports GET parameter testing

### 2. XSS Scanner
- Cross-Site Scripting vulnerability detection
- Tests both reflected and stored XSS
- Form input testing
- URL parameter testing
- Advanced payload obfuscation detection
- HTML parsing with BeautifulSoup4

### 3. Subdomain Finder
- DNS-based subdomain enumeration
- Async scanning for high performance
- HTTP/HTTPS verification
- Custom wordlist support
- Comprehensive subdomain database
- IP resolution for discovered subdomains

### 4. Directory Bruteforce
- Hidden directory and file discovery
- Async HTTP requests for speed
- Custom wordlist support
- File extension testing
- HTTP status code filtering
- Response size analysis

### 5. Login Bruteforce
- Automated login form detection
- Username and password bruteforcing
- Support for both GET and POST methods
- Custom wordlist support
- Rate limiting and delay configuration
- Success pattern detection

## 📦 Installation

### Requirements
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone or download VOIDEX:
```bash
cd VOIDEX
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Verify installation:
```bash
python main.py --help
```

## 🎯 Usage

### Basic Syntax
```bash
python main.py [tool] [options]
```

### SQL Injection Scanner
```bash
# Basic scan
python main.py sqli --url "http://example.com/page?id=1"

# With output file
python main.py sqli --url "http://example.com/page?id=1" -o results.json
```

### XSS Scanner
```bash
# Scan URL and forms
python main.py xss --url "http://example.com/search" --forms

# Scan URL parameters only
python main.py xss --url "http://example.com/search?q=test" --no-forms

# Save results
python main.py xss --url "http://example.com/login" -o xss_results.json
```

### Subdomain Finder
```bash
# Basic subdomain enumeration
python main.py subdomain --domain example.com

# With HTTP verification
python main.py subdomain --domain example.com --verify

# Custom wordlist
python main.py subdomain --domain example.com --wordlist custom_subs.txt -o subdomains.json
```

### Directory Bruteforce
```bash
# Basic directory scan
python main.py dirbrute --url "http://example.com"

# With file extensions
python main.py dirbrute --url "http://example.com" --extensions .php,.html,.txt

# Custom wordlist
python main.py dirbrute --url "http://example.com" --wordlist custom_dirs.txt -o found_dirs.json
```

### Login Bruteforce
```bash
# Test single username with password list
python main.py login --url "http://example.com/login" --username admin --passwords passwords.txt

# Test username and password lists
python main.py login --url "http://example.com/login" --usernames users.txt --passwords passwords.txt

# With custom delay
python main.py login --url "http://example.com/login" --username admin --passwords passwords.txt --delay 1.0
```

## ⚙️ Configuration

Edit `config.yaml` to customize tool behavior:

```yaml
# HTTP Request Settings
timeout: 10
verify_ssl: false
retry_count: 3
delay: 0.5

# Concurrency Settings
max_threads: 10
max_concurrent: 50

# User Agents
user_agents:
  - "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  # Add more user agents...
```

## 📁 Project Structure

```
VOIDEX/
├── main.py                      # Main CLI interface
├── config.yaml                  # Configuration file
├── requirements.txt             # Python dependencies
├── README.md                    # Documentation
│
├── core/                        # Core utilities
│   ├── __init__.py
│   ├── config.py               # Configuration manager
│   ├── http_client.py          # HTTP client with async support
│   ├── logger.py               # Colored logging
│   └── validator.py            # Input validation
│
├── tools/                       # Pentesting tools
│   ├── __init__.py
│   │
│   ├── sql_injection/          # SQL Injection Scanner
│   │   ├── __init__.py
│   │   ├── scanner.py
│   │   └── payloads.txt
│   │
│   ├── xss_scanner/            # XSS Scanner
│   │   ├── __init__.py
│   │   ├── scanner.py
│   │   └── payloads.txt
│   │
│   ├── subdomain_finder/       # Subdomain Finder
│   │   ├── __init__.py
│   │   └── finder.py
│   │
│   ├── dir_bruteforce/         # Directory Bruteforce
│   │   ├── __init__.py
│   │   └── bruteforce.py
│   │
│   └── login_bruteforce/       # Login Bruteforce
│       ├── __init__.py
│       └── bruteforce.py
│
└── wordlists/                   # Wordlists
    ├── subdomains.txt
    ├── directories.txt
    ├── passwords.txt
    └── usernames.txt
```

## 🛠️ Dependencies

- **requests** - HTTP library
- **beautifulsoup4** - HTML parsing
- **colorama** - Colored terminal output
- **aiohttp** - Async HTTP client
- **dnspython** - DNS resolver
- **tqdm** - Progress bars
- **PyYAML** - YAML configuration parser

## 🎨 Features

- ✅ Modular architecture
- ✅ Async operations for performance
- ✅ Professional colored output
- ✅ Progress bars for all operations
- ✅ Detailed error handling
- ✅ JSON output support
- ✅ Configurable via YAML
- ✅ Comprehensive wordlists
- ✅ SSL verification bypass
- ✅ Custom user agents
- ✅ Rate limiting

## 📝 Output Examples

Results can be saved in JSON format:

```json
{
  "vulnerable": true,
  "vulnerabilities": [
    {
      "type": "SQL Injection",
      "payload": "' OR '1'='1",
      "parameter": "id"
    }
  ],
  "url": "http://example.com/page?id=1"
}
```

## 🤝 Contributing

This is an educational project. Use responsibly and legally.

## 📄 License

This project is provided for **educational purposes only**. Use at your own risk.

## 🔒 Security Notice

- Always obtain proper authorization before testing
- Use only in controlled environments
- Follow responsible disclosure practices
- Respect privacy and data protection laws
- Do not use for malicious purposes

## �‍💻 Developer

**Sanad.CodeX**
- Security Researcher & Developer
- Penetration Testing Specialist
- Full Stack Security Professional

For more information, see [AUTHORS.md](AUTHORS.md)

## 📧 Contact

For educational inquiries and responsible security research only.

---

**© 2025 Sanad.CodeX - All Rights Reserved**

---

**Remember: With great power comes great responsibility. Use VOIDEX ethically and legally.**
