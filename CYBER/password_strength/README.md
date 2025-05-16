# README

## Project Overview

*   `manifest.json`: Defines metadata and configurations for the extension.
*   `popup.html`:  Defines the structure and content of the extension's popup window.
*   `popup.js`: Contains the JavaScript code that adds functionality and interactivity to the popup window.
*   `styles.css`:  Contains the CSS styles to control the appearance of the popup window.


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
This code is a manifest file (manifest.json) for a Chrome extension named "Password Strength Checker". Here's a breakdown:

*   **`manifest_version: 3`**: Specifies that the manifest file is using version 3 format, which is the latest version for Chrome extensions.
*   **`name: "Password Strength Checker"`**:  Defines the name of the extension as it will appear in the Chrome Web Store and in the Chrome extensions settings.
*   **`version: "1.0"`**:  Sets the version number of the extension to 1.0.  This is important for updates.
*   **`description: "A simple tool to check password strength"`**: Provides a brief description of the extension's purpose. This helps users understand what the extension does.
*   **`action`**: Configures the extension's popup window.
    *   **`default_popup: "popup.html"`**:  Specifies that the HTML file to be displayed when the extension's icon is clicked is "popup.html".
    *   **`default_icon: "icon64.png"`**: Sets the default icon for the extension to "icon64.png".
*   **`icons`**: Defines the icons used for the extension in various sizes.
    *   **`64: "icon64.png"`**: Specifies the 64x64 pixel icon file.
    *   **`96: "icon96.png"`**: Specifies the 96x96 pixel icon file.  Chrome uses different sizes depending on the context.
*   **`permissions: []`**: Declares the permissions the extension requires. This is an empty array, meaning the extension currently doesn't need any special permissions from the user.  If the extension needed to access the user's browsing history, for example, it would need to declare the `history` permission here.

In summary, this manifest file defines a simple Chrome extension that displays a popup (likely containing the password strength checker interface) when the extension icon is clicked. It has a name, version, description, icons, and doesn't require any special permissions.


- popup.html
### popup.html
This HTML code creates a simple password strength checker interface. Here's a breakdown:

*   **Title:** "Password Checker"
*   **Structure:** Uses `div` elements with classes like `container`, `input-group` to structure the content.
*   **Input:** Includes a password input field (`passwordInput`) where users enter their password and a button (`showPassword`) to toggle password visibility.
*   **Strength Meter:** Displays a strength meter (`strengthMeter` with a progress bar inside `strengthBar`) to visually represent the password's strength.
*   **Strength Text:** Shows a text label (`strengthText`) to describe the password strength (e.g., Weak, Medium, Strong).
*   **Requirements List:**  An unordered list (`requirements`)  displays the password requirements (length, uppercase, lowercase, number, special character).  Each requirement has a unique `id` for possible javascript interaction (e.g., `length`, `uppercase`).
*   **Generate Password Button:** A button (`generatePassword`) allows the user to generate a random password.
*   **JavaScript:** Includes a script file `popup.js`, which will likely contain the logic for the password strength evaluation, updating the strength meter/text, and handling the "Show Password" and "Generate Password" button functionalities.
*   **CSS:** Includes a stylesheet `styles.css` to handle visual presentation and layout.

In essence, this HTML sets up the visual framework for a password strength checker that relies on JavaScript for the actual functionality.


- popup.js
### popup.js
This JavaScript code implements a password strength checker and random password generator.

**Functionality:**

1.  **Password Input and Generation:**
    *   Listens for input changes in the `passwordInput` field and triggers the `checkPasswordStrength` function.
    *   Generates a random password of 15 characters using `generateRandomPassword` when the `generatePassword` button is clicked, populates the `passwordInput` field with it, and then calls `checkPasswordStrength`.
    *   Toggles the visibility of the password in the `passwordInput` field between plain text and masked (password) when the `showPassword` button is clicked.

2.  **Password Strength Check (`checkPasswordStrength`):**
    *   Checks if the password meets the following criteria:
        *   Minimum length of 8 characters.
        *   Contains at least one uppercase letter.
        *   Contains at least one lowercase letter.
        *   Contains at least one number.
        *   Contains at least one special character.
    *   Updates the visual indicators (likely list items with IDs 'length', 'uppercase', 'lowercase', 'number', 'special') by adding or removing the `valid` class, likely changing their appearance based on whether the criteria are met.
    *   Calculates a strength score based on the number of criteria met (20 points per criteria).
    *   Updates a progress bar (`strengthBar`)'s width to reflect the calculated strength score.
    *   Changes the color of the progress bar and the text of the `strengthText` element to indicate the password's strength:
        *   Red: Weak (strength < 40)
        *   Orange: Medium (strength < 80)
        *   Green: Strong (strength >= 80)

3.  **Random Password Generation (`generateRandomPassword`):**
    *   Creates a password by guaranteeing at least one character from each of the following character sets: lowercase, uppercase, numbers, and special characters.
    *   Fills the rest of the password up to the specified length (defaulting to 15) with random characters from all character sets.
    *   Shuffles the generated password to distribute the required characters randomly.
    *   Returns the generated random password.

**In Summary:**

The code provides a user interface for entering or generating a password. It dynamically assesses the password's strength based on several criteria (length, uppercase, lowercase, numbers, special characters), provides visual feedback using a progress bar and text indicator, and allows the user to toggle the password's visibility. The password generator creates strong, random passwords by including at least one character from each of the common character sets.


- styles.css
### styles.css
This CSS code styles a password strength checker interface. Here's a breakdown:

*   **General Body Styling:** Sets the body width, padding, font, and margin.
*   **Container Styling:** Uses flexbox to arrange elements in a column with spacing (gap).
*   **Password Input:** Styles the password input field with padding, border, and rounded corners.
*   **Strength Meter:** Creates a visual strength meter with a grey background and rounded corners.
*   **Strength Bar:** Represents the password strength within the meter. It uses `width` and `background-color` properties, with transitions for smooth updates.
*   **Requirements List:** Styles the list of password requirements, setting a default grey color and a green color for requirements that are met (`.valid` class).
*   **Button Styling:** Styles buttons with background color, text color, border radius, and cursor pointer.  Includes a hover effect for visual feedback.
*   **Button Container Styling:** Uses flexbox to evenly space the buttons in their container.
*   **Input Group Styling:** A container to group elements, in this case input and the password strength indicators, into a flexbox column layout.


