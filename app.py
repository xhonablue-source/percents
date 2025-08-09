import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime
import requests

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
        "🤖 Design Your Own Percent Problem (Dr. X)",
        "🧠 Quiz: The Percent Power-Up",
        "📚 External Resources",
        "📤 Export Progress"
    ]
)

# -------------------------------
# Helper functions
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

# --- Dr. X LLM Integration (same config you use elsewhere) ---
def ask_drx(message: str) -> str:
    try:
        response = requests.post(
            "https://ask-drx-730124987572.us-central1.run.app",
            json={"message": message},
            timeout=30
        )
        if response.status_code == 200:
            return response.json().get("reply", "Sorry, I couldn't process that.")
        return f"I'm having trouble connecting right now. Server responded with status {response.status_code}. Please try again."
    except requests.exceptions.Timeout:
        return "I'm having trouble connecting right now. The request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return "I'm having trouble connecting right now. There was a network error. Please check your internet connection and try again."
    except Exception as e:
        return f"I'm having trouble connecting right now. An unexpected error occurred: {e}. Please try again."

# -------------------------------
# Home & overview
# -------------------------------
if page == "🏠 Home & Overview":
    st.header("Welcome to MathCraft: The Power of Percents!")
    st.markdown("""
    Percent means “per 100.” In this lab you’ll convert between **fractions**, **decimals**, and **percents**,
    compute **discounts**, **tax**, **tips**, **commission**, and **simple interest**, and build real **receipts**.
    """)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="module-card">
            <h3>What you'll master</h3>
            <ul>
                <li>🧭 Convert between % ↔ decimal ↔ fraction</li>
                <li>🧮 Find the percent of a number</li>
                <li>🏷️ Compute discount, tax, and tip</li>
                <li>💼 Calculate commissions & simple interest</li>
                <li>🧩 Tackle real-world word problems</li>
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
                <li>Collect 🎖️ badges as you go</li>
                <li>Export a 📤 progress report for your teacher</li>
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
        <strong>📚 Relevant Common Core Standards:</strong>
        <ul>
            <li>6.RP.A.3c: Find a percent of a quantity.</li>
            <li>7.RP.A.3: Solve multistep ratio and percent problems.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="activity-box">
        <h4>🎯 The Percent Visualizer</h4>
        <p>Slide to change the percent and see its decimal and fraction forms with visuals (bar, 10×10 grid, and pie chart).</p>
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
    st.markdown("Practice converting between **percent**, **decimal**, and **fraction**. Get instant feedback and XP!")

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
# Percent of a Number (calculator + practice)
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
        st.session_state.poa_level = 1  # increases with correct answers

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
                st.session_state.poa_level = min(st.session_state.poa_level + 1, 5)
                record_result("Percent of Number", f"{p}% of {w}", user, True, fb, xp_gain=10)
            else:
                st.error(f"Close! {fb} Try another.")
                record_result("Percent of Number", f"{p}% of {w}", user, False, fb, xp_gain=0)

# -------------------------------
# Percent Change & Discounts
# -------------------------------
elif page == "📈 Percent Change & Discounts":
    st.header("📈 Percent Change & Discounts")
    st.latex(r"\text{Percent Change}=\frac{\text{New}-\text{Original}}{\text{Original}}\times 100")

    col1, col2 = st.columns(2)
    with col1:
        original_value = st.number_input("Original Value", value=100.0, step=1.0)
    with col2:
        new_value = st.number_input("New Value", value=120.0, step=1.0)

    if original_value != 0:
        percent_change = ((new_value - original_value) / original_value) * 100
        change_type = "increase" if percent_change >= 0 else "decrease"
        st.markdown(f"""
        <div class="concept-box">
            <p>Change: {(new_value-original_value):.2f}; Percent change = {percent_change:.2f}%</p>
            <h3>Result: A {abs(percent_change):.2f}% {change_type}.</h3>
        </div>
        """, unsafe_allow_html=True)
        draw_percent_bar(abs(percent_change))
    else:
        st.warning("Original value cannot be zero.")

    st.markdown("### Discount Simulator")
    price = st.number_input("Item Price ($)", value=60.0, step=0.5)
    discount = st.slider("Discount (%)", 0, 90, 20)
    savings = price * discount/100
    final_price = price - savings
    c1, c2, c3 = st.columns(3)
    with c1: st.metric("Original", f"${price:.2f}")
    with c2: st.metric("You Save", f"${savings:.2f}")
    with c3: st.metric("Final Price", f"${final_price:.2f}")
    if st.button("👍 I computed it! (+5 XP)"):
        award_xp(5, "Discount Simulator", "Percent Change")

