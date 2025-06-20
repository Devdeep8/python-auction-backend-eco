import os
from tortoise.contrib.sanic import register_tortoise
from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError
from dotenv import load_dotenv

load_dotenv()

DB_URL = f"mysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

def init_db(app):
    register_tortoise(
        app,
        db_url=DB_URL,
        modules={"models": ["app.models.auction"]},
        generate_schemas=True,
    )

    @app.listener("after_server_start")
    async def check_db_connection(app, loop):
        try:
            await Tortoise.init(
                db_url=DB_URL,
                modules={"models": ["app.models.auction"]}
            )
            conn = Tortoise.get_connection("default")
            await conn.execute_query("SELECT 1")
            print("✅ Database connection successful!")
        except DBConnectionError as e:
            print("❌ Failed to connect to database:", str(e))
        finally:
            await Tortoise.close_connections()
