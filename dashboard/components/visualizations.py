import streamlit as st
import pandas as pd
import altair as alt

def videos_per_month_chart(df):
    """
    Create a bar chart showing the number of videos published per month.
    
    Parameters:
    - df: DataFrame with a 'published_date' column.
    """
    if df.empty:
        st.write("No data available for visualization.")
        return

    # Convert published_date to datetime if not already (let pandas infer the format)
    try:
        df['published_date'] = pd.to_datetime(df['published_date'], errors='coerce')
    except Exception as e:
        st.error("Error converting published_date to datetime: " + str(e))
        return

    # Verify that the conversion resulted in a datetimelike dtype
    if not pd.api.types.is_datetime64_any_dtype(df['published_date']):
        st.error("The 'published_date' column is not in a datetime format.")
        return

    # Create a new column 'year_month' in the format YYYY-MM
    df['year_month'] = df['published_date'].dt.to_period('M').astype(str)

    # Group by year_month and count the number of videos
    chart_data = df.groupby('year_month').size().reset_index(name='count')

    # Build a bar chart using Altair
    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('year_month:N', title="Year-Month"),
        y=alt.Y('count:Q', title="Number of Videos"),
        tooltip=["year_month", "count"]
    ).properties(
        title="Videos Published per Month"
    )

    st.altair_chart(chart, use_container_width=True)
