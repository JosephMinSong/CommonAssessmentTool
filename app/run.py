import uvicorn


def start():
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        # If you're running in production, disable reload=True
        # it's meant for development only and consumes more resources.
        reload=True, 
    )


if __name__ == "__main__":
    start()
