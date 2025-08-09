nice program!  now add section where the student talks to an llm which prompts them to design their own percents problem.  the llm reasons with them until they have a solid understanding of percents and percent change and converting percents to decimals and percents as fractions.  extract the llm configurations from here # =====================================================================================
# MathCraft: The Equation of You — A Growth Mindset Program for CognitiveCloud.ai
# Developed by Xavier Honablue M.Ed
# =====================================================================================
import streamlit as st
import io
import time
import json
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title="MathCraft: The Equation of You",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for consistent styling (Inter font, CognitiveCloud.ai colors) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    body {
        font-family: 'Inter', sans-serif;
        background-color: #F8F7F4; /* Light neutral background */
        color: #333333; /* Dark text for readability */
    }
    .main-header {
        text-align: center;
        color: #6A0572; /* CognitiveCloud.ai primary header color */
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #4B0082; /* CognitiveCloud.ai secondary header color */
        font-size: 1.8rem;
        margin-bottom: 2rem;
    }
    .section-header {
        color: #005A9C; /* CognitiveCloud.ai accent blue */
        font-size: 2.2rem;
        font-weight: bold;
        margin-top: 2.5rem;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #E0E0E0;
        padding-bottom: 0.5rem;
    }
    .card {
        background-color: #FFFFFF;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border: 1px solid #E0E0E0;
    }
    .highlight-box {
        background-color: #E8F5E9; /* Light green for positive reinforcement */
        border-left: 5px solid #4CAF50; /* Green accent */
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .stButton > button {
        background-color: #005A9C; /* Accent blue button */
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: bold;
        transition: background-color 0.3s ease;
        cursor: pointer;
        border: none;
        margin-top: 10px;
    }
    .stButton > button:hover {
        background-color: #004070; /* Darker blue on hover */
    }
</style>
""", unsafe_allow_html=True)

# --- Header & Branding ---
col1, col2 = st.columns([1, 4])
with col1:
    try:
        st.image("https://placehold.co/80x80/6A0572/FFFFFF?text=CC", width=80)
    except:
        st.markdown("🌱")
with col2:
    st.markdown("### www.cognitivecloud.ai")
    st.markdown("**Developed by Xavier Honablue M.Ed**")

st.markdown("---")

st.markdown('<h1 class="main-header">🌱 MathCraft: The Equation of You</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your Present Actions = Your Future Self</p>', unsafe_allow_html=True)

# --- Dr. X LLM Integration ---
def ask_drx(message):
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

# --- Introduction & Core Concept ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">The Core Idea: Your Identity as an Equation</h2>', unsafe_allow_html=True)
st.markdown("""
<p style='font-size: 1.1rem; line-height: 1.6;'>
    Welcome! This MathCraft program helps you build a positive mindset using math concepts you already know.
    Your identity isn't a fixed number; it's a dynamic equation you are constantly solving.
    The most important part? The **equal sign (=)**.
</p>
<div class="highlight-box">
    <p style='font-weight: bold; color: #388E3C;'>
        **The Equal Sign is a Photograph:** It shows that your **Present Self** is an exact match for your **Future Self**, based on the actions you take today. By changing your variables on one side of the equation, you create a new, desired outcome on the other.
    </p>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# =====================================================================================
# Module 1: The Variables of Your Identity
# =====================================================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">1) The Variables of Your Identity 🧠</h2>', unsafe_allow_html=True)
st.markdown("""
<p style='font-size: 1.1rem;'>
    In math, variables like 'x' and 'y' can change. In life, your effort, practice, and perseverance are your variables. You control them, and they determine the outcome of your equation.
</p>
<ul style='list-style-type: none; padding-left: 0;'>
    <li class="highlight-box" style="background-color: #E3F2FD; border-left: 5px solid #2196F3;">
        <span style="font-weight: bold; color: #1565C0;">Your Equation:</span>
        <span style="color: #4CAF50;">(Your Effort) + (Your Practice) = Your Future Self</span>
    </li>
</ul>
""", unsafe_allow_html=True)

st.subheader("Explore Your Variables with Dr. X")
current_variable = st.text_input("What's one variable you want to work on? (e.g., 'Asking for help', 'Perseverance', 'Time management')", key="variable_input")
if st.button("Ask Dr. X about this variable", key="variable_btn"):
    if current_variable:
        drx_prompt = f"As a positive mindset coach for students, explain the importance of the variable '{current_variable}' in a simple, encouraging way. Use a math analogy if possible."
        with st.spinner("Dr. X is thinking..."):
            feedback = ask_drx(drx_prompt)
            st.markdown(f"<div class='highlight-box'><p style='font-weight: bold; color: #388E3C;'>Dr. X's Insight:</p><p style='color: #4CAF50;'>{feedback}</p></div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a variable to explore.")

st.markdown('</div>', unsafe_allow_html=True)

# =====================================================================================
# Module 2: The Power of Transformation
# =====================================================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">2) The Power of Transformation 🚀</h2>', unsafe_allow_html=True)
st.markdown("""
<p style='font-size: 1.1rem;'>
    Think of yourself as a point on a graph. Mistakes, effort, and learning are like transformations that move you toward your goals. Your goal isn't to be a static point; it's to transform into a better version of yourself.
</p>
""", unsafe_allow_html=True)

transform_choice = st.selectbox(
    "Choose a transformation to explore:",
    ["Reflection (from mistakes)", "Translation (steady progress)", "Scaling (growth over time)"],
    key="transformation_choice"
)

if st.button("Explore this transformation with Dr. X", key="transform_btn"):
    drx_prompt = f"Explain the concept of '{transform_choice}' using a math analogy for a student. Connect this to their personal growth and positive mindset."
    with st.spinner("Dr. X is thinking..."):
        feedback = ask_drx(drx_prompt)
        st.markdown(f"<div class='highlight-box'><p style='font-weight: bold; color: #388E3C;'>Dr. X's Explanation:</p><p style='color: #4CAF50;'>{feedback}</p></div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# =====================================================================================
# Module 3: Solving the Equation of You (Growth Journal)
# =====================================================================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h2 class="section-header">3) Solving Your Equation ✍️</h2>', unsafe_allow_html=True)
st.markdown("""
<p style='font-size: 1.1rem;'>
    Now, let's solve your own equation! Just as you use operations like addition and subtraction to solve for a variable, you can use positive actions to solve for your future self. Use this journal to reflect and get personalized coaching from Dr. X.
</p>
""", unsafe_allow_html=True)

# --- Journaling Section (Embedded & Modified) ---
st.subheader("Your Growth Journal")

# Challenge Entry (The 'problem' you need to solve)
challenge_text = st.text_area("Describe a challenge you're facing (your 'problem'):", height=100, key="journal_challenge_text_new")
if st.button("Get Feedback on Challenge", key="feedback_challenge_btn_new"):
    if challenge_text:
        journal_prompt = f"As a growth mindset coach for a middle/high school student, provide encouraging and constructive feedback on this challenge: {challenge_text}. Use the analogy of a math problem you need to solve. Emphasize perseverance and that every step is progress."
        with st.spinner("Dr. X is thinking..."):
            feedback = ask_drx(journal_prompt)
            st.markdown(f"<div class='highlight-box'><p style='font-weight: bold; color: #388E3C;'>Dr. X's Feedback:</p><p style='color: #4CAF50;'>{feedback}</p></div>", unsafe_allow_html=True)
    else:
        st.warning("Please describe your challenge before getting feedback.")

# Effort Entry (The 'operations' you're using to solve the problem)
effort_taken = st.text_area("What effort have you made so far? (your 'operations'):", height=100, key="journal_effort_taken_new")
if st.button("Get Feedback on Effort", key="feedback_effort_btn_new"):
    if effort_taken:
        journal_prompt = f"As a growth mindset coach, acknowledge and praise the effort described: {effort_taken}. Reinforce that effort is the 'variable' that changes the outcome and encourage continued dedication."
        with st.spinner("Dr. X is thinking..."):
            feedback = ask_drx(journal_prompt)
            st.markdown(f"<div class='highlight-box'><p style='font-weight: bold; color: #388E3C;'>Dr. X's Feedback:</p><p style='color: #4CAF50;'>{feedback}</p></div>", unsafe_allow_html=True)
    else:
        st.warning("Please describe your effort before getting feedback.")

# Mistake Entry (A 'wrong' operation that led to a lesson)
mistake_text = st.text_area("Describe a mistake you’ve made ('wrong' operation):", height=100, key="journal_mistake_text_new")
if st.button("Get Feedback on Mistake", key="feedback_mistake_btn_new"):
    if mistake_text:
        journal_prompt = f"As a growth mindset coach, help reframe this mistake: {mistake_text}. Use a math analogy to explain that mistakes are valuable for 'debugging' the equation and finding the correct path. Emphasize that mistakes are valuable for growth and learning."
        with st.spinner("Dr. X is thinking..."):
            feedback = ask_drx(journal_prompt)
            st.markdown(f"<div class='highlight-box'><p style='font-weight: bold; color: #388E3C;'>Dr. X's Feedback:</p><p style='color: #4CAF50;'>{feedback}</p></div>", unsafe_allow_html=True)
    else:
        st.warning("Please describe your mistake before getting feedback.")

# Lesson Learned Entry (The 'correct' operation for next time)
lesson_learned = st.text_area("What did you learn from that mistake? (the 'correct' operation for next time):", height=100, key="journal_lesson_learned_new")
if st.button("Get Feedback on Lesson Learned", key="feedback_lesson_btn_new"):
    if lesson_learned:
        journal_prompt = f"As a growth mindset coach, validate the learning from this mistake: {lesson_learned}. Encourage the student to apply this 'new operation' to their equation in the future."
        with st.spinner("Dr. X is thinking..."):
            feedback = ask_drx(journal_prompt)
            st.markdown(f"<div class='highlight-box'><p style='font-weight: bold; color: #388E3C;'>Dr. X's Feedback:</p><p style='color: #4CAF50;'>{feedback}</p></div>", unsafe_allow_html=True)
    else:
        st.warning("Please describe your lesson learned before getting feedback.")

# Growth Action Entry (The plan to solve the next equation)
growth_action = st.text_input("One action you’ll take to grow this week (your next 'operation'):", "e.g., Ask for help on a tough math problem", key="journal_growth_action_new")
if st.button("Get Feedback on Growth Action", key="feedback_growth_action_btn_new"):
    if growth_action:
        journal_prompt = f"As a growth mindset coach, provide encouraging feedback on this planned growth action: {growth_action}. Emphasize the importance of taking concrete steps to solve your personal 'equation'."
        with st.spinner("Dr. X is thinking..."):
            feedback = ask_drx(journal_prompt)
            st.markdown(f"<div class='highlight-box'><p style='font-weight: bold; color: #388E3C;'>Dr. X's Feedback:</p><p style='color: #4CAF50;'>{feedback}</p></div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter a growth action before getting feedback.")

# --- Download Button ---
if st.button("📅 Download My Journal as Text File", key="download_journal_btn"):
    buffer = io.StringIO()
    buffer.write("Growth Mindset Reflection Journal: The Equation of You\n\n")
    buffer.write(f"Challenge (Your Problem): {challenge_text}\n")
    buffer.write(f"Effort (Your Operations): {effort_taken}\n\n")
    buffer.write(f"Mistake ('Wrong' Operation): {mistake_text}\n")
    buffer.write(f"Lesson Learned ('Correct' Operation): {lesson_learned}\n\n")
    buffer.write(f"Growth Action (Next Operation): {growth_action}\n")
    st.download_button(
        label="Click to download",
        data=buffer.getvalue(),
        file_name="growth_journal.txt",
        mime="text/plain",
        key="download_button_final"
    )
st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; margin-top: 2rem; color: #666;'>
    <p>💡 <strong>Empowering Young Minds in STEAM</strong></p>
    <p>Developed by Xavier Honablue M.Ed for CognitiveCloud.ai Education</p>
</div>
""", unsafe_allow_html=True)
