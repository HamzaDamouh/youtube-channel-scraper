from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime, timedelta
from scraper.scraper import scrape_channel, insert_videos

def etl_task(channel_url):
    df = scrape_channel(channel_url, refresh=False, workers=5)
    records = df.to_dict('records')
    insert_videos(records)

with DAG(
    'youtube_etl',
    start_date=datetime(2025,4,1),
    schedule_interval='@daily',
    catchup=False,
    default_args={'retries':1,'retry_delay':timedelta(minutes=5)}
) as dag:

    channels = ['https://www.youtube.com/@channel1', 'https://www.youtube.com/@channel2']
    for url in channels:
        PythonOperator(
            task_id=f'scrape_{url.split('/')[-1]}',
            python_callable=etl_task,
            op_args=[url]
        )