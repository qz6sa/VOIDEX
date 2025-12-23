# VOIDEX - Installation & Setup Guide

**Developer:** Sanad.CodeX  
**Version:** 1.0.0

---

## 📦 Quick Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Internet connection (for dependencies)

### Step 1: Download VOIDEX
```bash
# If you have git installed
git clone <repository-url>
cd VOIDEX

# Or download and extract the ZIP file
# Then navigate to the VOIDEX folder
```

### Step 2: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
# Check if VOIDEX is working
python main.py --help
```

---

## 🚀 Quick Start

### Run Your First Scan
```bash
# SQL Injection test (on authorized target)
python main.py sqli --url "http://example.com/page?id=1"

# Display help
python main.py --help
```

---

## 🔧 Detailed Setup

### For Windows Users

**1. Install Python**
- Download Python from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"
- Verify: Open CMD and type `python --version`

**2. Install Dependencies**
```cmd
cd path\to\VOIDEX
pip install -r requirements.txt
```

**3. Run VOIDEX**
```cmd
python main.py --help
```

### For Linux Users

**1. Install Python**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip

# Arch
sudo pacman -S python python-pip
```

**2. Install Dependencies**
```bash
cd /path/to/VOIDEX
pip3 install -r requirements.txt
```

**3. Run VOIDEX**
```bash
python3 main.py --help
```

### For macOS Users

**1. Install Python**
```bash
# Using Homebrew
brew install python3
```

**2. Install Dependencies**
```bash
cd /path/to/VOIDEX
pip3 install -r requirements.txt
```

**3. Run VOIDEX**
```bash
python3 main.py --help
```

---

## 📋 Required Dependencies

The following packages will be installed automatically:

```
requests>=2.31.0       # HTTP requests
aiohttp>=3.9.1         # Async HTTP
beautifulsoup4>=4.12.2 # HTML parsing
dnspython>=2.4.2       # DNS operations
colorama>=0.4.6        # Colored output
tqdm>=4.66.1           # Progress bars
PyYAML>=6.0.1          # YAML config
```

---

## ⚙️ Configuration

### Default Configuration
VOIDEX comes with a default configuration in `config.yaml`

### Customize Settings
Edit `config.yaml` to change:
- Request timeout
- Number of threads
- User agents
- Tool-specific settings

Example:
```yaml
# HTTP Request Settings
timeout: 10
verify_ssl: false
max_threads: 10
```

---

## 🧪 Test Your Setup

### 1. Check Python Version
```bash
python --version
# Should show Python 3.8 or higher
```

### 2. Check Installed Packages
```bash
pip list
# Should show all required packages
```

### 3. Run Quick Test
```bash
python main.py --help
# Should display VOIDEX help menu
```

### 4. Test a Tool
```bash
# Test subdomain finder (safe test)
python main.py subdomain --domain example.com --wordlist wordlists/subdomains.txt
```

---

## 🐛 Troubleshooting

### Issue: "Python not found"
**Solution:** Ensure Python is installed and added to PATH

### Issue: "Module not found"
**Solution:** 
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "Permission denied"
**Solution:** 
```bash
# Windows: Run CMD as Administrator
# Linux/Mac: Use sudo
sudo pip install -r requirements.txt
```

### Issue: SSL Certificate Errors
**Solution:** In config.yaml, set:
```yaml
verify_ssl: false
```

### Issue: "Command not found: python"
**Solution:** Try using `python3` instead of `python`

---

## 📚 Next Steps

After successful installation:

1. **Read the Documentation**
   - README.md - Full documentation
   - TESTING_GUIDE.md - Testing instructions

2. **Understand the Legal Aspects**
   - LICENSE - Legal terms
   - Always get permission before testing

3. **Try the Tools**
   - Start with safe testing environments
   - Practice on your own systems first

4. **Customize VOIDEX**
   - Edit config.yaml for your needs
   - Add custom wordlists
   - Modify tool parameters

---

## 🎯 Usage Examples

### SQL Injection Scanner
```bash
python main.py sqli --url "http://target.com/page?id=1" -o results.json
```

### XSS Scanner
```bash
python main.py xss --url "http://target.com/search"
```

### Subdomain Finder
```bash
python main.py subdomain --domain target.com -o subdomains.txt
```

### Directory Bruteforce
```bash
python main.py dirbrute --url "http://target.com" --wordlist wordlists/directories.txt
```

### Login Bruteforce
```bash
python main.py login --url "http://target.com/login" --usernames wordlists/usernames.txt --passwords wordlists/passwords.txt
```

---

## 🔐 Security Reminders

⚠️ **Before Using VOIDEX:**

1. ✅ Ensure you have written permission to test
2. ✅ Understand local cybersecurity laws
3. ✅ Use only in authorized environments
4. ✅ Never test on systems you don't own
5. ✅ Follow responsible disclosure practices

---

## 💡 Tips for Best Results

1. **Start Small**
   - Test on local environments first
   - Use small wordlists initially
   - Understand each tool before full scans

2. **Optimize Performance**
   - Adjust thread counts in config
   - Use appropriate delays
   - Monitor system resources

3. **Document Everything**
   - Save all scan results
   - Keep notes of findings
   - Maintain testing logs

4. **Stay Legal**
   - Always get authorization
   - Follow testing scope
   - Report responsibly

---

## 📞 Getting Help

### If You Need Assistance:

1. **Check Documentation**
   - README.md
   - TESTING_GUIDE.md
   - This file

2. **Common Issues**
   - Review troubleshooting section
   - Check Python version
   - Verify dependencies

3. **Educational Resources**
   - OWASP resources
   - Security training platforms
   - Online tutorials

---

## 🎓 Learning Path

**Beginner:**
1. Install VOIDEX
2. Read all documentation
3. Set up local testing environment
4. Try basic scans
5. Understand results

**Intermediate:**
1. Customize configuration
2. Create custom wordlists
3. Test various scenarios
4. Analyze detailed results
5. Practice responsible disclosure

**Advanced:**
1. Modify tool code
2. Add custom features
3. Integrate with other tools
4. Conduct comprehensive assessments
5. Contribute to security community

---

## ✅ Installation Checklist

- [ ] Python 3.8+ installed
- [ ] pip installed
- [ ] Downloaded VOIDEX
- [ ] Installed dependencies
- [ ] Tested with --help
- [ ] Read README.md
- [ ] Read LICENSE
- [ ] Understood legal requirements
- [ ] Ready to use responsibly

---

## 🌟 You're Ready!

Congratulations! VOIDEX is now installed and ready to use.

**Remember:**
- Use responsibly
- Stay legal
- Learn continuously
- Share knowledge ethically

---

**Developer:** Sanad.CodeX  
**Project:** VOIDEX - Web Penetration Testing Toolkit  
**Version:** 1.0.0  
**Purpose:** Educational & Authorized Testing Only

© 2025 Sanad.CodeX - All Rights Reserved

---

**Happy Ethical Hacking! 🛡️**
