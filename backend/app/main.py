"""FastAPI 应用入口。"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models  # noqa: F401  注册表
from .database import Base, engine
from .routers import (
    admin,
    answers,
    auth,
    categories,
    notifications,
    questions,
    search,
    users,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="findanswer", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(questions.router)
app.include_router(answers.router)
app.include_router(categories.router)
app.include_router(search.router)
app.include_router(users.router)
app.include_router(notifications.router)
app.include_router(admin.router)


@app.get("/health")
def health():
    return {"status": "ok"}
