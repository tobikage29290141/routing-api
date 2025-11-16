from fastapi import FastAPI

app = FastAPI()

@app.get("/api/routing/health")
def health():
    return {"status": "ok"}
