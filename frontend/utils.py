import os

import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def call_root():
    response = requests.get(f"{BACKEND_URL}/")
    return response.json()


def call_health():
    response = requests.get(f"{BACKEND_URL}/health")
    return response.json()


def call_upload(file, file_type: str = "text/plain"):
    response = requests.post(
        f"{BACKEND_URL}/files/upload",
        files={"file_in": (file.name, file, file_type)},
    )
    return response.status_code, response.json()


def call_query(query: str, file_path: str):
    response = requests.post(
        f"{BACKEND_URL}/query",
        json={"query": query, "file_path": file_path},
    )
    return response.status_code, response.json()
