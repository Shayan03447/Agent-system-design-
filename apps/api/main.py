"""FastAPI entrypoint: ASGI app object lives here as `app`."""

from fastapi import FastAPI

app = FastAPI(
    title="Ecommerce Agent API",
    version="0.1.0",
    description="Day-1 health check and future chat/email routes.",
)


@app.get("/health", tags=["ops"])
def health() -> dict[str, str]:
    """Liveness probe for deploys and local checks."""
    return {"status": "ok"}
