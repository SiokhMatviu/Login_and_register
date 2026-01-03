from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from database import create_tables, delete_tables
from login import router as login_router
from register import router as register_router
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost:5173",  # Vite
    "http://127.0.0.1:5173",
    "https://your-frontend-domain.com",  # якщо буде прод
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # або ["*"] для тестів
    allow_credentials=True,
    allow_methods=["*"],          # GET, POST, PUT, DELETE
    allow_headers=["*"],          # Authorization, Content-Type
)



app.include_router(login_router)
app.include_router(register_router)


@app.get("/")
async def root():
    return {"status": "ok", "message": "API is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)