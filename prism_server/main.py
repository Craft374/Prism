# main.py
SECRET_DELETE_TOKEN = "3bb3fe309b352a7ca61215294a186c38c09fd4cb642db4771f0fcbf675df1873"

from fastapi import Body
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
from pathlib import Path
import uuid

app = FastAPI()
DATA_PATH = Path(__file__).parent / "account.json"


def load_data():
    if not DATA_PATH.exists():
        return {}
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


class AccountInit(BaseModel):
    username: str


class PasswordSet(BaseModel):
    username: str
    password_hash: str  # 클라이언트에서 (id + password) sha256 한 값


@app.get("/accounts")
def get_accounts():
    data = load_data()
    return JSONResponse(content=data)


@app.get("/check/{username}")
def check_user(username: str):
    data = load_data()
    if username in data:
        return {"exists": True, "id": data[username]["id"], "has_password": data[username]["password_hash"] is not None, "save_data": data[username]["save_data"]}
    return {"exists": False}


@app.post("/init")
def init_account(account: AccountInit):
    data = load_data()
    if account.username in data:
        raise HTTPException(status_code=400, detail="username already exists")
    user_id = str(uuid.uuid4())
    data[account.username] = {
        "id": user_id,
        "password_hash": None,
        "save_data": "MA=="
    }
    save_data(data)
    return {"message": "user id created", "id": user_id}


@app.post("/set_password")
def set_password(payload: PasswordSet):
    data = load_data()
    if payload.username not in data:
        raise HTTPException(status_code=404, detail="user not found")
    # 여기서는 해시를 검증하지 않고 그대로 저장만 함
    data[payload.username]["password_hash"] = payload.password_hash
    save_data(data)
    return {"message": "password set"}

class LoginPayload(BaseModel):
    username: str
    password_hash: str

@app.post("/login")
def login(payload: LoginPayload):
    data = load_data()
    if payload.username not in data:
        raise HTTPException(status_code=404, detail="user not found")
    stored = data[payload.username].get("password_hash")
    if stored is None:
        raise HTTPException(status_code=401, detail="password not set")
    if stored == payload.password_hash:
        return {"message": "login success"}
    raise HTTPException(status_code=401, detail="invalid credentials")

class SaveUpdate(BaseModel):
    username: str
    save_data: str  # base64 문자열 그대로


@app.post("/set_save")
def set_save(payload: SaveUpdate):
    data = load_data()

    if payload.username not in data:
        raise HTTPException(status_code=404, detail="user not found")

    # save_data만 수정 (password_hash / id는 건드리지 않음)
    data[payload.username]["save_data"] = payload.save_data

    save_data(data)
    return {"message": "save data updated"}

class DeletePayload(BaseModel):
    username: str
    token: str

@app.post("/delete")
def delete_account(payload: DeletePayload):
    if payload.token != SECRET_DELETE_TOKEN:
        raise HTTPException(status_code=403, detail="invalid delete token")

    data = load_data()

    if payload.username not in data:
        raise HTTPException(status_code=404, detail="user not found")

    del data[payload.username]
    save_data(data)

    return {"message": "account deleted"}