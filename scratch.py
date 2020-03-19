from graph_class import Graph
import requests
import time

g=Graph()

api_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"
token = 'c9916272fa1e2737b1850164ddf88e43280ad09c' #TODO should move this to a env file.
headers = {'Authorization': f'Token {token}',
           'Content-Type': 'application/json'}

response = requests.get(url=f"{api_url}init/", headers=headers)
print(f"{response.status_code}")
initial_room = response.json() #converts to object/dict.
print(f"initial room = {initial_room['room_id']}\n")
time.sleep(initial_room['cooldown']) #avoid movement penalty.

print(g.bfs(initial_room['room_id'], 0))
