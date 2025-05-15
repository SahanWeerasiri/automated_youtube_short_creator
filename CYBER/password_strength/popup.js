document.getElementById('passwordInput').addEventListener('input', function (e) {
    const password = e.target.value;
    checkPasswordStrength(password);
});

document.getElementById('generatePassword').addEventListener('click', function () {
    const password = generateRandomPassword();
    document.getElementById('passwordInput').value = password;
    checkPasswordStrength(password);
});

document.getElementById('showPassword').addEventListener('click', function () {
    const passwordInput = document.getElementById('passwordInput');
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        this.textContent = 'Hide Password';
    } else {
        passwordInput.type = 'password';
        this.textContent = 'Show Password';
    }
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

function generateRandomPassword(length = 15) {
    // Define character sets
    const lowercase = "abcdefghijklmnopqrstuvwxyz";
    const uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const numbers = "0123456789";
    const specials = "!@#$%^&*()_+[]{}|<>?";

    // Ensure we have at least one of each required character type
    let password = [
        lowercase[Math.floor(Math.random() * lowercase.length)],
        uppercase[Math.floor(Math.random() * uppercase.length)],
        numbers[Math.floor(Math.random() * numbers.length)],
        specials[Math.floor(Math.random() * specials.length)]
    ].join('');

    // Fill the rest with random characters from all sets
    const allChars = lowercase + uppercase + numbers + specials;
    while (password.length < length) {
        const randomIndex = Math.floor(Math.random() * allChars.length);
        password += allChars[randomIndex];
    }

    // Shuffle the password to mix the required characters
    return password.split('').sort(() => Math.random() - 0.5).join('');
}