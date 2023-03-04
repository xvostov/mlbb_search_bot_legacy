import os

from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
PROM_EXP_PORT = int(os.environ.get('PROM_EXP_PORT'))
DB_PASSWORD = os.environ.get('MYSQL_ROOT_PASSWORD')
DB_HOST = os.environ.get('MYSQL_HOST')
DB_PORT = os.environ.get('MYSQL_PORT')
DB_NAME = os.environ.get('MYSQL_DATABASE')

