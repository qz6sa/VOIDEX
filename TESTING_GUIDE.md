# VOIDEX Testing Guide / دليل التجربة

**Developer:** Sanad.CodeX

---

## ⚠️ Important / مهم
**Only test on websites you own or have permission to test!**
**اختبر فقط على المواقع التي تملكها أو لديك إذن باختبارها!**

## Safe Testing Environments / بيئات اختبار آمنة

### 1. Local Testing Sites
- **DVWA (Damn Vulnerable Web Application)**: http://www.dvwa.co.uk/
- **bWAPP**: http://www.itsecgames.com/
- **WebGoat**: https://owasp.org/www-project-webgoat/
- **OWASP Juice Shop**: https://owasp.org/www-project-juice-shop/

### 2. Legal Testing Platforms
- **HackTheBox**: https://www.hackthebox.com/
- **TryHackMe**: https://tryhackme.com/
- **PentesterLab**: https://pentesterlab.com/

## Quick Test Examples / أمثلة سريعة

### Test 1: SQL Injection Scanner
```bash
# Test on a vulnerable parameter
python main.py sqli --url "http://testphp.vulnweb.com/artists.php?artist=1"

# With output file
python main.py sqli --url "http://testphp.vulnweb.com/artists.php?artist=1" -o sqli_results.json
```

### Test 2: XSS Scanner
```bash
# Test forms and parameters
python main.py xss --url "http://testphp.vulnweb.com/search.php?test=query" --forms

# URL parameters only
python main.py xss --url "http://testphp.vulnweb.com/search.php?test=query" --no-forms
```

### Test 3: Subdomain Finder
```bash
# Find subdomains
python main.py subdomain --domain example.com

# With HTTP verification and save results
python main.py subdomain --domain example.com --verify -o subdomains.json
```

### Test 4: Directory Bruteforce
```bash
# Basic directory scan
python main.py dirbrute --url "http://testphp.vulnweb.com"

# With file extensions
python main.py dirbrute --url "http://testphp.vulnweb.com" --extensions .php,.html,.txt

# Custom wordlist
python main.py dirbrute --url "http://testphp.vulnweb.com" --wordlist wordlists/directories.txt
```

### Test 5: Login Bruteforce
```bash
# Test with single username
python main.py login --url "http://testsite.com/login" --username admin --passwords wordlists/passwords.txt

# Test with username and password lists
python main.py login --url "http://testsite.com/login" --usernames wordlists/usernames.txt --passwords wordlists/passwords.txt

# With custom delay (slower, safer)
python main.py login --url "http://testsite.com/login" --username admin --passwords wordlists/passwords.txt --delay 1.0
```

## Testing Your Own Local Server / اختبار سيرفر محلي

### Setup a Local Test Environment:

1. **Install XAMPP or WAMP**
2. **Create a vulnerable PHP page for testing:**

```php
<?php
// test.php - VULNERABLE CODE FOR TESTING ONLY
$id = $_GET['id'];
$conn = mysqli_connect("localhost", "root", "", "test");
$query = "SELECT * FROM users WHERE id = $id"; // Vulnerable!
$result = mysqli_query($conn, $query);
?>
```

3. **Test locally:**
```bash
python main.py sqli --url "http://localhost/test.php?id=1"
```

## Command Options / خيارات الأوامر

### Global Options:
- `-c, --config`: Path to config file (default: config.yaml)
- `-o, --output`: Save results to JSON file
- `--no-banner`: Hide the banner

### SQL Injection:
```bash
python main.py sqli --help
```

### XSS Scanner:
```bash
python main.py xss --help
```

### Subdomain Finder:
```bash
python main.py subdomain --help
```

### Directory Bruteforce:
```bash
python main.py dirbrute --help
```

### Login Bruteforce:
```bash
python main.py login --help
```

## Tips / نصائح

1. **Start with subdomain enumeration** - It's safe and doesn't modify anything
   ابدأ بالبحث عن النطاقات الفرعية - آمن ولا يعدل شيء

2. **Use custom wordlists** - The default ones are small
   استخدم قوائم كلمات مخصصة - الافتراضية صغيرة

3. **Save results** - Always use `-o results.json` to save findings
   احفظ النتائج - استخدم دائماً `-o results.json` لحفظ الاكتشافات

4. **Adjust delays** - Use `--delay` to avoid detection or rate limiting
   اضبط التأخير - استخدم `--delay` لتجنب الكشف أو الحد من المعدل

5. **Check config.yaml** - Customize timeouts, threads, user agents
   تحقق من config.yaml - خصص المهلات والخيوط ووكلاء المستخدم

## Reading Results / قراءة النتائج

Results are saved in JSON format:

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

## Troubleshooting / حل المشاكل

### Issue: Module not found
```bash
pip install -r requirements.txt
```

### Issue: SSL errors
Edit `config.yaml` and set `verify_ssl: false`

### Issue: Timeout errors
Edit `config.yaml` and increase `timeout: 20`

### Issue: Too slow
Edit `config.yaml` and increase `max_concurrent: 100`

## ⚠️ Legal Warning / تحذير قانوني

```
استخدام هذه الأداة على أهداف بدون إذن غير قانوني!
Using this tool on targets without permission is ILLEGAL!

- Test only on your own systems
- Get written permission before testing
- Follow all local and international laws
- Use responsibly and ethically

اختبر فقط على أنظمتك الخاصة
احصل على إذن كتابي قبل الاختبار
اتبع جميع القوانين المحلية والدولية
استخدم بمسؤولية وأخلاق
```

## Example Session / جلسة مثال

```bash
# Step 1: Scan for subdomains
python main.py subdomain --domain target.com -o subdomains.json

# Step 2: Directory bruteforce on found subdomain
python main.py dirbrute --url https://admin.target.com --extensions .php -o directories.json

# Step 3: Test found login page for SQL injection
python main.py sqli --url "https://admin.target.com/login.php?user=admin" -o sqli.json

# Step 4: Test for XSS
python main.py xss --url "https://admin.target.com/search.php" --forms -o xss.json
```

## Need Help? / تحتاج مساعدة؟

```bash
# General help
python main.py --help

# Tool-specific help
python main.py sqli --help
python main.py xss --help
python main.py subdomain --help
python main.py dirbrute --help
python main.py login --help
```

---
**Remember: With great power comes great responsibility!**
**تذكر: مع القوة العظيمة تأتي المسؤولية العظيمة!**
