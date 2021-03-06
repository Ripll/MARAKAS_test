import os
from dotenv import load_dotenv

load_dotenv()

user = os.environ['POSTGRES_USER']
password = os.environ['POSTGRES_PASSWORD']
host = os.environ['POSTGRES_HOST']
database = os.environ['POSTGRES_DB']
port = os.environ['POSTGRES_PORT']

SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
