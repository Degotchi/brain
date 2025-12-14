"""
Brain service entrypoint (FastAPI / Scheduler).

Scaffold-only: keep this file minimal until the Brain API is integrated into
the existing backend app (`degotchi/backend/main.py`).
"""

from fastapi import FastAPI


app = FastAPI(title="Degotchi Brain", version="0.1.0")


@app.get("/")
def health():
    return {"status": "ok"}


