import streamlit as st
import pandas as pd
from datetime import timedelta

# Convert seconds to hh:mm:ss
def seconds_to_hms(seconds: int) -> str:
    if seconds is None:
        return "00:00:00"
    return str(timedelta(seconds=seconds))

# Sample video data
videos = [
    {"title": "How to Learn Python", "view_count": 12000, "duration": seconds_to_hms(600), "url": "https://youtu.be/abc123"},
    {"title": "Top 10 AI Tools", "view_count": 30000, "duration": seconds_to_hms(400), "url": "https://youtu.be/xyz456"},
    {"title": "Shorts Test", "view_count": 500, "duration": seconds_to_hms(30), "url": "https://youtu.be/short123"},
]

# Create DataFrame
df = pd.DataFrame(videos)

# Streamlit title
st.title("🎥 YouTube Channel Video Explorer")

# Filters
st.subheader("🔍 Filter Videos")

# Search by title
keyword = st.text_input("Search by title:", "")

# Min views filter
min_views = st.slider("Minimum views:", 0, int(df["view_count"].max()), 0)

# Min duration filter (in minutes)
min_duration = st.slider("Minimum duration (minutes):", 0, 5, 0)

# Filter the DataFrame
filtered_df = df[
    df["title"].str.contains(keyword, case=False, na=False) &
    (df["view_count"] >= min_views) &
    (df["duration"].apply(lambda d: int(d.split(":")[0])) >= min_duration)
]

# Show filtered results
st.write(f"✅ Showing {len(filtered_df)} matching videos")
st.dataframe(filtered_df)

# Add bookmark functionality using Streamlit's session state to store favorites
if 'favorites' not in st.session_state:
    st.session_state.favorites = []

# Handle the bookmarking
st.subheader("⭐ Mark Videos as Favorites")

for _, row in filtered_df.iterrows():
    if st.button(f"⭐ Add to Favorites: {row['title']}", key=row['url']):
        st.session_state.favorites.append(row['title'])
        st.success(f"Added '{row['title']}' to favorites!")

# Display the bookmarked videos
if st.session_state.favorites:
    st.subheader("Your Favorites")
    st.write(st.session_state.favorites)

# Add a 'Watch Later' section (simple list storage)
if 'watch_later' not in st.session_state:
    st.session_state.watch_later = []

# Handle 'Watch Later' button
st.subheader("⏳ Add Videos to Watch Later")

for _, row in filtered_df.iterrows():
    if st.button(f"⏳ Watch Later: {row['title']}", key=f"watch_{row['url']}"):
        st.session_state.watch_later.append(row['title'])
        st.success(f"Added '{row['title']}' to Watch Later!")

# Display the 'Watch Later' list
if st.session_state.watch_later:
    st.subheader("Your Watch Later List")
    st.write(st.session_state.watch_later)
