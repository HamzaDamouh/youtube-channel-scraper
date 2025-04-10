import streamlit as st
import pandas as pd
from queries import fetch_all_videos

def main():
    
    st.title("YouTube Channel Analyzer Dashboard")
    st.markdown("This dashboard displays video data scraped from a YouTube channel, stored in PostgreSQL.")
    
    data = fetch_all_videos()
    
 
    st.subheader("Overview")
    st.write("Total videos:", len(data))
    
    
    st.subheader("Video Data Table")
    st.dataframe(data)
    
    

if __name__ == "__main__":
    main()