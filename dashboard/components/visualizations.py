import streamlit as st
import pandas as pd
import altair as alt
from wordcloud import WordCloud # type: ignore
import matplotlib.pyplot as plt # type: ignore


def videos_per_month_chart(df):
    df['published_date']=pd.to_datetime(df['published_date'])
    df['month']=df['published_date'].dt.to_period('M').astype(str)
    data=df.groupby('month').size().reset_index(name='count')
    chart=alt.Chart(data).mark_bar().encode(x='month',y='count')
    st.altair_chart(chart,use_container_width=True)


def avg_duration_chart(df):
    df['duration']=pd.to_timedelta(df['duration'])
    data=df.resample('M', on='published_date').duration.mean().reset_index()
    data['duration']=data['duration'].dt.total_seconds()/60
    chart=alt.Chart(data).mark_line().encode(x='published_date', y='duration')
    st.altair_chart(chart,use_container_width=True)


def wordcloud_chart(df):
    text=" ".join(df['description'].fillna(''))
    wc=WordCloud(width=400,height=200).generate(text)
    fig, ax=plt.subplots()
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)