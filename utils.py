import os
import requests
from typing import List, Dict
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

# Load environment variables
load_dotenv()

def validate_inputs(budget: float, purpose: str, location: str) -> bool:
    """
    Validate user inputs for PC parts search.
    
    Args:
        budget (float): User's budget
        purpose (str): Intended use of PC
        location (str): User's location
    
    Returns:
        bool: Whether inputs are valid
    """
    if not budget or budget <= 0:
        st.error("Please enter a valid budget.")
        return False
    
    if not purpose or len(purpose.strip()) < 2:
        st.error("Please specify the PC's purpose.")
        return False
    
    if not location or len(location.strip()) < 2:
        st.error("Please specify your location.")
        return False
    
    return True

def get_openai_recommendation(purpose: str, budget: float) -> str:
    """
    Use OpenAI to generate initial PC parts recommendation.
    
    Args:
        purpose (str): Intended use of PC
        budget (float): User's budget
    
    Returns:
        str: Recommendation string
    """
    try:
        # Initialize OpenAI client with just the API key
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a PC parts expert who helps users find the best components."},
                {"role": "user", "content": f"Recommend PC parts for {purpose} with a budget of {budget} INR. Provide specific component recommendations. Focus on key components like CPU, GPU, RAM, and storage. Give a detailed breakdown of recommended parts and their approximate costs."}
            ],
            max_tokens=300
        )
        
        # Access the content differently in the new API
        return response.choices[0].message.content or "No recommendation generated."
    except Exception as e:
        st.error(f"OpenAI API error: {e}")
        return "Unable to generate recommendations at this time."

def log_search(purpose: str, budget: float, location: str):
    """
    Log user search details (optional implementation for analytics).
    
    Args:
        purpose (str): Intended use of PC
        budget (float): User's budget
        location (str): User's location
    """
    try:
        log_df = pd.DataFrame({
            'Timestamp': [pd.Timestamp.now()],
            'Purpose': [purpose],
            'Budget': [budget],
            'Location': [location]
        })
        
        # Append to a CSV file (create if not exists)
        log_file = 'search_logs.csv'
        if os.path.exists(log_file):
            log_df.to_csv(log_file, mode='a', header=False, index=False)
        else:
            log_df.to_csv(log_file, index=False)
    except Exception as e:
        st.warning(f"Could not log search: {e}")