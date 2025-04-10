import streamlit as st
import pandas as pd
from queries import fetch_all_videos

# Import our components using relative imports
from components.filters import apply_filters
from components.visualizations import videos_per_month_chart

def main():
    st.title("YouTube Channel Analyzer Dashboard")
    st.markdown("This dashboard displays video data scraped from a YouTube channel stored in PostgreSQL.")

    
    data = fetch_all_videos()
    
    st.subheader("Overview")
    st.write("Total videos:", len(data))
    
    st.subheader("Filters")
    filtered_data = apply_filters(data.copy())  
   
   
    st.subheader("Filtered Video Data")
    st.dataframe(filtered_data)

    
    st.subheader("Visual Analytics")
    videos_per_month_chart(filtered_data)

if __name__ == "__main__":
    main()
