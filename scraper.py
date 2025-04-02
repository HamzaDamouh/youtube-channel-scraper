import yt_dlp
import pandas as pd
from datetime import timedelta

def seconds_to_hms(seconds: int) -> str:
    if seconds is None:
        return "00:00:00"
    return str(timedelta(seconds=seconds))

def scrape_channel_uploads(channel_url: str, output_csv: str = 'videos.csv'):
    ydl_opts = {
        'quiet': True,
        'extract_flat': False,  # Get full video data (not just metadata)
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Get the real channel ID from the channel URL
        channel_info = ydl.extract_info(channel_url, download=False)
        channel_id = channel_info.get('id')

        # Convert to the "uploads playlist" URL (all videos only)
        uploads_playlist_url = f"https://www.youtube.com/playlist?list=UU{channel_id[2:]}"
        print(f"📺 Fetching videos from: {uploads_playlist_url}")

        # Extract the uploads playlist content
        playlist_dict = ydl.extract_info(uploads_playlist_url, download=False)

    # Extract needed data
    videos = []
    for entry in playlist_dict.get('entries', []):
        videos.append({
            'id': entry['id'],
            'title': entry['title'],
            'duration': seconds_to_hms(entry.get('duration'))
        })

    # Save as CSV
    df = pd.DataFrame(videos)
    df.to_csv(output_csv, index=False)
    print(f"✅ Saved {len(df)} videos to {output_csv}")

if __name__ == "__main__":
    # 👇 Replace this with any public YouTube channel URL
    channel_url = 'https://www.youtube.com/@AndrejKarpathy'
    scrape_channel_uploads(channel_url)
