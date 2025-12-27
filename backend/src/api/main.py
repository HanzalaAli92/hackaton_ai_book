from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .v1.ingest import router as ingest_router
from .v1.query import router as query_router
from .v1.health import router as health_router
from ..config import settings
from ..middleware.rate_limit import rate_limit_check


def create_app():
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        debug=settings.debug,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add rate limiting middleware
    @app.middleware("http")
    async def add_rate_limiting(request: Request, call_next):
        # Extract client IP for rate limiting
        client_ip = request.headers.get("x-forwarded-for", request.client.host)
        if client_ip:
            # Use the first IP if there are multiple (in case of multiple proxies)
            client_ip = client_ip.split(",")[0].strip()
        else:
            client_ip = request.client.host

        # Apply rate limiting to API routes (not to health checks)
        if request.url.path.startswith(settings.api_v1_prefix) and not request.url.path.endswith("/health"):
            rate_limit_check(client_ip)

        response = await call_next(request)
        return response

    # Include API routers
    app.include_router(ingest_router, prefix=settings.api_v1_prefix)
    app.include_router(query_router, prefix=settings.api_v1_prefix)
    app.include_router(health_router, prefix=settings.api_v1_prefix)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)