import streamlit as st
from openai import OpenAI
import os

# Initialize the client for Hugging Face Inference API
client = OpenAI(
    base_url="https://api-inference.huggingface.co/v1",
    api_key=os.environ.get('HF_ACCESS_TOKEN')
)

# Set page title
st.set_page_config(page_title=" 💡Gordon AI™ .. An AI twin of Gordon")

# Initialize session state for message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Concise system prompt
system_prompt = "You are an expert fitness, personal training and exercises."

# Sidebar content
st.sidebar.title("🧠 Gordon AI™")
st.sidebar.write("🚀I am avaialble when Gordon is not around. Evaluation version only. Use caution.")
#st.sidebar.write(system_prompt)
st.sidebar.write("---")
st.sidebar.write("**⚠ Disclaimer:**")
st.sidebar.write("""
This chatbot is powered by AI and is designed to assist when 💪 Gordon is not available. You should always check with Gordon for real ⚡advice. I can take your requests and try answer to best of my abilities. I can also book an appointment for you on Gordon's calendar.  
Please note that Gordon AI™ is not a real trainer. For actual advice, please consult with 🧲 Gordon.
""")
st.sidebar.write("---")

# Clear chat history button
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.clear()
    st.experimental_rerun()


# Function to generate response
def generate_response(prompt, history):
    # Combine history and prompt
    context = system_prompt + "\n" + "\n".join([f"{msg['role']}: {msg['content']}" for msg in history]) + f"\nUser: {prompt}\nAssistant:"
    
    response = client.chat.completions.create(
        model="HuggingFaceH4/zephyr-7b-beta",  # Use the specified model
        messages=[{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": prompt}],
        max_tokens=2000,  # Increased token limit
        n=1,
        stop=None,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()

# Main app
st.title("Gordon AI™ ")

# Create two columns for input and response
input_col, response_col = st.columns(2)

with input_col:
    st.subheader("💡 Enter Your Question")
    user_input = st.text_input("📝 Type here and press Enter ➡️", key="user_input")

# User input
#user_input = st.text_input("Enter your question :")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "User", "content": user_input})
    
    try:
        # Generate response with more context
        response = generate_response(user_input, st.session_state.messages[-10:])  # Last 10 messages as context
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "Assistant", "content": response})
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        print(f"Error details: {e}")  # For debugging

# Display last two messages with the most recent on top
#if len(st.session_state.messages) > 0:
#    for message in reversed(st.session_state.messages[-4:]):  # Display last 4 messages
#        if message["role"] == "User":
#            st.write("You:", message["content"])
#        else:
#            st.write("Assistant:", message["content"])

with response_col:
    st.subheader("🤖 Gordon AI™ Responses")
    # Display last two messages with the most recent on top
    if len(st.session_state.messages) > 0:
        for message in reversed(st.session_state.messages[-4:]):  # Display last 4 messages
            if message["role"] == "User":
                st.write("📝 You:", message["content"])
            else:
                st.write("🔥 Gordon AI™:", message["content"])

