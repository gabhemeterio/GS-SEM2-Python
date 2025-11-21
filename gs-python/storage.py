import json
import os


def _get_path(filename: str) -> str:
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, filename)


def load_json(filename: str, default):
    """
    Carrega dados de um arquivo JSON.
    Se não existir ou estiver corrompido, retorna 'default'.
    """
    path = _get_path(filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        return default


def save_json(filename: str, data) -> None:
    """
    Salva 'data' em JSON (indentado, legível).
    """
    path = _get_path(filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)