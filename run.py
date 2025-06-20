from app.main import app

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
        auto_reload=True,     # <--- Enables file change watching
        workers=1             # <--- Use single worker to support reload
    )
