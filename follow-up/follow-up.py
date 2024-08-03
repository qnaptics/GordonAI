import streamlit as st
from openai import OpenAI
import os
import datetime

# Initialize the client for Hugging Face Inference API
client = OpenAI(
    base_url="https://api-inference.huggingface.co/v1",
    api_key=os.environ.get('HF_ACCESS_TOKEN')
)

# Set page title and layout
st.set_page_config(page_title="💡Gordon AI™ - Fitness Assistant", layout="wide")

# Initialize session state for message history and recent training sessions
if "messages" not in st.session_state:
    st.session_state.messages = []

# Recent training sessions
recent_sessions = {
    "": "",  # Blank user as default
    "Tina": "Strength Training",
    "Maya": "Cardio",
    "Jason": "CrossFit",
    "Ella": "Cycling",
    "Tim": "Boxing",
    "Dorothy": "Zumba"
}

# Sidebar content
st.sidebar.title("🧠 Gordon AI™ Settings")
st.sidebar.write("Customize your AI fitness assistant experience")

# User selection in sidebar
selected_user = st.sidebar.selectbox("Select a user:", list(recent_sessions.keys()))

# LLM Settings
st.sidebar.subheader("LLM Settings")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7, 0.1)
max_tokens = st.sidebar.slider("Max Tokens", 100, 2000, 1000, 50)

# System prompt (not shown in sidebar)
system_prompt = "You are an expert fitness, personal training and exercises assistant named Gordon AI. Provide helpful and motivating advice."

# Disclaimer
st.sidebar.markdown("---")
st.sidebar.subheader("⚠ Disclaimer")
st.sidebar.write("""
This chatbot is powered by AI and is designed to assist when 💪 Gordon is not available. 
Always consult with Gordon for real ⚡advice. I can take your requests and try to answer to the best of my abilities. 
I can also help schedule an appointment on Gordon's calendar.
""")

# Clear chat history button
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.experimental_rerun()

# Main content area
st.title("💡Gordon AI™ - Your Fitness Assistant")

# Display chat messages
for message in st.session_state.messages:
    with st.container():
        st.write(f"**{message['role'].title()}:** {message['content']}")

# Function to generate response
def generate_response(prompt, history):
    context = system_prompt + "\n" + "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]) + f"\nUser: {prompt}\nAssistant:"
    
    response = client.chat.completions.create(
        model="HuggingFaceH4/zephyr-7b-beta",
        messages=[{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature,
    )

    return response.choices[0].message.content.strip()

# Function to suggest recovery routine
def suggest_recovery_routine(name, exercise):
    recovery_prompt = f"Suggest a recovery routine for {name} who recently did {exercise}. Include stretching, nutrition, and rest recommendations."
    return generate_response(recovery_prompt, [])

# Chat input
user_input = st.text_input("Ask Gordon AI about fitness, exercises, or recovery...")

if st.button("Send"):
    if user_input:
        # Add user message to chat history
        full_input = f"{selected_user}: {user_input}" if selected_user else user_input
        st.session_state.messages.append({"role": "user", "content": full_input})
        
        # Check if the user is asking about recovery
        if "recover" in user_input.lower() and selected_user:
            exercise = recent_sessions[selected_user]
            if exercise:
                recovery_routine = suggest_recovery_routine(selected_user, exercise)
                ai_response = f"Hello {selected_user}! Here's a recovery routine based on your recent {exercise} session:\n\n{recovery_routine}"
            else:
                ai_response = f"I'm sorry, {selected_user}. I don't have information about your recent training session. Please provide more details about your workout, and I'll suggest a recovery routine."
        else:
            # Generate AI response for other queries
            ai_response = generate_response(full_input, st.session_state.messages)
        
        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
        # Rerun to update the chat display
        st.experimental_rerun()

# Additional features
st.markdown("---")
st.subheader("Quick Actions")

# Workout of the Day
if st.button("🏋️ Get Workout of the Day"):
    workout = generate_response("Suggest a quick workout of the day", st.session_state.messages)
    st.info(workout)

# Schedule Appointment
st.subheader("📅 Schedule an Appointment with Gordon")
appointment_date = st.date_input("Select a date", min_value=datetime.date.today())
appointment_time = st.time_input("Select a time")

if st.button("Book Appointment"):
    appointment_msg = f"Schedule an appointment with Gordon on {appointment_date} at {appointment_time}"
    response = generate_response(appointment_msg, st.session_state.messages)
    st.success(response)

# Footer
st.markdown("---")
st.markdown("Gordon AI™ - Powered by Qnaptics Technology")