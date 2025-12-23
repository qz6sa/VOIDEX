# 🐉 VOIDEX Installation Guide for Kali Linux

**Developer:** Sanad.CodeX  
**Version:** 1.0.0

---

## 📋 Prerequisites

Kali Linux comes with Python pre-installed, but make sure you have:
- Python 3.8 or newer
- pip (Python package manager)
- git (optional for downloading)
- Internet connection

---

## 🚀 Quick Installation Method

### Step 1️⃣: Update System

```bash
# Update package list
sudo apt update

# Update system (optional)
sudo apt upgrade -y
```

### Step 2️⃣: Verify Python and pip

```bash
# Check Python version
python3 --version

# Check pip
pip3 --version

# If pip is not installed
sudo apt install python3-pip -y
```

### Step 3️⃣: Download VOIDEX

#### Method 1: Using USB or Direct Download

```bash
# Navigate to where you want to save VOIDEX
cd ~/Desktop

# If you have a ZIP file
unzip VOIDEX.zip
cd VOIDEX

# Or if you copied the folder directly
cd VOIDEX
```

#### Method 2: Using Git (if on GitHub)

```bash
# Navigate to desired folder
cd ~/Desktop

# Clone the repository
git clone <repository-url>
cd VOIDEX
```

### Step 4️⃣: Install Requirements

#### ⚠️ If you encounter "externally-managed-environment" error

This is a common error in modern Kali Linux. Use one of the following solutions:

#### ✅ Solution 1: Use Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Now use the tool
python main.py --help

# To exit virtual environment later
deactivate
```

#### ✅ Solution 2: Install for Current User Only

```bash
# Install for current user only (without sudo)
pip3 install -r requirements.txt --user

# Then use
python3 main.py --help
```

#### ⚠️ Solution 3: Override Protection (Not Recommended)

```bash
# Use only if previous solutions fail
pip3 install -r requirements.txt --break-system-packages

# Or
sudo pip3 install -r requirements.txt --break-system-packages
```

### Step 5️⃣: Grant Execute Permissions

```bash
# Grant permissions to main files
chmod +x main.py
chmod +x setup.py
```

### Step 6️⃣: Verify Installation

```bash
# Display help menu
python3 main.py --help
```

---

## 🎯 Using VOIDEX on Kali Linux

### Basic Commands

```bash
# SQL Injection scan
python3 main.py sqli --url "http://target.com/page?id=1"

# XSS scan
python3 main.py xss --url "http://target.com/search"

# Subdomain discovery
python3 main.py subdomain --domain target.com

# Directory bruteforce
python3 main.py dirbrute --url "http://target.com"

# Login bruteforce
python3 main.py login --url "http://target.com/login"
```

---

## 🔧 Advanced Setup (Optional)

### 1. Create Alias for Easy Use

```bash
# Open bashrc file
nano ~/.bashrc

# Add this line at the end of file
alias voidex='python3 ~/Desktop/VOIDEX/main.py'

# Save file (Ctrl+O then Enter then Ctrl+X)

# Reload settings
source ~/.bashrc

# Now you can use the tool by typing
voidex --help
voidex sqli --url "http://target.com/page?id=1"
```

### 2. Create Symbolic Link

```bash
# Create link in /usr/local/bin
sudo ln -s ~/Desktop/VOIDEX/main.py /usr/local/bin/voidex

# Grant execute permissions
sudo chmod +x /usr/local/bin/voidex

# Now you can use the tool from anywhere
voidex --help
```

### 3. Create Virtual Environment

```bash
# Navigate to VOIDEX folder
cd ~/Desktop/VOIDEX

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Now use the tool
python main.py --help

# To exit virtual environment
deactivate
```

---

## 📝 Practical Examples on Kali Linux

### Example 1: Comprehensive Site Scan

```bash
#!/bin/bash
# Script file for comprehensive scan

TARGET="http://testsite.com"

echo "Starting VOIDEX Scan..."

# SQL Injection scan
python3 main.py sqli --url "$TARGET/page?id=1" -o sqli_results.json

