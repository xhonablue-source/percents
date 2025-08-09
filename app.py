import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime
import requests  # <-- for Dr. X

# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(
    page_title="MathCraft: The Power of Percents",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# Session state (progress, badges)
# -------------------------------
if "xp" not in st.session_state:
    st.session_state.xp = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "badges" not in st.session_state:
    st.session_state.badges = set()
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {time, module, prompt, user_answer, correct, feedback, xp}

def award_xp(amount, reason, module):
    st.session_state.xp += amount
    st.session_state.history.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "module": module,
        "prompt": reason,
        "user_answer": "",
        "correct": True,
        "feedback": f"+{amount} XP",
        "xp": st.session_state.xp
    })
    if st.session_state.xp >= 50:
        st.session_state.badges.add("Percent Apprentice")
    if st.session_state.xp >= 120:
        st.session_state.badges.add("Discount Detective")
    if st.session_state.xp >= 250:
        st.session_state.badges.add("Tax & Tip Pro")
    if st.session_state.streak >= 5:
        st.session_state.badges.add("Streak Master")

def record_result(module, prompt, user_answer, correct, feedback, xp_gain=0):
    if correct:
        st.session_state.streak += 1
        if xp_gain:
            st.session_state.xp += xp_gain
    else:
        st.session_state.streak = 0
    st.session_state.history.append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "module": module,
        "prompt": prompt,
        "user_answer": str(user_answer),
        "correct": bool(correct),
        "feedback": feedback,
        "xp": st.session_state.xp
    })
    if st.session_state.streak >= 5:
        st.session_state.badges.add("Streak Master")

