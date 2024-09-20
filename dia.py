import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
api_key = os.getenv('GOOGLE_API_KEY')

st.set_page_config(page_title='Disease Analysis')


safety_settings=[
                 {
                     "category": "HARM_CATEGORY_HARASSMENT",
                     "threshold": "BLOCK_ONLY_HIGH"
                 },
                 {
                     "category": "HARM_CATEGORY_HATE_SPEECH",
                     "threshold": "BLOCK_ONLY_HIGH"
                 },
                 {
                     "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                     "threshold": "BLOCK_ONLY_HIGH"
                 },
                 {
                     "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                     "threshold": "BLOCK_ONLY_HIGH"
                 },
             ]

system_prompt="""
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

symptoms:\n {symptoms}?\n
"""





st.title('Disease Diagnose')

txt = st.text_area(
    "Symptoms to analyze",

    )

submit=st.button('Diagnose...')

if submit:

    llm = GoogleGenerativeAI(model="gemini-pro", google_api_key=api_key)

    prompt = PromptTemplate.from_template(system_prompt)

    chain = prompt | llm




    if chain:
        st.title('Analysis: ')
        st.write(chain.invoke({"symptoms": txt}))





