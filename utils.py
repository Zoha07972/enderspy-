# -----------------------------------------------------------------------------
# File:        utils.py
# Description: Shared helpers for file I/O, formatting, and server queries.
# Author:      X
# Created:     06/02/2025
# Updated:     12/05/2025
# -----------------------------------------------------------------------------

import os
import json
import re
from datetime import datetime, timedelta
DATA_FILE = "server_data.json"
# ─── Helper: File I/O ────────────────────────────────────────────────────────────────
def save_data(data: dict):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def load_data() -> dict:
    if not os.path.isfile(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def format_uptime(seconds: int) -> str:
    td = timedelta(seconds=seconds)
    hrs, rem = divmod(td.seconds, 3600)
    mins, secs = divmod(rem, 60)
    parts = []
    if hrs:  parts.append(f"{hrs}h")
    if mins: parts.append(f"{mins}m")
    parts.append(f"{secs}s")
    return " ".join(parts)

def clear_data():
    if os.path.isfile(DATA_FILE):
        os.remove(DATA_FILE)

