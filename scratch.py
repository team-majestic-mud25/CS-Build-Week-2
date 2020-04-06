from graph_class import Graph
import requests
import time

g=Graph()

api_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"
token = 'c9916272fa1e2737b1850164ddf88e43280ad09c' #TODO should move this to a env file.
headers = {'Authorization': f'Token {token}',
           'Content-Type': 'application/json'}

response = requests.get(url=f"{api_url}init/", headers=headers)
initial_room = response.json() #converts to object/dict.
print(f"initial room = {initial_room['room_id']}\n")
time.sleep(initial_room['cooldown']) #avoid movement penalty.

print(f"found path = {g.bfs(initial_room['room_id'], 0)}")

path = g.bfs(initial_room['room_id'], 0)[:]
current_room = initial_room

while len(path) != 0:
    next_move = path.pop(0)
    print(g.connections[current_room['room_id']])
    payload = {"direction": f"{next_move}", "next_room_id":f"{g.connections[current_room['room_id']][next_move]}"}
    r = requests.post(url=f"{api_url}move/", headers=headers, json=payload)
    print(r.status_code, r)
    new_room = r.json()
    current_room = new_room
    time.sleep(new_room['cooldown'])