# -------------------------------
# Tax & Tip Receipt Builder
# -------------------------------
elif page == "🧾 Tax & Tip Receipt Builder":
    st.header("🧾 Tax & Tip Receipt Builder")
    st.markdown("Build a real receipt with **sales tax** and **tip**. Great for financial literacy!")

    items = st.number_input("Number of line items", 1, 10, 3)
    data = []
    for i in range(items):
        c1, c2, c3 = st.columns([3,1,1])
        with c1:
            name = st.text_input(f"Item {i+1} name", value=f"Item {i+1}")
        with c2:
            qty = st.number_input(f"Qty {i+1}", 1, 20, 1, key=f"qty_{i}")
        with c3:
            price = st.number_input(f"Price {i+1} ($)", 0.0, 1000.0, 9.99, 0.01, key=f"price_{i}")
        data.append({"Item": name, "Qty": qty, "Price": price, "Line Total": qty*price})
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
    subtotal = df["Line Total"].sum()

    col = st.columns(3)
    with col[0]:
        tax_rate = st.number_input("Sales Tax (%)", 0.0, 20.0, 6.625, 0.125)
    with col[1]:
        tip_rate = st.number_input("Tip (%)", 0.0, 30.0, 18.0, 0.5)
    with col[2]:
        extra = st.number_input("Extra Fees ($)", 0.0, 100.0, 0.0, 0.5)

    tax = subtotal * tax_rate/100
    tip = subtotal * tip_rate/100
    total = subtotal + tax + tip + extra

    st.markdown(f"**Subtotal:** ${subtotal:.2f}  •  **Tax:** ${tax:.2f}  •  **Tip:** ${tip:.2f}  •  **Fees:** ${extra:.2f}")
    st.markdown(f"### **Total: ${total:.2f}**")
    draw_pie(min(100, tip_rate))  # Quick visual: tip % of 100

    if st.button("Looks good! (+8 XP)"):
        award_xp(8, "Built a receipt", "Tax & Tip")

# -------------------------------
# Commission & Simple Interest
# -------------------------------
elif page == "💼 Commission & Simple Interest":
    st.header("💼 Commission & Simple Interest")
    st.markdown("""
    <div class="activity-box">
        <h4>Commission</h4>
        <p>Earnings = <b>Base Pay</b> + ( <b>Commission %</b> × <b>Sales</b> )</p>
    </div>
    """, unsafe_allow_html=True)
    base = st.number_input("Base Pay ($)", 0.0, 5000.0, 500.0, 10.0)
    sales = st.number_input("Total Sales ($)", 0.0, 100000.0, 2000.0, 50.0)
    rate = st.slider("Commission Rate (%)", 0, 50, 10)
    earnings = base + (rate/100)*sales
    st.metric("Earnings", f"${earnings:.2f}")

    st.markdown("""
    <div class="activity-box">
        <h4>Simple Interest</h4>
        <p>I = P × r × t (where r is the decimal rate, t is years)</p>
    </div>
    """, unsafe_allow_html=True)
    P = st.number_input("Principal ($)", 0.0, 10000.0, 1000.0, 10.0)
    r = st.number_input("Rate (%)", 0.0, 100.0, 5.0, 0.25) / 100
    t = st.number_input("Time (years)", 0.0, 10.0, 2.0, 0.5)
    I = P*r*t
    A = P + I
    c1, c2 = st.columns(2)
    with c1: st.metric("Interest (I)", f"${I:.2f}")
    with c2: st.metric("Amount (A)", f"${A:.2f}")

    if st.button("I did these calculations (+8 XP)"):
        award_xp(8, "Commission & Interest", "Finance")

