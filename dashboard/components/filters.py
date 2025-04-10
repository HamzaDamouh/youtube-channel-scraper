import streamlit as st
import pandas as pd
from datetime import datetime

def apply_filters(df):
    """
    Apply dynamic filters to the DataFrame.
    
    Parameters:
    - df: DataFrame with video data, expected to include 'title' and 'published_date' columns.
    
    Returns:
    - Filtered DataFrame.
    """
    if df.empty:
        st.write("No data available for filtering.")
        return df

    # -- Filter: Search by Title --
    search_term = st.text_input("Search by Title")
    if search_term:
        df = df[df['title'].str.contains(search_term, case=False, na=False)]
    
    

    # Get the min and max dates from the data for the filter range
    if df['published_date'].notnull().any():
        min_date = df['published_date'].min()
        max_date = df['published_date'].max()
    else:
        min_date = datetime.today()
        max_date = datetime.today()

    date_range = st.date_input("Select Publication Date Range", [min_date, max_date])
    
    # Ensure date_range has two dates (start and end)
    if isinstance(date_range, list) and len(date_range) == 2:
        start_date, end_date = date_range
        df = df[(df['published_date'] >= pd.Timestamp(start_date)) & (df['published_date'] <= pd.Timestamp(end_date))]
    
    return df
