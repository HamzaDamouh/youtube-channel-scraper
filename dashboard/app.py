import streamlit as st
import pandas as pd
from queries import load_all_data
from components.filters import apply_filters
from components.visualizations import (
    videos_per_month_chart,
    avg_duration_chart,
    wordcloud_chart
)

st.set_page_config(page_title='YouTube Analytics', layout='wide')

st.title('YouTube Channel Analytics')

data = load_all_data()

# Channel selector
channel = st.sidebar.selectbox('Channel', data['channel_name'].unique())
df = data[data['channel_name']==channel]

st.sidebar.write(f"Total Videos: {len(df)}")
st.sidebar.write(f"Date Range: {df['published_date'].min()} to {df['published_date'].max()}")

filtered = apply_filters(df)

# Main layout
col1, col2 = st.columns(2)
with col1:
    videos_per_month_chart(filtered)
    avg_duration_chart(filtered)
with col2:
    st.dataframe(filtered)
    wordcloud_chart(filtered)

st.markdown('**Download Data:**')
csv = filtered.to_csv(index=False)
st.download_button('Download CSV', data=csv, file_name=f'{channel}_videos.csv')