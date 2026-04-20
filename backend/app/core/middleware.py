import logging

from fastapi import FastAPI, Request
from starlette.responses import Response, JSONResponse

from backend.app.core.exceptions import AppError
from backend.app.core.security import decode_access_token

log = logging.getLogger(__name__)

PUBLIC_PATHS = {
    "/",
    "/auth/register",
    "/auth/login",
    "/auth/refresh",
    "/hotels",
    "/rooms/available",
    "/rooms",
    "/docs",
    "/openapi.json",
}

recent_requests: dict[str, float] = {}

def register_middleware(app: FastAPI) -> None:

   #  @app.middleware("http")
   #  async def rate_limit(
   #          request: Request,
   #          call_next
   # ):
   #      client_ip = request.client.host if request.client else "unknown"
   #      now = time.monotonic()
   #
   #      last_request = recent_requests.get(client_ip, 0)
   #
   #      if now - last_request < 1.0:
   #          return JSONResponse(
   #              status_code=429,
   #             content={"detail": "Too many requests"}
   #          )
   #      recent_requests[client_ip] = now
   #      return await call_next(request)

    @app.middleware("http")
    async def log_info_request(
            request: Request,
            call_next
    ):
        user_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path

        response = await call_next(request)

        log.info(f"{method} {path} — {response.status_code} — IP: {user_ip}")
        return response

    @app.middleware("http")
    async def token_verify(request: Request, call_next) -> Response:

        if request.method == "OPTIONS":
            return await call_next(request)

        path = request.url.path.rstrip("/") or "/"

        if any(path == p or path.startswith(p + "/") for p in PUBLIC_PATHS):
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"detail": "Token missing"}
            )
        token = auth_header.split(" ")[1]
        try:
            payload = decode_access_token(token)
        except AppError:
            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})
        if not payload:
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired token"}
            )

        request.state.user_payload = payload
        return await call_next(request)