# -------------------------------
# Word Problem Generator
# -------------------------------
elif page == "🧩 Word Problem Generator":
    st.header("🧩 Word Problem Generator")
    st.markdown("Get a fresh real-world percent problem. Enter your answer for instant feedback & XP.")

    topics = ["discount", "tax", "tip", "commission", "percent_of"]
    topic = st.selectbox("Choose topic", topics)

    if st.button("Generate problem"):
        if topic == "discount":
            price = random.choice([24.99, 38.50, 59.95, 120.0])
            disc = random.choice([10, 15, 20, 25, 30, 40])
            st.session_state.wp_text = f"A hoodie costs ${price:.2f}. It's on sale for {disc}% off. What is the sale price?"
            st.session_state.wp_answer = price * (1 - disc/100)
        elif topic == "tax":
            price = random.choice([14.99, 49.99, 83.75, 230.00])
            tax = random.choice([5.0, 6.625, 7.0, 8.875])
            st.session_state.wp_text = f"A gadget costs ${price:.2f}. Sales tax is {tax}%. What is the total cost?"
            st.session_state.wp_answer = price * (1 + tax/100)
        elif topic == "tip":
            bill = random.choice([18.75, 42.10, 63.40, 96.00])
            tip = random.choice([15, 18, 20, 22])
            st.session_state.wp_text = f"A restaurant bill is ${bill:.2f}. You tip {tip}%. What total do you pay?"
            st.session_state.wp_answer = bill * (1 + tip/100)
        elif topic == "commission":
            base = random.choice([0, 300, 500])
            sales = random.choice([1200, 2500, 4800, 7500])
            rate = random.choice([5, 8, 10, 12])
            st.session_state.wp_text = f"You earn a base pay of ${base} plus {rate}% of your ${sales} sales. What are your total earnings?"
            st.session_state.wp_answer = base + (rate/100)*sales
        else:
            p = random.choice([5, 10, 12.5, 20, 25, 40, 60, 75, 80])
            w = random.choice([40, 80, 120, 240, 400])
            st.session_state.wp_text = f"What is {p}% of {w}?"
            st.session_state.wp_answer = (p/100)*w

    if "wp_text" in st.session_state:
        st.info(st.session_state.wp_text)
        usr = st.text_input("Your answer ($ or number):", key="wp_user")
        if st.button("Check my answer"):
            correct = check_numeric_answer(usr, st.session_state.wp_answer, tol=0.02*max(1, abs(st.session_state.wp_answer)))
            if correct:
                st.success(f"✅ Correct! Answer ≈ {st.session_state.wp_answer:.2f}. +12 XP")
                record_result("Word Problems", st.session_state.wp_text, usr, True, "Correct.", xp_gain=12)
            else:
                st.error(f"Not quite. A good estimate is {st.session_state.wp_answer:.2f}. Try another!")
                record_result("Word Problems", st.session_state.wp_text, usr, False, "Incorrect.", xp_gain=0)

