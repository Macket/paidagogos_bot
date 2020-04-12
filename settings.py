import os
from dotenv import load_dotenv

load_dotenv()

# --- ALL ---
DEBUG = os.getenv('DEBUG') == 'True'
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID'))

# --- ONLY PROD ---
DATABASE_URL=os.getenv('DATABASE_URL')

# --- ONLY LOCAL ---
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
PROXY = os.getenv('PROXY')