# -------------------------------
# Dr. X LLM Integration (from your config)
# -------------------------------
def ask_drx(message: str) -> str:
    try:
        response = requests.post(
            'https://ask-drx-730124987572.us-central1.run.app',
            json={'message': message},
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get('reply', "Sorry, I couldn't process that.")
        else:
            return f"I'm having trouble connecting right now. Server responded with status {response.status_code}. Please try again."
    except requests.exceptions.Timeout:
        return "I'm having trouble connecting right now. The request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return "I'm having trouble connecting right now. There was a network error. Please check your internet connection and try again."
    except Exception as e:
        return f"I'm having trouble connecting right now. An unexpected error occurred: {e}. Please try again."

# System-style instructions we’ll prepend to user content for a Socratic math coach
DRX_SYSTEM = (
    "You are Dr. X, a friendly math coach for middle/high school students. "
    "Goal: help the student DESIGN their own percent problem and SOLVE it with reasoning. "
    "Teach percent ↔ decimal ↔ fraction, percent of a number, and percent change. "
    "Use short steps, ask one question at a time, check understanding often, and encourage mental math estimation. "
    "Require students to show: (1) convert % to decimal, (2) set up equation, (3) compute, (4) sanity check. "
    "Do NOT just give the final answer unless the student has attempted; nudge with hints first. "
)

# -------------------------------
# Custom CSS (playful theme)
# -------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka+One&family=Roboto:wght@400;700&display=swap');
    body { font-family: 'Roboto', sans-serif; color: #4a4a4a; }
    .main-header {
        background: linear-gradient(135deg, #ff6b6b, #ffa07a);
        color: #ffffff; padding: 2.5rem; border-radius: 20px;
        text-align: center; margin-bottom: 2rem; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .main-header h1 { font-family: 'Fredoka One', cursive; font-size: 3.5rem; text-shadow: 3px 3px 6px rgba(0,0,0,0.4); }
    .main-header h3 { font-family: 'Fredoka One', cursive; font-size: 1.5rem; }
    .module-card {
        background: #fff8f0; color: #4a4a4a; padding: 1.5rem; border-radius: 15px;
        margin: 1rem 0; box-shadow: 0 5px 10px rgba(0,0,0,0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .module-card:hover { transform: translateY(-3px); box-shadow: 0 8px 15px rgba(0,0,0,0.15); }
    .concept-box { background: #fff0d9; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 5px solid #ff6b6b; }
    .activity-box { background: #e6f9ff; padding: 1.5rem; border-radius: 10px; margin: 1rem 0; border-left: 5px solid #ffa07a; }
    .standards-box { background: #f0e6ff; padding: 1rem; border-radius: 10px; margin: 1rem 0; border-left: 5px solid #9c27b0; }
    .stButton>button {
        background-color: #ffa07a; color: white; border-radius: 8px; padding: 0.5rem 1rem; border: none;
        transition: background-color 0.2s ease, transform 0.2s ease;
    }
    .stButton>button:hover { background-color: #ff8c69; transform: translateY(-2px); }
    h1, h2, h3, h4, h5, h6 { font-family: 'Fredoka One', cursive; color: #4a4a4a; }
    p, li, div, label, span { font-family: 'Roboto', sans-serif; font-weight: 400; color: #4a4a4a; }
    .st-bb { background-color: #fff8f0; }
    .badge {
        display: inline-block; margin: 0.25rem 0.35rem; padding: 0.35rem 0.6rem;
        border-radius: 999px; background: #ffe1c9; border: 1px solid #ff9a76; font-weight: 700; color: #8a4b2f;
    }
    .chat-bubble-user { background:#ffe7da; padding:.75rem 1rem; border-radius:12px; margin:.35rem 0; }
    .chat-bubble-assistant { background:#e9f7ff; padding:.75rem 1rem; border-radius:12px; margin:.35rem 0; }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Header with live progress
# -------------------------------
st.markdown("""
<div class="main-header">
    <h1>🎨 MathCraft 🔢</h1>
    <h3>The Power of Percents: A Middle School Curriculum</h3>
    <p>Unlock the secrets of fractions, decimals, percentages — with hands-on labs & real receipts!</p>
</div>
""", unsafe_allow_html=True)

top_cols = st.columns([2,1,1])
with top_cols[0]:
    st.markdown("**Progress**")
    st.progress(min(st.session_state.xp % 100 / 100, 1.0))
with top_cols[1]:
    st.metric("⭐ XP", st.session_state.xp)
with top_cols[2]:
    st.metric("🔥 Streak", st.session_state.streak)

if st.session_state.badges:
    st.markdown("**Badges:** " + " ".join([f"<span class='badge'>{b}</span>" for b in sorted(st.session_state.badges)]), unsafe_allow_html=True)

# -------------------------------
# Sidebar navigation
# -------------------------------
st.sidebar.title("📚 Modules")
page = st.sidebar.selectbox(
    "Choose a section:",
    [
        "🏠 Home & Overview",
        "🔍 The Basics of Percents",
        "🎛️ Conversion Lab (%, decimal, fraction)",
        "✖️ Percent of a Number",
        "📈 Percent Change & Discounts",
        "🧾 Tax & Tip Receipt Builder",
        "💼 Commission & Simple Interest",
        "🧩 Word Problem Generator",
        "🤖 Design-Your-Own Percent Problem (Dr. X)",   # NEW
        "🧠 Quiz: The Percent Power-Up",
        "📚 External Resources",
        "📤 Export Progress"
    ]
)

# -------------------------------
# Helper functions & visuals
# -------------------------------
def percent_to_decimal(p):  # p in [0,100]
    return p / 100

def decimal_to_percent(d):  # d in [0,1]
    return d * 100

def fraction_to_percent(num, den):
    if den == 0:
        return None
    return (num / den) * 100

def draw_percent_bar(pct, color='#ff6b6b'):
    fig, ax = plt.subplots(figsize=(8, 1))
    ax.barh([0], [pct], color=color)
    ax.barh([0], [100 - pct], left=[pct], color='#e0e0e0')
    ax.set_xlim(0, 100); ax.set_yticks([]); ax.set_xticks([0, 25, 50, 75, 100])
    ax.text(min(pct/2, 95), 0, f'{pct:.0f}%', ha='center', va='center', color='white', fontsize=16)
    st.pyplot(fig)

def draw_10x10_grid(pct):
    filled = int(round(pct))
    fig, ax = plt.subplots(figsize=(4,4))
    grid = np.zeros((10,10))
    count = 0
    for r in range(10):
        for c in range(10):
            if count < filled:
                grid[r,c] = 1
                count += 1
    ax.imshow(grid, cmap='Greys', vmin=0, vmax=1)
    ax.set_xticks(np.arange(-.5, 10, 1)); ax.set_yticks(np.arange(-.5, 10, 1))
    ax.set_xticklabels([]); ax.set_yticklabels([])
    ax.grid(color='black', linestyle='-', linewidth=0.5)
    ax.set_title(f"{pct:.0f}% shaded")
    st.pyplot(fig)

def draw_pie(percent):
    sizes = [percent, 100 - percent]
    labels = [f"{percent:.0f}%", ""]
    fig, ax = plt.subplots(figsize=(3,3))
    ax.pie(sizes, labels=labels, startangle=90, counterclock=False, autopct=None)
    ax.axis('equal')
    st.pyplot(fig)

def check_numeric_answer(user_value, correct_value, tol=1e-6):
    try:
        return abs(float(user_value) - float(correct_value)) <= tol
    except:
        return False

# -------------------------------
# Home & overview
# -------------------------------
if page == "🏠 Home & Overview":
    st.header("Welcome to MathCraft: The Power of Percents!")
    st.markdown("""
    Percent means “per 100.” In this lab you’ll convert between **fractions**, **decimals**, and **percents**,
    compute **discounts**, **tax**, **tips**, **commission**, and **simple interest**, build real **receipts**, and chat with **Dr. X** to design your own problem.
    """)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="module-card">
            <h3>What you'll master</h3>
            <ul>
                <li>🧭 Convert between % ↔ decimal ↔ fraction</li>
                <li>🧮 Percent of a number</li>
                <li>🏷️ Discounts, tax, and tip</li>
                <li>📈 Percent change</li>
                <li>🤖 Socratic coaching with Dr. X</li>
            </ul>
            <small><b>Standards:</b> 6.RP.A.3c, 7.RP.A.2b, 7.RP.A.3</small>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="module-card">
            <h3>How to level up</h3>
            <ul>
                <li>Earn ⭐ XP for correct answers</li>
                <li>Build 🔥 streaks for consecutive wins</li>
                <li>Collect 🎖️ badges</li>
                <li>Export a 📤 progress report</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    if st.button("Claim your Starter Bonus (+10 XP)"):
        award_xp(10, "Starter Bonus", "Home")

# -------------------------------
# Basics of Percents (visual lab)
# -------------------------------
elif page == "🔍 The Basics of Percents":
    st.header("🔍 Module 1: The Basics of Percents")
    st.markdown("""
    <div class="standards-box">
        <strong>📚 Standards:</strong> 6.RP.A.3c, 7.RP.A.3
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="activity-box">
        <h4>🎯 The Percent Visualizer</h4>
        <p>Slide to change the percent and see its decimal and fraction forms with visuals.</p>
    </div>
    """, unsafe_allow_html=True)

    percent_value = st.slider("Select a percentage", 0, 100, 40, 1)
    decimal_value = percent_to_decimal(percent_value)
    st.markdown(f"""
    <div class="concept-box">
        <ul>
            <li><b>As a Decimal:</b> {percent_value}% = {decimal_value}</li>
            <li><b>As a Fraction:</b> {percent_value}% = {percent_value}/100 = {percent_value/100:.2f} of the whole</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    v1, v2, v3 = st.columns([3,3,2])
    with v1:
        st.caption("Percent Bar")
        draw_percent_bar(percent_value)
    with v2:
        st.caption("10×10 Grid")
        draw_10x10_grid(percent_value)
    with v3:
        st.caption("Pie View")
        draw_pie(percent_value)

# -------------------------------
# Conversion Lab
# -------------------------------
elif page == "🎛️ Conversion Lab (%, decimal, fraction)":
    st.header("🎛️ Conversion Lab")
    st.markdown("Practice converting between **percent**, **decimal**, and **fraction**.")

    tab1, tab2, tab3 = st.tabs(["Percent → Decimal", "Decimal → Percent", "Fraction → Percent"])
    with tab1:
        p = st.number_input("Enter a percent (%)", 0.0, 100.0, 25.0, 0.1)
        st.write(f"Decimal = {percent_to_decimal(p)}")
        if st.button("Check understanding (Percent → Decimal)"):
            record_result("Conversion", "Percent→Decimal", p, True, "Converted.", xp_gain=5)
            st.success("Nice! +5 XP")

    with tab2:
        d = st.number_input("Enter a decimal (0 to 1)", 0.0, 1.0, 0.6, 0.01, key="dec_to_pct")
        st.write(f"Percent = {decimal_to_percent(d):.2f}%")
        if st.button("Check understanding (Decimal → Percent)"):
            record_result("Conversion", "Decimal→Percent", d, True, "Converted.", xp_gain=5)
            st.success("Great! +5 XP")

    with tab3:
        num = st.number_input("Numerator", 0, 100, 1, 1)
        den = st.number_input("Denominator", 1, 100, 4, 1)
        pct = fraction_to_percent(num, den)
        st.write(f"Percent = {pct:.2f}%")
        if st.button("Check understanding (Fraction → Percent)"):
            record_result("Conversion", "Fraction→Percent", f"{num}/{den}", True, "Converted.", xp_gain=5)
            st.success("Well done! +5 XP")

# -------------------------------
# Percent of a Number
# -------------------------------
elif page == "✖️ Percent of a Number":
    st.header("✖️ Finding the Percent of a Number")
    st.latex(r"\text{Part} = \frac{\text{Percent}}{100}\times \text{Whole}")

    c1, c2 = st.columns(2)
    with c1:
        percent_input = st.number_input("Percent (%)", min_value=0.0, max_value=100.0, value=25.0, step=0.5)
    with c2:
        whole_input = st.number_input("Whole", min_value=0.0, value=120.0, step=1.0)

    part = (percent_input/100.0) * whole_input if whole_input != 0 else 0.0
    st.markdown(f"""
    <div class="concept-box">
        <p>{percent_input}% of {whole_input} = <b>{part:.2f}</b></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Adaptive Practice")
    if "poa_level" not in st.session_state:
        st.session_state.poa_level = 1

    if st.button("New Practice Problem"):
        p = random.choice([5,10,15,20,25,30,40,50,60,75,80,90])
        w = random.randint(20*st.session_state.poa_level, 80*st.session_state.poa_level)
        st.session_state.poa_problem = (p, w)
        st.session_state.poa_answer = (p/100)*w

    if "poa_problem" in st.session_state:
        p, w = st.session_state.poa_problem
        user = st.text_input(f"What is {p}% of {w}?", key="poa_user")
        if st.button("Check Answer"):
            correct = check_numeric_answer(user, st.session_state.poa_answer, tol=1e-2)
            fb = f"Correct: {p}% of {w} is {st.session_state.poa_answer:.2f}."
            if correct:
                st.success(fb + " +10 XP")
                st.session_state.poa_level = min(st.session
