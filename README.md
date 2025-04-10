YouTube Channel Scraper
A simple Python script that uses yt-dlp to scrape video metadata from a YouTube channel. It extracts information like title, duration, published date, and description. The script uses parallel processing and caching, and it exports data in CSV, JSON, or Excel formats.

Requirements
Python 3.6 or higher

yt-dlp

pandas

ffmpeg (ensure it's installed and available in your system PATH or update the script with its location)

Install dependencies with:

bash
Copy
pip install yt-dlp pandas
Usage
Run the script using the command line. For example:

bash
Copy
python scraper.py --channel "https://www.youtube.com/@{channelid}/videos" --output "channel_videos.csv" --format csv --refresh --workers 8
Command-Line Options
--channel: (Required) The YouTube channel URL.

--output: Output filename (default: videos.csv).

--format: Output format: csv, json, or excel (default: csv).

--refresh: Force a fresh scrape (ignore cached data).

--workers: Number of parallel worker threads (default: 5).

Notes
The script assigns sequential IDs (1, 2, 3, …) to videos instead of the original YouTube video IDs.

The data is cached to avoid re-scraping unchanged channels.
