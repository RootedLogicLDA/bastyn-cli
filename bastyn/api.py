import httpx

from .state import State


def _post(state: State, path: str, token: str) -> dict:
    payload = {"license_token": token, "client_info": state.client_info()}
    with httpx.Client(base_url=state.api_url, timeout=60.0) as c:
        r = c.post(path, json=payload)
        if r.status_code == 401:
            raise RuntimeError("Invalid license token")
        if r.status_code == 403:
            raise RuntimeError(r.json().get("detail", "License not active"))
        r.raise_for_status()
        return r.json()


def activate(state: State, token: str) -> dict:
    return _post(state, "/activate", token)


def rotate(state: State, token: str) -> dict:
    return _post(state, "/rotate", token)
