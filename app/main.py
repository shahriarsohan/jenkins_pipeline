from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "breathing... and healthy v3"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
