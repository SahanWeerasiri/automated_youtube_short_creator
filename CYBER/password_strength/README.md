# README

## Project Overview

This project is a Python application.

## Project Structure

The project structure is as follows:

```
- icon64.png
- icon96.png
- manifest.json
- method.md
- popup.html
- popup.js
- styles.css
```

## Project Details

This project contains the following files:

- manifest.json
### manifest.json
This code is a manifest file for a Chrome extension called "Password Strength Checker". Here's a breakdown:

*   **`manifest_version: 3`**:  Specifies that the extension uses Manifest V3, the latest version of the manifest file format.
*   **`name: "Password Strength Checker"`**:  Sets the name of the extension as it will appear in the Chrome Web Store and in the browser's extensions manager.
*   **`version: "1.0"`**:  Indicates the version number of the extension.
*   **`description: "A simple tool to check password strength"`**:  Provides a brief description of the extension's purpose.
*   **`action`**:  Defines the extension's user interface. In this case:
    *   **`default_popup: "popup.html"`**: Specifies that `popup.html` is the HTML file that will be displayed when the extension's icon is clicked.
    *   **`default_icon: "icon64.png"`**: Sets the default icon for the extension.
*   **`icons`**:  Provides different sized icons for the extension, used in various places within the browser and Chrome Web Store.
    *   **`64: "icon64.png"`**
    *   **`96: "icon96.png"`**
*   **`permissions: []`**:  Indicates that the extension doesn't require any special permissions to access user data or browser functionalities. An empty array means no permissions are requested.

In short, it defines a simple extension with a popup UI (`popup.html`) that checks password strength and doesn't require any specific permissions.


- popup.html
### popup.html
This HTML code creates a simple password strength checker interface. Here's a breakdown:

*   **Title:** "Password Checker"
*   **CSS Link:** Links to an external stylesheet named "styles.css".
*   **Container:**  A main `div` with class "container" to hold the password checker elements.
*   **Heading:**  An `h2` tag displaying "Password Strength Checker".
*   **Input Field:**  A `div` with class "input-group" contains:
    *   A password input field (`input type="password"`) with the ID "passwordInput" and a placeholder "Enter password".
    *   A button with the ID "showPassword" and the text "Show Password" to toggle password visibility.
*   **Strength Meter:** A `div` with the ID "strengthMeter" containing:
    *   A `div` with the ID "strengthBar" to visually represent password strength.
*   **Strength Text:**  A `div` with the ID "strengthText" displays "Strength: ".  The actual strength level will likely be updated dynamically via JavaScript.
*   **Requirements List:** An unordered list (`ul`) with the ID "requirements" containing `li` elements specifying password criteria. Each `li` has a unique ID (length, uppercase, lowercase, number, special). These `li`s will likely be updated with styling via JavaScript to indicate whether the password meets each requirement.
*   **Generate Password Button:** Another container with a button to generate a random password.
*   **JavaScript Link:** Links to an external JavaScript file named "popup.js", which will handle the logic for password strength calculation, visibility toggle, and password generation.


- popup.js
### popup.js
This Javascript code implements a password strength checker and generator. Here's a breakdown:

**Functionality:**

*   **Password Input and Event Listeners:**
    *   Listens for `input` events on an HTML element with the ID `passwordInput`. When the password field is changed, it calls the `checkPasswordStrength` function to analyze the entered password.
    *   Listens for `click` events on an HTML element with the ID `generatePassword`. When clicked, it generates a random password using the `generateRandomPassword` function, populates the `passwordInput` field with the generated password, and calls `checkPasswordStrength` to analyze it.
    *   Listens for `click` events on an HTML element with the ID `showPassword`. When clicked, it toggles the visibility of the password in the `passwordInput` field between plain text and obscured (password) by changing the `type` attribute.  It also updates the button text to "Show Password" or "Hide Password" accordingly.

*   **`checkPasswordStrength(password)` Function:**
    *   **Requirements Checking:** Determines if the password meets the following criteria:
        *   Minimum length of 8 characters.
        *   Contains at least one uppercase letter.
        *   Contains at least one lowercase letter.
        *   Contains at least one number.
        *   Contains at least one special character (defined in the regex).
    *   **Requirement List Update:**  Uses the `classList.toggle` method to add or remove the class "valid" from HTML elements with the IDs `length`, `uppercase`, `lowercase`, `number`, and `special`.  This likely updates the visual styling of these elements (e.g., changing color) to indicate whether the corresponding requirement is met.
    *   **Strength Calculation:** Assigns a strength score (0-100) based on the number of requirements met (20 points per requirement).
    *   **Strength Meter Update:**
        *   Updates the width of an HTML element with the ID `strengthBar` to visually represent the password strength.
        *   Changes the background color of the `strengthBar` and the text content of the `strengthText` element based on the strength score to display a "Weak", "Medium", or "Strong" indicator.

*   **`generateRandomPassword(length = 15)` Function:**
    *   **Character Sets:** Defines strings containing lowercase letters, uppercase letters, numbers, and special characters.
    *   **Guaranteed Characters:** Ensures the generated password contains at least one character from each character set by randomly selecting one from each and concatenating them.
    *   **Filling Remaining Length:**  Fills the remaining characters of the password with random characters from all character sets until the desired length is reached.
    *   **Shuffling:** Shuffles the characters in the generated password to randomize the order and ensure the guaranteed characters aren't always at the beginning. Returns the randomized password.

**In essence, the code provides a real-time password strength evaluation as the user types, generates a random password that meets specific complexity requirements, and allows the user to toggle the visibility of the password field.**


- styles.css
### styles.css
The CSS code provides styling for a password strength meter and its associated elements. Here's a breakdown:

*   **`body`:** Sets the overall style for the body, defining width, padding, and font.
*   **`.container`:** Uses flexbox to arrange elements in a column with a 10px gap between them.
*   **`#passwordInput`:** Styles the password input field with padding, border, and rounded corners.
*   **`#strengthMeter`:** Styles the container for the strength bar, giving it height, background color, and rounded corners.
*   **`#strengthBar`:** Styles the actual strength bar inside the meter. Its width dynamically changes to represent the password strength, and it transitions smoothly with background color changes.
*   **`#requirements`:** Styles the list of password requirements with left padding.
*   **`#requirements li`:** Styles each list item, giving it a default color and a different color (`#2ecc71`) when the requirement is met (class `.valid`).
*   **`.button`:** Styles buttons with padding, background color, text color, no border, rounded corners, and a pointer cursor. Also, it has a hover effect.
*   **`#buttonContainer`:** Uses flexbox to arrange buttons horizontally with space in between.
*   **`#input-group`:** Styles the grouping of the input field by using flexbox to arrange items into a column.


