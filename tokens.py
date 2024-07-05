import json
from websockets.sync.client import connect


def get_name() -> str:
    with connect('ws://localhost:20727/tokens?updatesPerSecond=60') as websocket:
        websocket.send(json.dumps(['username']))
        data = json.loads(websocket.recv())
        username = data['username']
    return username


def get_status() -> int:
    with connect('ws://localhost:20727/tokens?updatesPerSecond=60') as websocket:
        websocket.send(json.dumps(['status']))
        data = json.loads(websocket.recv())
        status = int(data['status'])
    return status


def get_combo() -> int:
    with connect('ws://localhost:20727/tokens?updatesPerSecond=60') as websocket:
        websocket.send(json.dumps(['combo']))
        data = json.loads(websocket.recv())
        combo = int(data['combo'])
    return combo


def get_misses() -> int:
    with connect('ws://localhost:20727/tokens?updatesPerSecond=60') as websocket:
        websocket.send(json.dumps(['misses']))
        data = json.loads(websocket.recv())
        misses = int(data['misses'])
    return misses


def get_50() -> int:
    with connect('ws://localhost:20727/tokens?updatesPerSecond=60') as websocket:
        websocket.send(json.dumps(['c50']))
        data = json.loads(websocket.recv())
        c50 = int(data['c50'])
    return c50


def get_100() -> int:
    with connect('ws://localhost:20727/tokens?updatesPerSecond=60') as websocket:
        websocket.send(json.dumps(['c100']))
        data = json.loads(websocket.recv())
        c100 = int(data['c100'])
    return c100


def get_300() -> int:
    with connect('ws://localhost:20727/tokens?updatesPerSecond=60') as websocket:
        websocket.send(json.dumps(['c300']))
        data = json.loads(websocket.recv())
        c300 = int(data['c300'])
    return c300


def get_hp() -> float:
    with connect('ws://localhost:20727/tokens?updatesPerSecond=60') as websocket:
        websocket.send(json.dumps(['playerHp']))
        data = json.loads(websocket.recv())
        hp = float(data['playerHp'])
    return hp

