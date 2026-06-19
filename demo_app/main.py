from itertools import count
from typing import Optional

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, EmailStr


app = FastAPI(title="QA Portfolio Demo App")

ADMIN_TOKEN = "demo-admin-token"
VIEWER_TOKEN = "demo-viewer-token"

users = {
    1: {
        "id": 1,
        "name": "Admin QA",
        "email": "admin@teste.com",
        "role": "admin",
        "status": "active",
    },
    2: {
        "id": 2,
        "name": "Viewer QA",
        "email": "viewer@teste.com",
        "role": "viewer",
        "status": "active",
    },
}
next_user_id = count(3)


class LoginPayload(BaseModel):
    email: EmailStr
    password: str


class CreateUserPayload(BaseModel):
    name: str
    email: EmailStr
    role: str


def require_token(authorization: Optional[str] = Header(default=None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = authorization.removeprefix("Bearer ").strip()
    if token not in {ADMIN_TOKEN, VIEWER_TOKEN}:
        raise HTTPException(status_code=401, detail="Invalid bearer token")
    return token


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/auth/login")
def login(payload: LoginPayload):
    credentials = {
        ("admin@teste.com", "Admin@123"): ADMIN_TOKEN,
        ("viewer@teste.com", "Viewer@123"): VIEWER_TOKEN,
        ("iron@teste.com", "Senha@123"): ADMIN_TOKEN,
    }
    token = credentials.get((payload.email, payload.password))
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"token": token}


@app.get("/api/users")
def list_users(authorization: Optional[str] = Header(default=None)):
    require_token(authorization)
    return list(users.values())


@app.post("/api/users", status_code=201)
def create_user(payload: CreateUserPayload, authorization: Optional[str] = Header(default=None)):
    require_token(authorization)
    if payload.role not in {"admin", "viewer"}:
        raise HTTPException(status_code=422, detail="Invalid role")

    if any(user["email"] == payload.email for user in users.values()):
        return JSONResponse(
            status_code=409,
            content={"message": "User already exists"},
        )

    user_id = next(next_user_id)
    user = {
        "id": user_id,
        "name": payload.name,
        "email": payload.email,
        "role": payload.role,
        "status": "active",
    }
    users[user_id] = user
    return user


@app.delete("/api/users/{user_id}", status_code=204)
def delete_user(user_id: int, authorization: Optional[str] = Header(default=None)):
    token = require_token(authorization)
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")

    del users[user_id]
    return None


@app.get("/login", response_class=HTMLResponse)
def login_page():
    return """
    <!doctype html>
    <html lang="pt-BR">
      <head>
        <meta charset="utf-8" />
        <title>Login - QA Portfolio</title>
      </head>
      <body>
        <main>
          <h1>Login</h1>
          <form id="login-form">
            <label for="email">Email</label>
            <input id="email" name="email" type="email" />

            <label for="senha">Senha</label>
            <input id="senha" name="senha" type="password" />

            <button type="submit">Entrar</button>
          </form>
          <div id="messages"></div>
        </main>
        <script>
          const form = document.querySelector("#login-form");
          const messages = document.querySelector("#messages");

          form.addEventListener("submit", (event) => {
            event.preventDefault();
            messages.innerHTML = "";

            const email = document.querySelector("#email").value;
            const senha = document.querySelector("#senha").value;

            if (!email || !senha) {
              messages.innerHTML = "<p>Campo obrigatório</p><p>Campo obrigatório</p>";
              return;
            }

            if (email === "iron@teste.com" && senha === "Senha@123") {
              window.location.href = "/dashboard";
              return;
            }

            messages.innerHTML = '<div role="alert">Credenciais inválidas</div>';
          });
        </script>
      </body>
    </html>
    """


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard_page():
    return """
    <!doctype html>
    <html lang="pt-BR">
      <head>
        <meta charset="utf-8" />
        <title>Dashboard - QA Portfolio</title>
      </head>
      <body>
        <header>
          <span data-testid="user-name">Iron</span>
        </header>
        <main>
          <h1>Bem-vindo</h1>
        </main>
      </body>
    </html>
    """
