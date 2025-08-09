import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime

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
    # Badges
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
    # Badge based on streak handled in award_xp; here we can still check:
    if st.session_state.streak >= 5:
        st.session_state.badges.add("Streak Master")

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
    st.markdown("**Badges:** " + " ".join([f"<span class='badge'>{b}</sp]()
