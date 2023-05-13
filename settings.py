from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME, SECRET_KEY
import os

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
SECRET_KEY = SECRET_KEY
