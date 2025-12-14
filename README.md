# PRODIGY_CS_03
## Task-03: Password Complexity Checker & Generator

This repository contains a Python-based Graphical User Interface (GUI) tool that assesses password strength and helps users generate secure credentials. It goes beyond basic rule checking by calculating **Shannon Entropy** to estimate how long a password would take to crack.

### Usage
1. Run the script: `password_checker.py`
2. **Type** a password to see real-time strength analysis and crack-time estimation.
3. **Click "⚡ Generate Strong"** to instantly create a secure, high-entropy password.
4. **Click "📋 Copy"** to save the password to your clipboard.

### Watch the Demo Video
[Click to view the demo](password_checker_demo.mp4)

### Features & Logic
* **Real-Time Analysis:** Instant feedback on password strength (Weak/Moderate/Strong).
* **Time-to-Crack Estimation:** Calculates how long a brute-force attack would take (e.g., "3 days" vs "400 centuries") based on entropy.
* **Secure Generator:** Creates random, high-entropy 12-character passwords using Python's `random` and `string` libraries.
* **Common Password Detection:** Instantly flags weak passwords like "123456" or "password" using a blacklist check.
* **Visual Feedback:** The progress bar changes color (Red → Orange → Green → Blue) based on the security score.

### Example

**Weak Password:**
* **Input:** `password`
* **Output:** Red Bar, Suggestion: "⚠️ Common password detected!"

**Strong Password:**
* **Input:** `Tr0ub4dor&3`
* **Output:** Blue Bar, Result: "Very Strong", Estimated Crack Time: "Centuries"