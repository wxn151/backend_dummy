"""
░░░ ░░▀ ░░▀▀░░░
     w x n
░░░▄ ░░░▄░▄  ░░
"""
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.routing import APIRoute
from backend.core.config import description, title
from .routers import (auth, user, article)

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

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(article.router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Solo defines el esquema Bearer una vez
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Aplica BearerAuth solo a endpoints que usen `get_current_user`
    for route in app.routes:
        if isinstance(route, APIRoute):
            if any(
                getattr(d.call, "__name__", None) == "get_current_user"
                for d in route.dependant.dependencies
            ):
                path = openapi_schema["paths"].get(route.path)
                if path:
                    for operation in path.values():
                        operation.setdefault("security", []).append({"BearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


@app.get("/")
def read_root():
    return {"message": "Behemoth Backend"}
