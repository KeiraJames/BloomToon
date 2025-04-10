import streamlit as st


st.title("Chatbot 🤖")
st.write("Welcome to the Chatbot page!")
st.markdown(
    """
    <style>
    .stApp {
    background: linear-gradient(135deg, #e0f7e9 25%, #a5d6a7 25%, #a5d6a7 50%, #e0f7e9 50%, #e0f7e9 75%, #a5d6a7 75%, #a5d6a7 100% );
    background-size: 200% 200%;
    animation: wave 10s ease infinite;
    height: 100vh;
    }
    @keyframes wave{
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }
    </style>
    """,
    unsafe_allow_html=True
)