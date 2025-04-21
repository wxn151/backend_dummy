"""
░░▀ ░▀ ▀░▀▀░░
    w x n
░░▄░▄ ░▄░▄ ░░
"""
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from backend.core.config import description, title
from .routers import (auth, root, user)
#, visit, raking, docs, easter_egg)

app = FastAPI(
    title=title,
    description=description,
    version="1.0.0",
    # docs_url=None,  # <= Esto desactiva /docs
    # redoc_url=None,  # <= Esto desactiva /redoc
    # openapi_url=None  # <= Esto desactiva /openapi.json
)


origins = ["*"]

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root.router)
app.include_router(auth.router)
app.include_router(user.router)
# app.include_router(docs.router)
# app.include_router(visit.router)
# app.include_router(raking.router)

# Swagger: forzar esquema Bearer y eliminar client_id, username, etc.
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