# -------------------------------
# Dr. X: Design Your Own Percent Problem
# -------------------------------
elif page == "🤖 Design Your Own Percent Problem (Dr. X)":
    st.header("🤖 Design Your Own Percent Problem (with Dr. X)")
    st.markdown("""
    Work with **Dr. X** to **brainstorm** a real scenario, then **formalize** it as a math problem
    and **check** your work. Dr. X will use a friendly, Socratic style to make sure you understand:
    - converting percents ↔ decimals ↔ fractions  
    - finding a percent of a number  
    - percent increase/decrease  
    """)

    if "drx_chat" not in st.session_state:
        st.session_state.drx_chat = []

    st.markdown("### 1) Brainstorm your scenario")
    starter = st.text_area(
        "Describe a real situation you care about (shopping discount, tip at a restaurant, sales commission, school fundraiser, etc.).",
        placeholder="Example: I’m buying sneakers that cost $120 and there’s a 25% off coupon…",
        height=100
    )

    colB1, colB2 = st.columns([1,1])
    with colB1:
        if st.button("🧠 Brainstorm with Dr. X"):
            if starter.strip():
                system_prompt = (
                    "You are Dr. X, a friendly math coach for middle/high school students. "
                    "Use short, supportive messages and ask guiding questions (Socratic). "
                    "Goal: help the student design a clear percent problem and understand:\n"
                    "- Converting percent to decimal and to fraction\n"
                    "- Finding a percent of a number\n"
                    "- Percent increase/decrease\n"
                    "Keep the tone upbeat and concrete with small steps."
                )
                user_prompt = (
                    f"{system_prompt}\n\nStudent scenario:\n{starter}\n\n"
                    "Help them turn this into a solvable percent problem. Ask one guiding question to move them forward."
                )
                reply = ask_drx(user_prompt)
                st.session_state.drx_chat.append(("Dr. X", reply))
            else:
                st.warning("Write a quick scenario first.")

    with colB2:
        user_msg = st.text_input("Reply to Dr. X here and keep the conversation going:", key="drx_reply")
        if st.button("📨 Send to Dr. X"):
            if user_msg.strip():
                st.session_state.drx_chat.append(("You", user_msg))
                followup = ask_drx(
                    "You are Dr. X, continue coaching concisely. Student said:\n"
                    + user_msg +
                    "\nAsk one question or give one next step. Keep it focused on percents (decimal/fraction forms, percent-of, or percent change)."
                )
                st.session_state.drx_chat.append(("Dr. X", followup))
            else:
                st.warning("Type a message to send.")

    if st.session_state.drx_chat:
        st.markdown("---")
        st.markdown("### Conversation")
        for speaker, msg in st.session_state.drx_chat[-12:]:
            if speaker == "Dr. X":
                st.info(f"**{speaker}:** {msg}")
            else:
                st.write(f"**{speaker}:** {msg}")

    st.markdown("---")
    st.markdown("### 2) Formalize your math problem")
    st.caption("Fill any two, and I’ll compute the third. Use this to pin down your numbers.")

    tabA, tabB = st.tabs(["Percent of a Number", "Percent Change"])
    with tabA:
        c1, c2, c3 = st.columns(3)
        with c1:
            pct = st.number_input("Percent (%)", min_value=0.0, max_value=100.0, value=25.0, step=0.5, key="llm_pct")
        with c2:
            whole = st.number_input("Whole", min_value=0.0, value=120.0, step=1.0, key="llm_whole")
        with c3:
            st.caption("Part (auto)")
            part_calc = (pct/100.0) * whole
            st.success(f"Part = {part_calc:.2f}")

        st.markdown(f"- Decimal form: **{pct/100:.3f}**  |  Fraction form: **{int(pct)}/100** (simplify if possible)")

    with tabB:
        c4, c5 = st.columns(2)
        with c4:
            orig = st.number_input("Original value", value=80.0, step=1.0, key="llm_orig")
        with c5:
            newv = st.number_input("New value", value=100.0, step=1.0, key="llm_new")
        if orig != 0:
            pc = ((newv - orig) / orig) * 100
            direction = "increase" if pc >= 0 else "decrease"
            st.success(f"Percent change = {abs(pc):.2f}% {direction}")
            st.markdown(f"- Decimal change factor = **{newv/orig:.3f}**")
        else:
            st.warning("Original must be nonzero.")

    st.markdown("---")
    st.markdown("### 3) Check yourself")
    ans = st.text_input("Write your final problem in one sentence, and give the answer you think is correct.")
    if st.button("✅ Quick feedback"):
        if ans.strip():
            feedback = ask_drx(
                "You are Dr. X. The student wrote this percent problem and answer:\n"
                + ans +
                "\nGive brief, supportive feedback: Is it clear? Are the numbers consistent? "
                "Remind them how to convert the percent to a decimal/fraction if relevant."
            )
            st.info(feedback)
        else:
            st.warning("Write your one-sentence problem and answer first.")

