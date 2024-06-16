from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from authlib.integrations.starlette_client import OAuth
from .config import settings

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

router = APIRouter()


@router.get("/login", name="login")
async def login(request: Request):
    try:
        redirect_uri = request.url_for("auth")
        print(f"Redirect URI: {redirect_uri}")
        return await oauth.google.authorize_redirect(request, redirect_uri)
    except Exception as e:
        print(f"Error in login route: {e}")
        raise e


@router.get("/auth", name="auth")
async def auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
        user = token.get("userinfo")
        print(f"User Info: {user}")
        request.session["user"] = user
        return RedirectResponse(url="/auth/profile")
    except Exception as e:
        print(f"Error in auth callback: {e}")
        raise e


@router.get("/profile", response_class=HTMLResponse)
async def profile(request: Request):
    user = request.session.get("user")
    if user:
        return f"""
        <html>
            <head>
                <title>Profile</title>
            </head>
            <body>
                <h1>Welcome, {user['name']}!</h1>
                <img src="{user['picture']}" alt="Profile Picture">
                <p><strong>Email:</strong> {user['email']}</p>
                <p><strong>Given Name:</strong> {user['given_name']}</p>
                <p><strong>Family Name:</strong> {user['family_name']}</p>
                <a href="/auth/logout">Logout</a>
            </body>
        </html>
        """
    return {"error": "User not logged in"}


@router.get("/logout", name="logout")
async def logout(request: Request):
    request.session.pop("user", None)
    return RedirectResponse(url="/")
