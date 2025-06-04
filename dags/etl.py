from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import requests

default_args = {
    'start_date': datetime.now() - timedelta(days=1)
}

with DAG(
    dag_id='nasa_apod_postgres',
    description='ETL Pipeline that fetches NASA APOD data and loads into Postgres.',
    schedule='@daily',
    default_args=default_args,
    catchup=False,
    tags=['NASA'],
) as dag:

    @task
    def create_table():
        postgres_hook = PostgresHook(postgres_conn_id='postgres_default')
        create_table_query = """ 
        CREATE TABLE IF NOT EXISTS apod_data(
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE,
            media_type VARCHAR(50)
        );
        """
        postgres_hook.run(create_table_query)

    @task
    def extract_apod():
        url = 'https://api.nasa.gov/planetary/apod'
        params = {
            'api_key': 'WKLHKz4mtu0KrezQG67wOtMg2p2T0TSmv3K3KgnF'  # Replace with your API key or load from Variables
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    @task
    def transform_apod_data(response):
        return {
            'title': response.get('title', ''),
            'explanation': response.get('explanation', ''),
            'url': response.get('url', ''),
            'date': response.get('date', ''),
            'media_type': response.get('media_type', '')
        }

    @task
    def load_data_to_postgres(apod_data):
        postgres_hook = PostgresHook(postgres_conn_id='postgres_default')
        insert_query = """
        INSERT INTO apod_data (title, explanation, url, date, media_type)
        VALUES (%s, %s, %s, %s, %s);
        """
        postgres_hook.run(insert_query, parameters=[
            apod_data['title'], apod_data['explanation'],
            apod_data['url'], apod_data['date'], apod_data['media_type']
        ])

    create = create_table()
    extracted = extract_apod()
    transformed = transform_apod_data(extracted)
    load = load_data_to_postgres(transformed)

    create >> extracted
