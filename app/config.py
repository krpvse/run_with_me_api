import os

from dotenv import load_dotenv

load_dotenv('.env')


# App
secret_key = os.getenv('SECRET_KEY')
hash_algorithm = os.getenv('HASH_ALGORITHM')

# PostgreSQL
db_host = os.getenv('DB_HOST')
db_port = int(os.getenv('DB_PORT'))
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_url = f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
