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
    Use OpenAI to generate precise PC parts recommendation based on budget.
    
    Args:
        purpose (str): Intended use of PC
        budget (float): User's budget in INR
    
    Returns:
        str: Detailed recommendation string
    """
    try:
        # Initialize OpenAI client with just the API key
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Extremely detailed and precise prompt
        detailed_prompt = f"""
You are a professional PC parts consultant specializing in budget-optimized system builds for the Indian market. 

STRICT REQUIREMENTS:
- Total system budget: {budget} INR
- Purpose: {purpose}
- MANDATORY: Utilize the FULL budget effectively
- Provide EXACT part recommendations that match the budget
- Include CURRENT market prices in INR
- Breakdown MUST include:
  1. Processor (CPU)
  2. Motherboard
  3. Graphics Card (GPU)
  4. RAM
  5. Storage (SSD + HDD if budget allows)
  6. Power Supply
  7. Cabinet

CRITICAL INSTRUCTIONS:
- Recommend parts that MAXIMIZE performance for the given budget
- Do NOT underspend
- Prefer Indian market availability
- Balance between performance and cost
- Consider future upgradability

BUDGET ALLOCATION GUIDE:
- CPU: 15-25% of total budget
- Motherboard: 10-15% of total budget
- GPU: 25-35% of total budget
- RAM: 10% of total budget
- Storage: 10-15% of total budget
- PSU & Cabinet: Remaining budget

Example Format:
"Budget: 200,000 INR
1. CPU: [Exact Model] - Price: X INR
2. Motherboard: [Exact Model] - Price: Y INR
... (continue for all components)

Total Spend: {budget} INR"

RESPOND WITH A PRECISE, COMPREHENSIVE RECOMMENDATION THAT FULLY UTILIZES THE BUDGET!
"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert PC parts consultant specialized in budget-optimized builds."},
                {"role": "user", "content": detailed_prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        # Access the content 
        recommendation = response.choices[0].message.content or "No recommendation generated."
        
        return recommendation
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