# XSS scan
python3 main.py xss --url "$TARGET/search" -o xss_results.json

# Subdomain scan
python3 main.py subdomain --domain testsite.com -o subdomains.txt

echo "Scan completed!"
```

### Example 2: Using with Proxychains

```bash
# Run VOIDEX through Tor
proxychains python3 main.py sqli --url "http://target.com/page?id=1"
```

### Example 3: Organized Results Storage

```bash
# Create results folder
mkdir -p ~/VOIDEX_Results/$(date +%Y%m%d)

# Run scan with saved results
python3 main.py sqli --url "http://target.com/page?id=1" \
  -o ~/VOIDEX_Results/$(date +%Y%m%d)/sqli_scan.json
```

---

## 🛠️ Common Problems & Solutions

### Problem 1: externally-managed-environment ⚠️ (Most Common)

**Error:**
```
error: externally-managed-environment
× This environment is externally managed
```

**Recommended Solution - Use Virtual Environment:**

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Now you can use VOIDEX normally
python main.py --help

# 5. When finished, you can deactivate
deactivate
```

**📝 Note:** Every time you want to use VOIDEX, activate the virtual environment first:
```bash
cd ~/Desktop/VOIDEX
source venv/bin/activate
python main.py --help
```

**Alternative Solutions:**

```bash
# Solution 2: Install for user only
pip3 install -r requirements.txt --user

# Solution 3: Override protection (not recommended)
pip3 install -r requirements.txt --break-system-packages
```

### Problem 2: Permission Error

```bash
# Solution: Install for current user only
pip3 install --user -r requirements.txt

# Or use virtual environment (recommended)
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

### Problem 3: SSL Error

```bash
# In config.yaml file, make sure:
verify_ssl: false

# Or use:
python3 main.py sqli --url "http://target.com" --no-verify-ssl
```

### Problem 4: Python command not found

```bash
# Use python3 instead of python
python3 main.py --help

# Or create alias
alias python=python3
```

### Problem 5: Module not found

```bash
# Reinstall requirements
pip3 install -r requirements.txt --upgrade --force-reinstall

# Or install each library manually
pip3 install requests aiohttp beautifulsoup4 dnspython colorama tqdm PyYAML
```

### Problem 6: Memory Error

```bash
# Reduce number of threads in config.yaml
max_threads: 5
max_concurrent: 25
```

---

## 🎯 Tips for Using on Kali Linux

### 1. Using with Other Kali Tools

```bash
# Combine with nmap
nmap -p- target.com > ports.txt
python3 main.py dirbrute --url "http://target.com:8080"

# Combine with whatweb
whatweb target.com
python3 main.py xss --url "http://target.com"
```

### 2. Running in Background

```bash
# Run in background with nohup
nohup python3 main.py subdomain --domain target.com > scan.log 2>&1 &

# Check running processes
ps aux | grep main.py

# Stop process
kill <PID>
```

### 3. Schedule Scans

```bash
# Use cron to schedule regular scans
crontab -e

# Add this line for daily scan at 2 AM
0 2 * * * cd ~/Desktop/VOIDEX && python3 main.py subdomain --domain target.com -o /tmp/daily_scan.txt
```

### 4. Using with tmux

```bash
# Start tmux session
tmux new -s voidex_scan

# Run scan
python3 main.py dirbrute --url "http://target.com"

# Detach from session (Ctrl+B then D)

# Return to session
tmux attach -t voidex_scan
```

---

## 📊 Performance Monitoring

### Resource Usage

```bash
# Monitor CPU and memory usage
htop

# Monitor network usage
iftop

# Monitor VOIDEX process specifically
watch -n 1 'ps aux | grep main.py'
```

---

## 🔒 Safe Usage on Kali

### 1. Use VPN

```bash
# Enable VPN before scanning
sudo openvpn config.ovpn

# Then use VOIDEX
python3 main.py sqli --url "http://target.com"
```

### 2. Change MAC Address

```bash
# Change MAC address before scanning
sudo macchanger -r eth0

# Verify change
macchanger -s eth0
```

### 3. Use Tor

```bash
# Start Tor service
sudo service tor start

