# app/db.py
import os
from tortoise.contrib.sanic import register_tortoise
from dotenv import load_dotenv

load_dotenv()

DB_URL = f"mysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

def init_db(app):
    print("DB_URL:", DB_URL)
    register_tortoise(
        app,
        db_url=DB_URL,
        modules={"models": ["app.models.auction", "app.models.bid"]},  # Add bid model
        generate_schemas=True,
    )