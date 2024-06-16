from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import HTMLResponse
from .routes import router

app = FastAPI()

# Secret key for session management
SECRET_KEY = (
    "your-generated-secret-key"  # Replace this with the strong secret key you generated
)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

app.include_router(router, prefix="/auth", tags=["auth"])


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Home</title>
        </head>
        <body>
            <h1>Welcome to Matie</h1>
            <a href="/auth/login"><button>Login with Google</button></a>
        </body>
    </html>
    """


@app.on_event("startup")
async def startup_event():
    # Debugging: Print registered routes
    for route in app.routes:
        print(route.path, route.name)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
