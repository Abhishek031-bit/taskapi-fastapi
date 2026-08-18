from fastapi import FastAPI

from taskapi.routers import auth

app = FastAPI(title="TaskAPI")
app.include_router(auth.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
