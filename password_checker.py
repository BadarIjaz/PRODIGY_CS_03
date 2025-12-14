import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import math
import random
import string

# --- Configuration ---
COMMON_PASSWORDS = ["password", "123456", "qwerty", "admin", "welcome", "iloveyou", "secret"]

def generate_strong_password():
    """Generates a random 12-character high-entropy password."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    # Ensure at least one of each type
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice("!@#$%^&*")
    ]
    # Fill the rest randomly
    password += [random.choice(chars) for _ in range(8)]
    random.shuffle(password)
    
    # Insert into entry field
    final_password = "".join(password)
    password_entry.delete(0, tk.END)
    password_entry.insert(0, final_password)
    check_password() # Trigger the check immediately

def copy_to_clipboard():
    """Copies the current password to the clipboard."""
    password = password_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showwarning("Empty", "Nothing to copy!")

def estimate_time_to_crack(entropy):
    guesses_per_second = 10**10 # 10 Billion guesses/sec
    total_combinations = 2 ** entropy
    seconds = total_combinations / guesses_per_second
    
    if seconds < 1: return "Instantly"
    if seconds < 60: return "A few seconds"
    if seconds < 3600: return f"{int(seconds // 60)} minutes"
    if seconds < 86400: return f"{int(seconds // 3600)} hours"
    if seconds < 31536000: return f"{int(seconds // 86400)} days"
    if seconds < 31536000 * 100: return f"{int(seconds // 31536000)} years"
    return "Centuries"

def calculate_entropy(password):
    pool_size = 0
    if re.search(r"[a-z]", password): pool_size += 26
    if re.search(r"[A-Z]", password): pool_size += 26
    if re.search(r"\d", password): pool_size += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): pool_size += 32
    
    if pool_size == 0: return 0
    entropy = len(password) * math.log2(pool_size)
    return entropy

def check_password(event=None):
    password = password_entry.get()
    feedback = []
    score = 0
    
    # Blacklist Check
    if password.lower() in COMMON_PASSWORDS:
        update_meter(0, 0, ["⚠️ Common password detected!", "• Do not use dictionary words"], "Instantly")
        return

    # Basic Rules
    if len(password) >= 8: score += 1
    else: feedback.append("• Too short (aim for 8+ chars)")
        
    if re.search(r"[A-Z]", password): score += 1
    else: feedback.append("• Add uppercase letters (A-Z)")
        
    if re.search(r"[a-z]", password): score += 1
    else: feedback.append("• Add lowercase letters (a-z)")
        
    if re.search(r"\d", password): score += 1
    else: feedback.append("• Add numbers (0-9)")
        
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password): score += 1
    else: feedback.append("• Add special chars (!@#$)")

    # Entropy & Timing
    entropy = calculate_entropy(password)
    crack_time = estimate_time_to_crack(entropy)
    
    update_meter(score, entropy, feedback, crack_time)

def update_meter(score, entropy, feedback, crack_time):
    feedback_label.config(text="")
    
    if score <= 2:
        strength_text = "Weak"
        color = "red"
        meter_value = 20
    elif score == 3 or score == 4:
        strength_text = "Moderate"
        color = "orange"
        meter_value = 60
    else:
        strength_text = "Strong"
        color = "#00b300" # Green
        meter_value = 100
        
    if entropy > 60 and score == 5:
        strength_text = "Very Strong"
        color = "blue"
        meter_value = 100

    result_label.config(text=f"Strength: {strength_text}", fg=color)
    time_label.config(text=f"Estimated Crack Time: {crack_time}", fg="#333")
    progress['value'] = meter_value
    
    style.configure("red.Horizontal.TProgressbar", foreground=color, background=color)
    progress.configure(style="red.Horizontal.TProgressbar")

    if feedback:
        feedback_text = "\n".join(feedback)
        feedback_label.config(text=f"Suggestions:\n{feedback_text}", fg="#555")
    elif password_entry.get() == "":
        result_label.config(text="Enter a password...", fg="black")
        time_label.config(text="")
        progress['value'] = 0

# --- GUI Setup ---
root = tk.Tk()
root.title("Prodigy InfoTech - Cyber Tool")
root.geometry("400x520") # Taller for new buttons
root.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')
style.configure("red.Horizontal.TProgressbar", background='red')

# Header
tk.Label(root, text="🛡️ Password Auditor", font=("Arial", 16, "bold"), pady=10).pack()

# Input Area
entry_frame = tk.Frame(root)
entry_frame.pack(pady=5)
password_entry = tk.Entry(entry_frame, width=25, font=("Arial", 12), show="*")
password_entry.pack(side=tk.LEFT, padx=5)
password_entry.bind("<KeyRelease>", check_password)

def toggle_visibility():
    if password_entry.cget('show') == '':
        password_entry.config(show='*')
        toggle_btn.config(text='👁')
    else:
        password_entry.config(show='')
        toggle_btn.config(text='🔒')

toggle_btn = tk.Button(entry_frame, text="👁", command=toggle_visibility, width=3)
toggle_btn.pack(side=tk.LEFT)

# Buttons Frame
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

# Generate Button
gen_btn = tk.Button(btn_frame, text="⚡ Generate Strong", command=generate_strong_password, bg="#ddd")
gen_btn.pack(side=tk.LEFT, padx=5)

# Copy Button
copy_btn = tk.Button(btn_frame, text="📋 Copy", command=copy_to_clipboard, bg="#ddd")
copy_btn.pack(side=tk.LEFT, padx=5)

# Progress Bar
progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=300, mode='determinate', style="red.Horizontal.TProgressbar")
progress.pack(pady=10)

# Labels
result_label = tk.Label(root, text="Enter a password...", font=("Arial", 14, "bold"))
result_label.pack()

time_label = tk.Label(root, text="", font=("Arial", 11, "italic"), fg="#333")
time_label.pack(pady=5)

feedback_label = tk.Label(root, text="", font=("Arial", 10), justify=tk.LEFT)
feedback_label.pack(pady=10)

root.mainloop()