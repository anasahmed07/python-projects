import re
import random
import string
import streamlit as st

# Array of commonly used weak passwords
COMMON_WEAK_PASSWORDS = [
    "123456", "12345678", "qwerty", "abc123", "monkey", "letmein",
    "dragon", "111111", "baseball", "iloveyou", "trustno1", "1234567",
    "sunshine", "master", "welcome", "shadow", "ashley", "football",
    "jesus", "ninja", "mustang", "password", "password1", "password123",
    "123123", "qwerty123", "admin", "login", "princess", "solo",
    "starwars", "12345", "superman", "hottie", "loveme", "zaq1zaq1",
    "zaq12wsx", "qazwsx", "qwertyuiop", "passw0rd", "michael", "killer",
    "robert", "daniel", "jordan", "jennifer", "zxcvbnm", "1q2w3e4r",
    "q1w2e3r4", "qwer1234", "asdfgh", "samsung", "11111", "1234"
]

def check_password_strength(password):
    score = 0
    suggestions = []
    
    if password.lower() in COMMON_WEAK_PASSWORDS:
        suggestions.append("🚫 Password is too common. Choose a less common password.")
        return 0, suggestions
    
    if len(password) >= 8:
        score += 2
    else:
        suggestions.append("❌ Password should be at least 8 characters long.")
    
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        suggestions.append("❌ Include both uppercase and lowercase letters.")
    
    if re.search(r"\d", password):
        score += 1
    else:
        suggestions.append("❌ Add at least one digit (0-9).")
    
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        suggestions.append("❌ Include at least one special character (!@#$%^&*).")
    
    return score, suggestions

def classify_password(score):
    """Returns a classification based on the score."""
    if score == 5:
        return "✅ Strong"
    elif 3 <= score <= 4:
        return "⚠️ Moderate"
    else:
        return "❌ Weak"

def generate_strong_password(length=10):
    min_letters = 2  
    min_digits = 1
    min_special = 1
    remaining = length - 4

    r1 = random.randint(0, remaining)
    r2 = random.randint(0, remaining - r1)
    r3 = remaining - r1 - r2

    n_letters = min_letters + r1
    n_digits = min_digits + r2
    n_special = min_special + r3

    uppercase = random.choice(string.ascii_uppercase)
    lowercase = random.choice(string.ascii_lowercase)
    n_remaining_letters = max(n_letters - 2, 0)
    letters = [random.choice(string.ascii_letters) for _ in range(n_remaining_letters)]
    letters.extend([uppercase, lowercase])
    
    digits = [random.choice(string.digits) for _ in range(n_digits)]
    specials = [random.choice("!@#$%^&*") for _ in range(n_special)]
    
    # Combine and shuffle
    password_list = letters + digits + specials
    random.shuffle(password_list)
    return "".join(password_list)

def update_password():
    password = st.session_state.password_input
    score, suggestions = check_password_strength(password)
    st.session_state.score = score
    st.session_state.suggestions = suggestions
    st.session_state.strength = classify_password(score)

def main():
    st.title("🔐 Password Strength Meter")
    st.write("Enter a password to check its strength and receive suggestions to improve it.")

    with st.container(border=True):
        st.subheader("📝 Password Strength Checker")
        
        st.text_input("Enter Password", type="password", key="password_input", on_change=update_password)
        
        if "password_input" in st.session_state and st.session_state.password_input:
            score = st.session_state.get("score", 0)
            if score == 5:
                color = "green"
            elif score >= 3:
                color = "orange"
            else:
                color = "red"
            st.markdown(f"""
            <style>
            div[data-testid="stTextInput"] input {{
                border: 4px solid {color} !important;
                border-radius: 5px;
                padding: 0.5rem;
            }}
            </style>
            """, unsafe_allow_html=True)
            
            strength = st.session_state.get("strength", "Not Evaluated")
            suggestions = st.session_state.get("suggestions", [])
            
            st.write(f"**Strength:** {strength}")
            st.write(f"**Score:** {score} / 5")
            
            if suggestions:
                st.write("**Suggestions:**")
                for suggestion in suggestions:
                    st.warning(f"- {suggestion}")
            else:
                st.success("Your password meets all the criteria!",icon="🎉")
    
    with st.container(border=True):
        st.subheader("🔑 Generate a Strong Password")
        desired_length = st.slider("Select Password Length", min_value=8, max_value=20, value=10)
        
        if st.button("Suggest a Strong Password"):
            strong_password = generate_strong_password(desired_length)
            st.write("**Suggested Strong Password:**")
            st.write("Copy the password and store it in a safe place.")
            st.code(strong_password, language="text")

if __name__ == '__main__':
    main()
