import uvicorn


def start():
    uvicorn.run(
        "app.main:app",
        reload=True,
    )


if __name__ == "__main__":
    start()
