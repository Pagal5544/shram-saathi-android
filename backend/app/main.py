from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.api.routes import router as marketplace_router
from app.core.config import settings
from app.core.database import engine

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Backend API for the Shram Saathi local labour marketplace.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(marketplace_router)


@app.get("/", tags=["system"])
def root():
    return {"name": settings.app_name, "version": "0.1.0", "docs": "/docs"}


@app.get(f"{settings.api_v1_prefix}/health", tags=["system"])
def health():
    return {"status": "ok", "service": "shram-saathi-api"}


@app.get(f"{settings.api_v1_prefix}/health/database", tags=["system"])
def database_health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        postgis = connection.execute(text("SELECT PostGIS_Version()")).scalar_one()
    return {"status": "ok", "database": "connected", "postgis": postgis}
