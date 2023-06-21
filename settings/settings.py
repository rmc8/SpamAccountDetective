import os
import json
from typing import Dict, List

import PySimpleGUI as sg


def save_credentials(credentials: Dict[str, str]) -> None:
    with open("twitter_credentials.json", "w") as file:
        json.dump(credentials, file)


def load_credentials() -> Dict[str, str]:
    if os.path.exists("twitter_credentials.json"):
        with open("twitter_credentials.json", "r") as file:
            credentials = json.load(file)
        return credentials
    return {}


def create_input_box(
    text: str, key: str, size_tuple: tuple, credentials: Dict[str, str]
) -> List:
    return [
        sg.Text(text, size=size_tuple),
        sg.Input(key=key, default_text=credentials.get(key, "")),
    ]


sg.theme("Dark Brown")
size_tuple: tuple = (16, 1)
credentials: Dict[str, str] = load_credentials()
input_boxes: List = [
    create_input_box(t, k, size_tuple, credentials)
    for t, k in (
        ("API Key", "api_key"),
        ("API Key Secret", "api_key_secret"),
        ("Bearer Token", "bearer_token"),
        ("Access Token", "access_token"),
        ("Access Token Secret", "token_secret"),
    )
]
layout: list = input_boxes + [[sg.Button("Save"), sg.Button("Exit")]]

window = sg.Window("Twitter API Credentials", layout)

while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "Exit"):
        break
    elif event == "Save":
        credentials = {key: values[key] for key in credentials}
        save_credentials(credentials)
        sg.popup("Credentials saved successfully!", title="Success")
window.close()
