# Building a Chrome Extension for Password Strength Checking

Here's a step-by-step guide to create a simple password strength checker Chrome extension:

## 1. Create the Basic Extension Structure

Create a folder for your extension with these files:

```
password-strength-checker/
├── manifest.json
├── popup.html
├── popup.js
├── styles.css
└── icon.png (optional)
```

## 2. manifest.json

```json
{
  "manifest_version": 3,
  "name": "Password Strength Checker",
  "version": "1.0",
  "description": "A simple tool to check password strength",
  "action": {
    "default_popup": "popup.html",
    "default_icon": "icon.png"
  },
  "icons": {
    "16": "icon.png",
    "48": "icon.png",
    "128": "icon.png"
  },
  "permissions": []
}
```

## 3. popup.html

```html
<!DOCTYPE html>
<html>
<head>
  <title>Password Checker</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="container">
    <h2>Password Strength Checker</h2>
    <input type="password" id="passwordInput" placeholder="Enter password">
    <div id="strengthMeter">
      <div id="strengthBar"></div>
    </div>
    <div id="strengthText">Strength: </div>
    <ul id="requirements">
      <li id="length">At least 8 characters</li>
      <li id="uppercase">Contains uppercase letter</li>
      <li id="lowercase">Contains lowercase letter</li>
      <li id="number">Contains number</li>
      <li id="special">Contains special character</li>
    </ul>
  </div>
  <script src="popup.js"></script>
</body>
</html>
```

## 4. styles.css

```css
body {
  width: 250px;
  padding: 10px;
  font-family: Arial, sans-serif;
}

.container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

#passwordInput {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

#strengthMeter {
  height: 10px;
  background-color: #eee;
  border-radius: 5px;
  margin-bottom: 10px;
}

#strengthBar {
  height: 100%;
  width: 0%;
  border-radius: 5px;
  transition: width 0.3s, background-color 0.3s;
}

#requirements {
  padding-left: 20px;
}

#requirements li {
  margin-bottom: 5px;
  color: #777;
}

#requirements li.valid {
  color: #2ecc71;
}
```

## 5. popup.js

```javascript
document.getElementById('passwordInput').addEventListener('input', function(e) {
  const password = e.target.value;
  checkPasswordStrength(password);
});

function checkPasswordStrength(password) {
  // Check requirements
  const hasMinLength = password.length >= 8;
  const hasUpperCase = /[A-Z]/.test(password);
  const hasLowerCase = /[a-z]/.test(password);
  const hasNumber = /[0-9]/.test(password);
  const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);
  
  // Update requirement list
  document.getElementById('length').classList.toggle('valid', hasMinLength);
  document.getElementById('uppercase').classList.toggle('valid', hasUpperCase);
  document.getElementById('lowercase').classList.toggle('valid', hasLowerCase);
  document.getElementById('number').classList.toggle('valid', hasNumber);
  document.getElementById('special').classList.toggle('valid', hasSpecialChar);
  
  // Calculate strength score (0-100)
  let strength = 0;
  if (hasMinLength) strength += 20;
  if (hasUpperCase) strength += 20;
  if (hasLowerCase) strength += 20;
  if (hasNumber) strength += 20;
  if (hasSpecialChar) strength += 20;
  
  // Update strength meter
  const strengthBar = document.getElementById('strengthBar');
  strengthBar.style.width = strength + '%';
  
  // Set color based on strength
  if (strength < 40) {
    strengthBar.style.backgroundColor = '#e74c3c'; // Red
    document.getElementById('strengthText').textContent = 'Strength: Weak';
  } else if (strength < 80) {
    strengthBar.style.backgroundColor = '#f39c12'; // Orange
    document.getElementById('strengthText').textContent = 'Strength: Medium';
  } else {
    strengthBar.style.backgroundColor = '#2ecc71'; // Green
    document.getElementById('strengthText').textContent = 'Strength: Strong';
  }
}
```

## 6. Load the Extension in Chrome

1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select your extension folder

## Optional Enhancements

1. **Add a password generator**:
   ```javascript
   function generatePassword() {
     const length = 12;
     const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()";
     let password = "";
     for (let i = 0; i < length; i++) {
       password += charset.charAt(Math.floor(Math.random() * charset.length));
     }
     document.getElementById('passwordInput').value = password;
     checkPasswordStrength(password);
   }
   ```

2. **Add zxcvbn library** for more advanced password strength checking:
   - Include the library in your project
   - Replace the simple checker with zxcvbn's algorithm

3. **Add options page** to customize requirements

This extension provides real-time feedback on password strength as the user types, with visual indicators for which requirements are met. The strength meter changes color based on the calculated strength.