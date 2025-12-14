# Password Checker: Code Analysis & Walkthrough

This document provides a technical deep-dive into the `password_checker.py` implementation. It outlines the algorithmic logic, Regular Expressions (Regex), and GUI event handling used to evaluate security.

## Core Concepts
To implement this tool effectively, three key Python concepts were utilized:

1. **Regular Expressions (`re`)**: A powerful sequence of characters that specifies a search pattern (e.g., `[A-Z]` searches for uppercase letters).
2. **Shannon Entropy (`math`)**: A mathematical formula used to estimate the "information density" or randomness of the password strings.
3. **Event-Driven Programming (`tkinter`)**: The code waits for specific user actions (like lifting a key) to trigger functions immediately.

---

## Logic Breakdown

### 1. Calculating Entropy (Math Logic)
This function determines the mathematical difficulty of guessing the password.

```python
def calculate_entropy(password):
    pool_size = 0
    if re.search(r"[a-z]", password): pool_size += 26
    if re.search(r"[A-Z]", password): pool_size += 26
    if re.search(r"\d", password): pool_size += 10
    if re.search(r"[!@#$%^&*...]", password): pool_size +=32 
```

**pool_size:** We first determine the "universe" of characters the password is drawn from.  
If lowercase exists, we add 26 possibilities.
If digits exist, we add 10 possibilities.
The larger the pool, the harder the password is to brute-force.

```
if pool_size == 0:
        return 0
    entropy = len(password) * math.log2(pool_size)
    return entropy
```

**The Formula:** Entropy = Length x log_2(PoolSize).  
**math.log2:** Calculates how many "bits" of information each character represents.  
**Result:** A password with higher entropy is exponentially harder to crack.


### 2 Estimating Crack Time
We translate the abstract "Entropy" score into a human-readable time estimate.

```python
def estimate_time_to_crack(entropy):
    guesses_per_second = 10**10 # 10 Billion guesses/sec
    total_combinations = 2 ** entropy
    seconds = total_combinations / guesses_per_second
    
    if seconds < 60: return "A few seconds"
    # ... conversion logic (seconds -> years) ...
```

**Assumption:** We assume a hacker is using a powerful GPU rig capable of trying 10 billion passwords per second.   
**Calculation:** Total Combinations / Speed = Time in Seconds.   
**Output:** Converts the raw seconds into "Minutes", "Days", or "Centuries" to give the user realistic feedback.

### 3. Security First: Blacklist Check
Before running complex math, the code checks if the password is a known weak credential.

```python
COMMON_PASSWORDS = ["password", "123456", "qwerty", "admin", ...]

def check_password(event=None):
    if password.lower() in COMMON_PASSWORDS:
        update_meter(0, 0, ["⚠️ Common password detected!"], "Instantly")
        return
```

**COMMON_PASSWORDS List:** A predefined list of the most hacked passwords.   
**Logic:** If the user's input matches a word in this list, we immediately flag it as "Weak" and skip the rest of the calculations. This prevents passwords like "Password123!" from getting a high score just because they contain numbers and symbols.

### 4. The Validation Logic (Regex)
This function runs the standard security rules against the user's input.

```python
def check_password(event=None):
    password = password_entry.get()
    
    # Criterion: Uppercase Letters
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("• Add uppercase letters (A-Z)")
```

**re.search(r"[A-Z]", password):** This scans the string password. If it finds at least one capital letter, it returns a match object (True).  
**score += 1:** If the condition is met, we increment the security score.  
**feedback.append(...):** If the condition fails, we add a specific tip to the list, which will later be displayed to the user.


### 5 Password Generation Logic
To solve the user's problem, we generate a high-strength password programmatically.

```python
def generate_strong_password():
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*")
    ]
    password += [random.choice(chars) for _ in range(8)]
    random.shuffle(password)
```

**Mandatory Inclusion:** We ensure at least one of every character type (Upper, Lower, Digit, Symbol) is present. Random Filling: We fill the remaining length (up to 12 chars) with random selections. Shuffle: We shuffle the final list so the mandatory characters aren't always at the start.


### 6. Dynamic UI Updates
This function translates the numerical score into visual feedback for the user.

```python
def update_meter(score, entropy, feedback, crack_time):
    # Standard Rules
    if score <= 2:
        strength_text = "Weak"
        color = "red"
    elif score == 3 or score == 4:
        strength_text = "Moderate"
        color = "orange"
    else:
        strength_text = "Strong"
        color = "#00b300" # Green

    # Bonus: High Entropy Check
    if entropy > 60 and score == 5:
        strength_text = "Very Strong (High Entropy!)"
        color = "blue"
```

**Logic:** We use conditional statements (if/elif) to set the UI properties. Visuals:    

**Red:** Weak (Score 0-2).  
**Orange:** Moderate (Score 3-4).  
**Green:** Strong (Score 5).  
**Blue:** Reserved for passwords that are mathematically very difficult to crack (High Entropy).    
**High Entropy Bonus:** Even if a password meets all rules (Score 5), it might be short. This check ensures only mathematically tough passwords get the "Blue" rating.


### 7. Real-Time Event Binding
This is what makes the tool feel responsive.

```python
password_entry.bind("<KeyRelease>", check_password)
```

**KeyRelease:** This is a specific Tkinter event. It fires the moment the user lifts their finger off a key.  
**Result:** The check_password function runs instantly after every keystroke, updating the bar dynamically without needing a "Submit" button.

### 8. Visibility Toggle (UX)
A convenience feature for the user.

```python
def toggle_visibility():
    if password_entry.cget('show') == '':
        password_entry.config(show='*')
    else:
        password_entry.config(show='')
```

**config(show='*'):** This tells the entry field to mask characters (standard password protection).  
**config(show=''):** Setting this to an empty string reveals the plain text, allowing the user to check for typos.

### 9. Execution Control

```python 
root.mainloop()
```

**mainloop():** This method puts the script into an infinite loop, waiting for user events (clicks, typing). The window remains open until the user explicitly closes it.
