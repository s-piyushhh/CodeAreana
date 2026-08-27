from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.database import engine, Base
from apps import auth, problems, submissions

# creates all tables if they don't exist yet — fine for dev,
# switch to Alembic migrations once schema changes get more frequent
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CodeArena API")

app.add_middleware(
    CORSMiddleware,
    # tighten this to your real frontend URL before deploying
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(problems.router)
app.include_router(submissions.router)


@app.get("/")
def root():
    return {"message": "CodeArena API is running"}
