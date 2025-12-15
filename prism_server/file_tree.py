import os
import json


def build_tree(path: str) -> dict:
    """주어진 경로의 폴더 구조 및 파일 내용을 트리(dict)로 반환."""
    children = []

    for entry in os.listdir(path):
        full = os.path.join(path, entry)

        if os.path.isdir(full):
            children.append({
                "name": entry,
                "type": "folder",
                "children": build_tree(full).get("children", [])
            })
        else:
            # 파일 내용 읽기
            try:
                with open(full, "r", encoding="utf-8") as f:
                    content = f.read()
            except:
                # 바이너리 파일 등 읽기 불가한 경우 빈 문자열 처리
                content = ""

            children.append({
                "name": entry,
                "type": "file",
                "content": content
            })

    return {
        "name": os.path.basename(path),
        "type": "folder",
        "children": children
    }


def save_structure(src_path: str, json_path: str) -> None:
    """폴더 구조 및 파일 내용을 JSON 파일로 저장."""
    tree = build_tree(src_path)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(tree, f, indent=4, ensure_ascii=False)


def create_structure(base_path: str, node: dict) -> None:
    """JSON 트리를 기반으로 실제 폴더 구조 및 파일 내용을 생성."""
    current = os.path.join(base_path, node["name"])

    if node["type"] == "folder":
        os.makedirs(current, exist_ok=True)
        for child in node.get("children", []):
            create_structure(current, child)

    elif node["type"] == "file":
        create_file(current, node.get("content", ""))


def create_file(file_path: str, content: str) -> None:
    """파일 생성 및 내용 쓰기."""
    # 폴더와 같은 이름이면 건너뜀
    if os.path.isdir(file_path):
        return

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)


def load_structure(json_path: str, target_path: str) -> None:
    """JSON 파일을 읽어 실제 폴더와 파일로 복원."""
    with open(json_path, "r", encoding="utf-8") as f:
        tree = json.load(f)
    create_structure(target_path, tree)


if __name__ == "__main__":
    src = "/Users/jeongwoo/Documents/Github/ARG_Game/prism_server/Alex_PC"
    json_file = "/Users/jeongwoo/Documents/Github/ARG_Game/client/Client/Assets/StreamingAssets/computer/Q6.json"
    target = "/Users/jeongwoo/Documents/Github/ARG_Game/prism_server/folders/RecreatedFolder"

    save_structure(src, json_file)
    # load_structure(json_file, target)
    print("완료")