# Use VOIDEX with proxychains
proxychains python3 main.py sqli --url "http://target.com"
```
### ⚡ الطريقة السريعة مع Virtual Environment (موصى بها)

```bash
# نسخ ولصق هذه الأوامر للبدء السريع
cd ~/Desktop
# [انسخ مجلد VOIDEX هنا]
cd VOIDEX

# إنشاء وتفعيل البيئة الافتراضية
python3 -m venv venv
source venv/bin/activate

# تثبيت المتطلبات
pip install -r requirements.txt

# منح صلاحيات التنفيذ
chmod +x main.py

# تجربة الأداة
python main.py --help
```

### 📝 للاستخدام اللاحق

```bash
# في كل مرة تريد استخدام VOIDEX:
cd ~/Desktop/VOIDEX
source venv/bin/activate
python main.py --help

# عند الانتهاء:
deactivate
- [ ] تم تثبيت المتطلبات (requirements.txt)
- [ ] تم اختبار الأداة بـ `--help`
- [ ] لديك إذن مكتوب لاختبار الهدف
- [ ] VPN/Proxy معدّ (إذا لزم الأمر)
- [ ] مجلدات النتائج جاهزة
- [ ] تم قراءة الإرشادات القانونية

---

## 🎓 موارد إضافية لمستخدمي Kali

### دورات وموارد تعليمية

- Kali Linux Official Documentation
- Offensive Security Training
- TryHackMe Kali Rooms
- HackTheBox with Kali

### أدوات تكميلية في Kali

```bash
# أدوات مفيدة مع VOIDEX
burpsuite      # لتحليل الطلبات
wireshark      # For network monitoring
metasploit     # For advanced exploitation
sqlmap         # For advanced SQL scanning
nikto          # For server scanning
```

---

## 🚀 Quick Start

### ⚡ Quick Method with Virtual Environment (Recommended)

```bash
# Copy and paste these commands to start quickly
cd ~/Desktop
# [Copy VOIDEX folder here]
cd VOIDEX

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Grant execute permissions
chmod +x main.py

# Test the tool
python main.py --help
```

### 📝 For Later Use

```bash
# Every time you want to use VOIDEX:
cd ~/Desktop/VOIDEX
source venv/bin/activate
python main.py --help

# When finished:
deactivate
```

---

## 📋 Quick Checklist

Before using VOIDEX on Kali:

- [ ] Python 3.8+ installed
- [ ] pip3 installed
- [ ] Requirements installed (requirements.txt)
- [ ] Tool tested with `--help`
- [ ] Have written permission to test target
- [ ] VPN/Proxy configured (if necessary)
- [ ] Results folders ready
- [ ] Read legal guidelines

---

## ⚠️ Important Legal Reminder

**Specifically for Kali Linux:**

Kali Linux is a very powerful tool that comes with professional penetration testing tools. Using VOIDEX on Kali requires:

- ⚖️ **Written permission** for testing
- 📜 **Compliance with laws** local and international
- 🎓 **Educational purposes** only
- 🛡️ **Isolated environments** or authorized ones
- ❌ **Do not test** unauthorized targets

**Illegal hacking is a serious crime!**

---

## 📞 Support and Help

If you encounter problems:

1. Check `README.md` file
2. Review `INSTALL.md`
3. Read `SECURITY_ETHICS.md`
4. Check logs in `logs/` folder

---

## ✅ Conclusion

You are now ready to use VOIDEX on Kali Linux! 🎉

**Remember:**
- Use responsibly
- Always get permission
- Learn and develop your skills
- Help secure the internet

---

**Developer:** Sanad.CodeX  
**Project:** VOIDEX - Web Penetration Testing Toolkit  
**Version:** 1.0.0  
**Purpose:** Educational and Authorized Testing Only

© 2025 Sanad.CodeX - All Rights Reserved

---

**🐉 Good Luck on Your Security Journey with Kali Linux! 🛡️**

**🐉 حظاً موفقاً في رحلتك الأمنية على Kali Linux! 🛡️**
