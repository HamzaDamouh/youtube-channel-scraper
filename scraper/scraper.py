import argparse
import concurrent.futures
import logging
import os
import pickle
import yt_dlp
import pandas as pd
from datetime import timedelta
from db.db_connection import insert_videos

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def seconds_to_hms(seconds): return timedelta(seconds=seconds) if seconds else timedelta()

def get_cache_file(channel_url): return f"cache/{channel_url.split('/')[-1]}.pkl"

def load_cache(channel_url):
    file = get_cache_file(channel_url)
    if os.path.exists(file):
        with open(file,'rb') as f: return pickle.load(f)
    return None

def save_cache(channel_url, df):
    os.makedirs('cache', exist_ok=True)
    with open(get_cache_file(channel_url),'wb') as f: pickle.dump(df, f)


def scrape_video(url, opts):
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
        date = info.get('upload_date')
        if date and len(date)==8: date = f"{date[:4]}-{date[4:6]}-{date[6:]}"
        return dict(
            title=info.get('title'),
            duration=str(timedelta(seconds=info.get('duration') or 0)),
            url=f"https://youtu.be/{info.get('id')}",
            published_date=date,
            description=info.get('description','')
        )
    except Exception as e:
        logging.warning(f"Error scraping {url}: {e}")
        return None


def scrape_channel(channel_url, refresh, workers):
    name = channel_url.split('/')[-1]
    df = None
    if not refresh:
        df = load_cache(channel_url)
    if df is None:
        base_opts = {'quiet':True,'skip_download':True,'extract_flat':True}
        with yt_dlp.YoutubeDL(base_opts) as ydl:
            info = ydl.extract_info(channel_url, download=False)
            plist = info.get('related_playlists',{}).get('uploads')
            playlist_url = f"https://www.youtube.com/playlist?list={plist}" if plist else channel_url
            entries = ydl.extract_info(playlist_url, download=False).get('entries',[])
        urls = [f"https://youtu.be/{e['id']}" for e in entries if e.get('id')]
        vids=[]
        opts={'quiet':True,'skip_download':True}
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
            for r in ex.map(lambda u: scrape_video(u,opts), urls):
                if r: vids.append(r)
        df = pd.DataFrame(vids)
        df['channel_name']=name
        save_cache(channel_url, df)
    return df


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--channels', nargs='+', required=True)
    p.add_argument('--refresh', action='store_true')
    p.add_argument('--workers', type=int, default=5)
    args=p.parse_args()

    all_videos=[]
    for ch in args.channels:
        df = scrape_channel(ch, args.refresh, args.workers)
        df.insert(0, 'id', range(1, len(df)+1))
        all_videos.extend(df.to_dict('records'))

    insert_videos(all_videos)

if __name__=='__main__':
    main()