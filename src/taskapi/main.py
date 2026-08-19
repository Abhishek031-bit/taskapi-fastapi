from fastapi import FastAPI

from taskapi.routers import auth, organizations, projects, users

app = FastAPI(title="TaskAPI")
app.include_router(auth.router)
app.include_router(organizations.router)
app.include_router(projects.router)
app.include_router(users.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
