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
You are a world-class PC parts consultant with 20+ years of experience, specializing in high-performance, budget-optimized builds for the Indian market. Your task is to provide a comprehensive recommendation for a complete PC build that uses exactly the full budget provided, with no underspending or overspending.

Total Budget: {budget} INR
Intended Use: {purpose}

Requirements:
- You must use exactly {budget} INR. Ensure that the sum of all component prices equals exactly {budget} INR. If necessary, adjust prices slightly to reach the exact total.
- Provide detailed, specific recommendations for the following components:
    1. Processor (CPU)
    2. Motherboard
    3. Graphics Card (GPU)
    4. RAM
    5. Storage (include at least one SSD; add an HDD if the budget permits)
    6. Power Supply
    7. Cabinet
- For each component, include:
    - The exact model name (ensuring availability in the Indian market)
    - The current price in INR
    - A brief rationale for the choice and its role in the overall build

Additional Guidelines:
- Ensure your recommendations reflect the most current market pricing and availability.
- Optimize for performance, value, and future upgradability.
- If minor rounding adjustments are needed to achieve the exact total, mention them briefly.

Output Format:
Your response should strictly follow this format (with actual values replacing placeholders):

"Budget: {budget} INR
1. CPU: [Exact Model] - Price: X INR
2. Motherboard: [Exact Model] - Price: Y INR
3. GPU: [Exact Model] - Price: Z INR
4. RAM: [Exact Model] - Price: A INR
5. Storage: [Exact Model(s)] - Price: B INR
6. Power Supply: [Exact Model] - Price: C INR
7. Cabinet: [Exact Model] - Price: D INR

Total Spend: {budget} INR"

Respond with a precise, comprehensive recommendation that fully utilizes the entire budget without any underspending.
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