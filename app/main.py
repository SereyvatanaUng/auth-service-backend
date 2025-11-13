from fastapi import FastAPI
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, users

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/", tags=["Root"])
def root():
    """Root endpoint - API information"""
    return {
        "message": "Auth Service API",
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_PREFIX}/docs",
        "redoc": f"{settings.API_V1_PREFIX}/redoc",
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "service": "auth-service", "version": settings.VERSION}


app.include_router(auth.router, prefix=f"{settings.API_V1_PREFIX}/auth", tags=["Auth"])
app.include_router(
    users.router, prefix=f"{settings.API_V1_PREFIX}/users", tags=["User"]
)
