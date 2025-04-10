import argparse
import concurrent.futures
import logging
import os
import pickle
import yt_dlp
import pandas as pd
from datetime import timedelta

def seconds_to_hms(seconds: int) -> str:
    """Convert seconds to hh:mm:ss format."""
    if seconds is None:
        return "00:00:00"
    return str(timedelta(seconds=seconds))

def get_cache_file(channel_url: str) -> str:
    """Create a cache filename based on the channel URL."""
    return f"{channel_url.split('/')[-1]}.pkl"

def load_cache(channel_url: str):
    """Load cached data if available."""
    cache_file = get_cache_file(channel_url)
    if os.path.exists(cache_file):
        logging.info("Loading data from cache.")
        with open(cache_file, 'rb') as f:
            return pickle.load(f)
    return None

def save_cache(channel_url: str, data):
    """Save scraped data to cache."""
    with open(get_cache_file(channel_url), 'wb') as f:
        pickle.dump(data, f)
    logging.info("Data saved to cache.")

def scrape_video(video_url: str, ydl_opts: dict):
    """
    Scrape metadata for a single video.
    Each thread instantiates its own YoutubeDL object for thread safety.
    """
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_data = ydl.extract_info(video_url, download=False)
        logging.info(f"Scraped video: {video_data.get('title')}")
        # Extract published_date from 'upload_date' if available
        published_date = video_data.get('upload_date')
        if published_date and len(published_date) == 8:
            published_date = f"{published_date[:4]}-{published_date[4:6]}-{published_date[6:]}"
        else:
            published_date = None
        # Extract description (or default to an empty string)
        description = video_data.get('description', "")
        return {
            'title': video_data.get('title'),
            'duration': seconds_to_hms(video_data.get('duration')),
            'url': f"https://www.youtube.com/watch?v={video_data.get('id')}",
            'published_date': published_date,
            'description': description
        }
    except Exception as e:
        logging.warning(f"Failed to fetch video {video_url}: {e}")
        return None

def save_output(df: pd.DataFrame, output_file: str, output_format: str):
    """Save the output DataFrame in CSV, JSON, or Excel format."""
    if output_format.lower() == 'csv':
        df.to_csv(output_file, index=False)
    elif output_format.lower() == 'json':
        df.to_json(output_file, orient='records', force_ascii=False, indent=4)
    elif output_format.lower() == 'excel':
        df.to_excel(output_file, index=False)
    else:
        # just in case
        logging.error(f"Unsupported output format: {output_format}")
        return
    logging.info(f"Saved {len(df)} videos to {output_file}")

def scrape_channel_uploads(channel_url: str, output_file: str, output_format: str,
                           refresh_cache: bool, max_workers: int = 5):
    """
    Scrape a YouTube channel's uploads.
    Checks and optionally bypasses the cache
    Uses the channel's 'uploads' playlist (if available) for complete results
    Scrapes video metadata in parallel
    Saves the results in the specified output format.
    """
    # Use cache if available unless a refresh is requested
    if not refresh_cache:
        cached = load_cache(channel_url)
        if cached is not None:
            logging.info("Using cached data.")
            cached.insert(0, 'id', range(1, len(cached) + 1))
            return cached

    
    base_ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,   #
        'playlistend': None,    
    }

    with yt_dlp.YoutubeDL(base_ydl_opts) as ydl:
        try:
            channel_info = ydl.extract_info(channel_url, download=False)
        except Exception as e:
            logging.error(f"Failed to extract channel info: {e}")
            return None

        
        uploads_playlist_url = None
        if 'related_playlists' in channel_info and 'uploads' in channel_info['related_playlists']:
            uploads_playlist_id = channel_info['related_playlists']['uploads']
            uploads_playlist_url = f"https://www.youtube.com/playlist?list={uploads_playlist_id}"
        
        if uploads_playlist_url:
            logging.info(f"Using uploads playlist: {uploads_playlist_url}")
            try:
                playlist_info = ydl.extract_info(uploads_playlist_url, download=False)
                entries = playlist_info.get('entries', [])
            except Exception as e:
                logging.error(f"Failed to extract playlist info: {e}")
                entries = []
        else:
            entries = channel_info.get('entries', [])

        logging.info(f"Found {len(entries)} videos. Starting metadata scraping...")

        
        video_urls = []
        for entry in entries:
            video_id = entry.get('id')
            if video_id:
                full_url = f"https://www.youtube.com/watch?v={video_id}"
                logging.info(f"Queueing video URL: {full_url}")
                video_urls.append(full_url)
            else:
                logging.warning("Skipping an entry without a video id.")

    
    video_ydl_opts = {
        'quiet': True,
        'skip_download': True
    }
    
    # ThreadPoolExecutor to scrape video metadata in parallel
    videos = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(scrape_video, url, video_ydl_opts): url for url in video_urls}
        for future in concurrent.futures.as_completed(future_to_url):
            result = future.result()
            if result:
                videos.append(result)

    
    df = pd.DataFrame(videos)
    
    df.insert(0, 'id', range(1, len(df) + 1))
    save_output(df, output_file, output_format)
    save_cache(channel_url, df)
    return df



if __name__ == '__main__':
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Set up command-line arguments
    parser = argparse.ArgumentParser(description="YouTube Channel Scraper")
    parser.add_argument('--channel', required=True, help="YouTube channel URL or channel videos URL")
    parser.add_argument('--output', default='videos.csv', help="Output file name")
    parser.add_argument('--format', default='csv', choices=['csv', 'json', 'excel'], 
                        help="Output file format (csv, json, excel)")
    parser.add_argument('--refresh', action='store_true', help="Force refresh (ignore cache)")
    parser.add_argument('--workers', type=int, default=5, help="Maximum number of parallel workers")
    args = parser.parse_args()

    scrape_channel_uploads(args.channel, args.output, args.format, args.refresh, args.workers)
