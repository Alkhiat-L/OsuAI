"""
Versão antiga do projeto, que foi feita para funcionar gravando a tela do jogo original,
essa versão não está mais sendo atualizada. A versão atualizada do projeto está na pasta
'osupy'.
"""

import json
import time
from urllib import request

from websockets.sync.client import connect


def get_name() -> str:
    with connect("ws://localhost:20727/tokens?updatesPerSecond=60") as websocket:
        websocket.send(json.dumps(["username"]))
        data = json.loads(websocket.recv())
        username = data["username"]
    return username


def get_status() -> str:
    with connect("ws://localhost:20727/tokens?updatesPerSecond=60") as websocket:
        websocket.send(json.dumps(["status"]))
        data = json.loads(websocket.recv())
        status_id = int(data["status"])
        if status_id == 1:
            return "Listening"
        if status_id == 2:
            return "Playing"
    return "Error"


if __name__ == "__main__":
    start_time = time.time()
    print(json.loads(request.urlopen("http://localhost:20727/json").read()))
    print("Seconds since start: ", time.time() - start_time)
    print(get_status())


# 2 == 'Playing'
# 1 == Listening
def get_combo() -> int:
    with connect("ws://localhost:20727/tokens?updatesPerSecond=60") as websocket:
        websocket.send(json.dumps(["combo"]))
        data = json.loads(websocket.recv())
        combo = int(data["combo"])
    return combo


def get_misses() -> int:
    with connect("ws://localhost:20727/tokens?updatesPerSecond=60") as websocket:
        websocket.send(json.dumps(["misses"]))
        data = json.loads(websocket.recv())
        misses = int(data["misses"])
    return misses


def get_50() -> int:
    with connect("ws://localhost:20727/tokens?updatesPerSecond=60") as websocket:
        websocket.send(json.dumps(["c50"]))
        data = json.loads(websocket.recv())
        c50 = int(data["c50"])
    return c50


def get_100() -> int:
    with connect("ws://localhost:20727/tokens?updatesPerSecond=60") as websocket:
        websocket.send(json.dumps(["c100"]))
        data = json.loads(websocket.recv())
        c100 = int(data["c100"])
    return c100


def get_300() -> int:
    with connect("ws://localhost:20727/tokens?updatesPerSecond=60") as websocket:
        websocket.send(json.dumps(["c300"]))
        data = json.loads(websocket.recv())
        c300 = int(data["c300"])
    return c300


def get_hp() -> float:
    with connect("ws://localhost:20727/tokens?updatesPerSecond=60") as websocket:
        websocket.send(json.dumps(["playerHp"]))
        data = json.loads(websocket.recv())
        hp = float(data["playerHp"])
    return hp
