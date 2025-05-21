import streamlit as st
import openai

openai.api_key = st.secrets["openai"]["api_key"]