# -------------------------------
# Quiz (auto-graded)
# -------------------------------
elif page == "🧠 Quiz: The Percent Power-Up":
    st.header("🧠 Quiz: The Percent Power-Up")
    st.markdown("Answer all questions. Get instant feedback and a summary score.")

    score = 0
    total = 3

    st.subheader("1) What is 75% as a decimal?")
    q1 = st.radio("Choose one:", ["7.5", "0.75", "750", "0.075"], index=None, key="qq1")
    if q1:
        if q1 == "0.75":
            score += 1
            st.success("Correct! 75 ÷ 100 = 0.75")
            record_result("Quiz", "75% → decimal", q1, True, "Correct.", xp_gain=6)
        else:
            st.error("Incorrect. Divide by 100 to convert percent to decimal.")
            record_result("Quiz", "75% → decimal", q1, False, "Divide by 100.", xp_gain=0)

    st.subheader("2) What is 30% of 200?")
    q2 = st.text_input("Enter a number:", key="qq2")
    if q2:
        if check_numeric_answer(q2, 60, tol=1e-6):
            score += 1
            st.success("Correct! 0.30 × 200 = 60")
            record_result("Quiz", "30% of 200", q2, True, "Correct.", xp_gain=6)
        else:
            st.error("Incorrect. Convert to decimal first (0.30) then multiply by 200.")
            record_result("Quiz", "30% of 200", q2, False, "Convert then multiply.", xp_gain=0)

    st.subheader("3) A $50 shirt is on sale for $40. What is the percent discount?")
    q3 = st.radio("Choose one:", ["10%", "20%", "25%", "40%"], index=None, key="qq3")
    if q3:
        if q3 == "20%":
            score += 1
            st.success("Correct! Change = -$10; (-10/50)×100 = -20% → 20% discount.")
            record_result("Quiz", "Percent discount from 50→40", q3, True, "Correct.", xp_gain=6)
        else:
            st.error("Not quite. Discount% = (Original - Sale)/Original × 100 = (50-40)/50 × 100 = 20%.")
            record_result("Quiz", "Percent discount from 50→40", q3, False, "Compute change/original.", xp_gain=0)

    st.markdown("---")
    st.subheader(f"Score: {score}/{total}")
    if score == total:
        st.success("Perfect! +10 XP Bonus")
        award_xp(10, "Quiz Perfect", "Quiz")

# -------------------------------
# External Resources
# -------------------------------
elif page == "📚 External Resources":
    st.header("📚 External Resources")
    st.subheader("Keep learning!")
    st.markdown("""
    <div class="resources-box">
        <ul>
            <li><a href="https://www.khanacademy.org/math/pre-algebra/pre-algebra-ratios-rates/pre-algebra-percent-problems/v/finding-percentages-example" target="_blank">Khan Academy: Percent problems</a></li>
            <li><a href="https://www.mathisfun.com/percentage.html" target="_blank">Math is Fun: Introduction to Percentages</a></li>
            <li><a href="https://www.ixl.com/math/grade-7/percent-of-a-number" target="_blank">IXL: Practice Problems</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# Export Progress
# -------------------------------
elif page == "📤 Export Progress":
    st.header("📤 Export Progress")
    st.write("Download a CSV of your activity for teacher records or your portfolio.")

    if st.session_state.history:
        hist_df = pd.DataFrame(st.session_state.history)
        st.dataframe(hist_df, use_container_width=True)
        csv = hist_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Progress CSV", data=csv, file_name="percent_progress.csv", mime="text/csv")
    else:
        st.info("No activity yet. Try a module and come back!")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #888;">
    <p><em>"Math is a journey, not a race. Keep crafting!"</em></p>
    <p>Built by Xavier Honablue M.Ed | MathCraft</p>
</div>
""", unsafe_allow_html=True)
