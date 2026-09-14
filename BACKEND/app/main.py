import os
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import OperationalError

from . import models
from .database import engine
from .routers import auth_router, progress_router


def create_tables_with_retry(max_attempts=10, delay_seconds=3):
    """Reintenta crear las tablas mientras MySQL termina de arrancar
    (útil en Docker Compose, donde ambos contenedores se lanzan a la vez)."""
    for attempt in range(1, max_attempts + 1):
        try:
            models.Base.metadata.create_all(bind=engine)
            print(f"[startup] Conectado a la base de datos (intento {attempt}).")
            return
        except OperationalError as e:
            print(f"[startup] MySQL no está listo aún (intento {attempt}/{max_attempts}): {e}")
            time.sleep(delay_seconds)
    raise RuntimeError("No se pudo conectar a la base de datos tras varios intentos.")


create_tables_with_retry()

app = FastAPI(title="PRENDE_SQL API")

# En producción, cambia "*" por el dominio real donde sirvas el HTML
# (por ejemplo: ["https://tudominio.com"]).
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(progress_router.router)


@app.get("/health")
def health():
    return {"status": "ok"}
