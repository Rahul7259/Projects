
import re

# List of common weak passwords for basic analysis
COMMON_WEAK_PASSWORDS = [
    "123456", "password", "123456789", "12345678", "12345",
    "1234567", "1234567890", "qwerty", "abc123", "password1"
]

def calculate_password_strength(password):
    """Analyzes the strength of a password and returns a score."""
    score = 0
    feedback = []

    # Length check
    if len(password) < 8:
        feedback.append("Password is too short. Use at least 8 characters.")
    elif len(password) >= 8:
        score += 1
        if len(password) >= 12:
            score += 1  # Bonus for longer passwords

    # Check for variety of character types
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Include lowercase letters.")
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Include uppercase letters.")
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Include numbers.")
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Include special characters (e.g., !, @, #).")

    # Check against common weak passwords
    if password.lower() in COMMON_WEAK_PASSWORDS:
        feedback.append("Avoid using common passwords like '123456' or 'password'.")
    else:
        score += 1

    # Overall feedback
    if score < 4:
        feedback.append("Your password needs improvement. Aim for a mix of characters and a longer length.")
    elif score == 4:
        feedback.append("Your password is decent but could be stronger.")
    else:
        feedback.append("Your password is strong!")

    return score, feedback


def main():
    print("=== Password Strength Analyzer ===")
    password = input("Enter a password to analyze: ")

    score, feedback = calculate_password_strength(password)

    print("\nPassword Strength Score:", score, "/ 6")
    print("Feedback:")
    for tip in feedback:
        print("-", tip)


if __name__ == "__main__":
    main()
