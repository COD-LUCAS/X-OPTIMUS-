import os
import sys
import time
import json
import pkgutil
import importlib
from dataclasses import dataclass, field

from telethon import TelegramClient
from telethon.sessions import StringSession


def load_env_file(path="config.env"):
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            os.environ.setdefault(key, value)


load_env_file()


def parse_int(value, default=0):
    try:
        return int(str(value))
    except Exception:
        return default


def parse_sudo_ids(raw):
    ids = set()
    if not raw:
        return ids
    for part in raw.replace(",", " ").split():
        try:
            ids.add(int(part))
        except Exception:
            pass
    return ids


def read_version(path="version.txt"):
    if not os.path.exists(path):
        return "1.0.0"
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().strip() or "1.0.0"
    except Exception:
        return "1.0.0"


@dataclass
class BotConfig:
    api_id: int
    api_hash: str
    string_session: str
    owner_id: int
    owner_name: str
    sudo_ids: set = field(default_factory=set)
    mode: str = "PUBLIC"
    version: str = "1.0.0"
    start_time: float = field(default_factory=time.time)
    core_plugins: list = field(default_factory=list)
    loaded_plugins: dict = field(default_factory=dict)


api_id_env = os.environ.get("API_ID")
api_hash_env = os.environ.get("API_HASH")
string_env = os.environ.get("STRING_SESSION")

if not api_id_env or not api_hash_env or not string_env:
    print("Missing API_ID / API_HASH / STRING_SESSION in env or config.env")
    sys.exit(1)

API_ID = parse_int(api_id_env)
API_HASH = api_hash_env
STRING_SESSION = string_env

OWNER_ID = parse_int(os.environ.get("OWNER_ID"))
OWNER_NAME
