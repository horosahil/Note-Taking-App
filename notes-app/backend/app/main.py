from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import connect_to_mongo, close_mongo_connection, settings
from .auth import router as auth_router
from .notes import router as notes_router

app = FastAPI(title="Notes API", version="1.0.0")

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

app.include_router(auth_router)
app.include_router(notes_router)

@app.get("/healthz")
def health():
    return {"status": "ok"}