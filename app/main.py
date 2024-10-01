import socket
import logging
import os
import secrets
import string

from fastapi import FastAPI
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware

def generate_secret_key(length=38):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))


app = FastAPI()

logger = logging.getLogger("api")

app.add_middleware(SessionMiddleware, secret_key=os.environ.get("SECRET_KEY", default=generate_secret_key()),
                   session_cookie=os.environ.get(
                       "SESSION_COOKIE_NAME", default=f"session-fastapi-hello-world-{generate_secret_key(length=4)}"))


@app.get('/health')
async def health():
    return {
        "status": "OK"
    }


@app.get("/")
async def root(request: Request):

    hostname = socket.gethostname()

    if "counter" not in request.session:
        request.session["counter"] = 0

    if "hostnames" not in request.session:
        request.session["hostnames"] = {}

    if socket.gethostname() not in request.session["hostnames"]:
        request.session["hostnames"][hostname] = 0

    request.session["hostnames"][hostname] += 1
    request.session["counter"] += 1

    debug_msg = {
        "counter": request.session["counter"],
        "host": socket.getfqdn(),
        "hostnames": request.session["hostnames"],
        "request": {
            "method": request.method,
            "url": request.url,
            "headers": request.headers,
            "path_params": request.path_params,
            "client": request.client,
            "cookies": request.cookies,
            "session": request.session,
        },
    }

    logger.debug(debug_msg)

    return debug_msg
