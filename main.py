import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app="server:app",
        workers=1,
    )