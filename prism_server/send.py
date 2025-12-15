# send.py
import requests
import hashlib
import base64


BASE_URL = "http://cr-api.kro.kr:56024"
# 로그인 가능 여부
def login(username: str, raw_password: str):
    # 먼저 사용자 존재 확인해서 id 가져오기
    res = requests.get(f"{BASE_URL}/check/{username}")
    if res.status_code != 200:
        return {"ok": False, "error": f"check failed: {res.status_code}"}
    info = res.json()
    if not info.get("exists"):
        return {"ok": False, "error": "user not found"}

    user_id = info["id"]
    # 클라이언트에서 (id + password) 해시 생성
    to_hash = (user_id + raw_password).encode("utf-8")
    password_hash = hashlib.sha256(to_hash).hexdigest()

    # 서버에 로그인 시도
    res = requests.post(f"{BASE_URL}/login", json={"username": username, "password_hash": password_hash})
    if res.status_code == 200:
        return {"ok": True, "result": res.json()}
    else:
        # 서버가 401/400 등 반환할 수 있음
        try:
            return {"ok": False, "error": res.json()}
        except Exception:
            return {"ok": False, "error": f"status {res.status_code}"}

# 유저가 있나 없나 체크
def check_user(username: str):
    res = requests.get(f"{BASE_URL}/check/{username}")
    print("check_user:", res.status_code, res.json())
    return res.json()

# id 발급
def init_account(username: str):
    res = requests.post(f"{BASE_URL}/init", json={"username": username})
    print("init_account:", res.status_code, res.json())
    return res.json()

# 패스워드 등록
def set_password(username: str, user_id: str, raw_password: str):
    # 클라이언트에서 (id + password)로 해시 생성
    to_hash = (user_id + raw_password).encode("utf-8")
    password_hash = hashlib.sha256(to_hash).hexdigest()
    res = requests.post(
        f"{BASE_URL}/set_password",
        json={"username": username, "password_hash": password_hash},
    )
    print("set_password:", res.status_code, res.json())
    return res.json()
def delete_account(username: str, token: str):
    res = requests.post(
        f"{BASE_URL}/delete",
        json={"username": username, "token": token}
    )
    try:
        return res.json()
    except:
        return {"ok": False, "error": "invalid response"}


def get_save_data(username: str, base64_decode: bool = True):
    # 유저 전체 정보 조회
    res = requests.get(f"{BASE_URL}/check/{username}")
    if res.status_code != 200:
        return None

    data = res.json()
    if not data.get("exists"):
        return None

    # user 데이터 내부의 save_data가 base64 문자열
    save_b64 = data.get("save_data")
    if not save_b64:
        return None

    try:
        if base64_decode:
            return str(base64.b64decode(save_b64).decode("utf-8"))
        else:
            return save_b64
    except Exception:
        return None

def set_save_data(username: str, save_raw: str):
    # 문자열 → base64
    save_b64 = base64.b64encode(save_raw.encode("utf-8")).decode("ascii")

    # save_data만 서버로 전송
    payload = {
        "username": username,
        "save_data": save_b64,
    }

    res = requests.post(f"{BASE_URL}/set_save", json=payload)
    return res.status_code == 200

if __name__ == "__main__":
    # 수정
    inp = int(input("1. 로그인 2. 회원가입 3. 데이터가져오기:  4.데이터저장 5"))
    if inp ==1:
        username = input("ID: ")
        pw = input("PWD: ")
        r = login(username, pw)
        print("login:", type(r), r["ok"])
    elif inp==2:
        username = input("ID: ")
        info = check_user(username)

        if not info.get("exists"):
            # 2. 계정 초기화 → id만 받아오기
            created = init_account(username)
            user_id = created["id"]
            pw = input("PWD: ")
            set_password(username, user_id, pw)
            r = login(username, pw)
            print("login:", r)
        else:
            print("이미 있는 아이디 입니다.")
    elif inp==3:
        username = input("ID: ")
        data = get_save_data(username, False)
        print("get_save_data:", data) # data상에 있는 \n이 작동안함
        # 데이터를 test.txt 파일로 저장
        try:
            with open('test.txt', 'w', encoding='utf-8') as f:
                f.write(data)
            print("✅ 데이터가 'test.txt' 파일에 성공적으로 저장되었습니다.")

            print("\n📜 파일 내용 출력:")
            with open('test.txt', 'r', encoding='utf-8') as f:
                lines = f.readlines()

                for line in lines:
                    print(line, end='')

        except IOError as e:
            print(f"❌ 파일 저장 또는 읽기 중 오류가 발생했습니다: {e}")
    elif inp==4:
        username = input("ID: ")
        save_raw = input("저장할 데이터: ").encode("utf-8").decode("unicode_escape")
        success = set_save_data(username, save_raw)
        print("set_save_data:", success)
    elif inp==5:
        username = input("ID: ")
        token = input("TOKEN: ")
        r = delete_account(username, token)
        print("delete_account:", r)