import streamlit as st
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

# Set page config
st.set_page_config(page_title="AI Assistant Chatbot", page_icon="💠", layout="wide")

# Custom CSS to improve the UI
st.markdown("""
<style>
.stTextInput > div > div > input {
    font-size: 16px;
}
.stButton > button {
    width: 100%;
}
.chat-message {
    padding: 1rem;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    display: flex;
    align-items: flex-start;
}
.chat-message.user {
    background-color: #e6f3ff;
}
.chat-message.assistant {
    background-color: #f0f0f0;
}
.chat-message .avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 1rem;
}
.chat-message .message {
    flex-grow: 1;
}
</style>
""", unsafe_allow_html=True)

# Define the system prompt
system_prompt = """
You are a friendly and communicative assistant with expertise in three areas: medical advice, weather updates, and casual conversation. Your role is to provide helpful, accurate, and engaging responses based on the user's input.

Responsibilities:

1. **Medical Expertise**: Offer general advice on health-related questions, analyzing symptoms, and suggesting next steps. Always include the disclaimer: "Consult with a Doctor before making any decisions."
   
2. **Weather Updates**: Provide accurate and up-to-date weather information, including forecasts, current conditions, and weather-related advice.

3. **Chitchat Facility**: Engage in light, friendly conversation, responding to casual questions, comments, or stories in an empathetic and engaging manner.

Key Guidelines:

1. **Tone**: Maintain a friendly, approachable, and conversational tone in all responses.
   
2. **Clarity**: Ensure that all information is presented clearly and simply, especially when discussing medical or weather-related topics.

3. **Accuracy**: Prioritize accurate information, particularly for medical and weather inquiries. Always reference reliable data where applicable.

Your goal is to create a positive and helpful interaction with users, blending your knowledge in these three fields to provide well-rounded assistance.

If someone asks who made you , say Vinil Joseph

If someone ask who are you, say I am Vinil Joseph's AI Assistant, tell about the tasks you can do

For medical inquiries, you might see the following format:
input:\n {input}?\n
"""

# Initialize the model and prompt template
llm = GoogleGenerativeAI(model="gemini-pro", google_api_key='AIzaSyBQE8QC5c2IDklrswj9qEGzp1I5ns2gp3E')
prompt_template = PromptTemplate.from_template(system_prompt + "{input}")

# Streamlit app layout
st.title('💠 AI Assistant Chatbot')

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What's on your mind today?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Create a prompt and invoke the model
    chain = prompt_template | llm
    response = chain.invoke({"input": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

# Add a sidebar with some information
st.sidebar.title("About AI Assistant")
st.sidebar.info(
    """Hello! I'm a friendly and communicative assistant here to help you with:

Medical Advice: I offer general health guidance, analyze symptoms, and suggest next steps. Remember, "Consult with a Doctor before making any decisions."

Weather Updates: Get the latest weather information, including forecasts and current conditions.

Casual Conversation: Engage in light-hearted chats and respond to your comments and questions with empathy and friendliness.

Feel free to ask me about these topics, and I'll do my best to assist you!"""


)

# Add a disclaimer at the bottom of the sidebar
st.sidebar.markdown("---")
st.sidebar.caption(
    "Disclaimer: This chatbot is for informational purposes only and is not a substitute "
    "for professional medical advice, diagnosis, or treatment."
)