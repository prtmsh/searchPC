import os
import requests
import streamlit as st
from typing import List, Dict
from utils import get_gemini_recommendation

class PCPartsFinder:
    def __init__(self):
        """
        Initialize PCPartsFinder with Serper.dev API key.
        """
        self.serper_api_key = os.getenv('SERPER_API_KEY')
        if not self.serper_api_key:
            raise ValueError("Serper API key not found. Please set SERPER_API_KEY in .env")

    def search_pc_parts(self, query: str, location: str) -> List[Dict]:
        """
        Search for PC parts using Serper.dev API.
        
        Args:
            query (str): Search query for PC parts
            location (str): Location for localized search results
        
        Returns:
            List[Dict]: List of PC part search results
        """
        url = "https://google.serper.dev/shopping"
        
        payload = {
            "q": query,
            "gl": "in",  # Default to India
            "hl": "en"
        }
        
        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            shopping_results = data.get('shopping', [])
            
            # Process and filter results
            processed_results = []
            for item in shopping_results[:10]:  # Limit to 10 results
                processed_item = {
                    'title': item.get('title', 'No Title'),
                    'price': item.get('price', 'Price Not Available'),
                    'source': item.get('source', 'Unknown'),
                    'link': item.get('link', '#')
                }
                processed_results.append(processed_item)
            
            return processed_results
        
        except requests.RequestException as e:
            st.error(f"Error searching parts: {e}")
            return []

    def get_part_recommendations(self, purpose: str, budget: float, location: str) -> Dict:
        """
        Generate comprehensive PC part recommendations.
        
        Args:
            purpose (str): Intended PC use
            budget (float): Total budget
            location (str): User's location
        
        Returns:
            Dict: Comprehensive part recommendations
        """
        # Initial recommendation from Gemini
        ai_recommendation = get_gemini_recommendation(purpose, budget)
        
        # Break down recommendation into specific part searches
        part_categories = {
            'CPU': f"{purpose} high-performance CPU",
            'GPU': f"{purpose} graphics card",
            'Motherboard': "Compatible motherboard",
            'RAM': f"{purpose} RAM",
            'Storage': f"{purpose} SSD"
        }
        
        recommendations = {}
        
        for category, search_query in part_categories.items():
            results = self.search_pc_parts(search_query, location)
            recommendations[category] = results
        
        return {
            'ai_recommendation': ai_recommendation,
            'part_recommendations': recommendations
        }