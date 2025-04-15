import streamlit as st
from parts_finder import PCPartsFinder
from utils import validate_inputs, log_search, parse_gemini_recommendation

def main():
    """
    Main Streamlit application for PC Parts Finder.
    """
    st.set_page_config(
        page_title="PC Parts Finder",
        page_icon="💻",
        layout="wide"
    )
    
    st.title("🖥️ PC Parts Finder")
    st.markdown("Find the perfect PC components tailored to your needs!")
    
    # Sidebar for user inputs
    with st.sidebar:
        st.header("Configure Your PC")
        budget = st.number_input(
            "Budget (INR)", 
            min_value=10000, 
            max_value=1000000, 
            value=50000, 
            step=5000
        )
        
        purpose = st.selectbox(
            "PC Purpose", 
            [
                "Gaming", 
                "Programming", 
                "Machine Learning", 
                "Video Editing", 
                "General Use", 
                "Professional Work"
            ]
        )
        
        location = st.text_input("Location", placeholder="e.g., Mumbai, India")
        
        # Advanced options
        st.subheader("Advanced Options")
        preferred_brands = st.multiselect(
            "Preferred Brands", 
            ["Intel", "AMD", "NVIDIA", "Samsung", "Western Digital"]
        )
        
        search_button = st.button("Find PC Parts")
    
    # Main content area for results
    results_container = st.container()
    
    if search_button:
        if validate_inputs(budget, purpose, location):
            # Log the search
            log_search(purpose, budget, location)
            
            # Initialize parts finder
            try:
                parts_finder = PCPartsFinder()
                
                # Show loading spinner
                with st.spinner("Finding the best PC parts for you..."):
                    recommendations = parts_finder.get_part_recommendations(
                        purpose, budget, location
                    )
                
                # Display results in the results container
                with results_container:
                    st.success("PC Parts Recommendations Found!")
                    
                    # Display AI Recommendation
                    st.subheader("🤖 Complete PC Build Recommendation")
                    st.write(recommendations['ai_recommendation'])
                    
                    # Extract components from the recommendation for better display
                    components = parse_gemini_recommendation(recommendations['ai_recommendation'])
                    
                    # Display Part Recommendations
                    st.subheader("🔍 Where to Buy These Components")
                    
                    for category, parts in recommendations['part_recommendations'].items():
                        if parts:  # Only show categories with results
                            with st.expander(f"{category}: {components.get(category, 'Not specified')}"):
                                for part in parts:
                                    st.markdown(f"""
                                    ### {part['title']}
                                    - **Price**: {part['price']}
                                    - **Source**: {part['source']}
                                    - [View Details]({part['link']})
                                    """)
            
            except Exception as e:
                st.error(f"An error occurred: {e}")
        
    # Footer
    st.markdown("---")
    st.markdown("💡 Tip: Refine your search by adjusting budget or purpose.")

if __name__ == "__main__":
    main()