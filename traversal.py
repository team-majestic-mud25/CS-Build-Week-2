import requests
import time
from graph_class import Graph

start = time.time()
graph = Graph()

#make initial request and pass result room into dft recursive
api_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"
token = 'c9916272fa1e2737b1850164ddf88e43280ad09c' #TODO should move this to a env file.
headers = {'Authorization': f'Token {token}',
           'Content-Type': 'application/json'}

response = requests.get(url=f"{api_url}init/", headers=headers)
print(f"{response.status_code}")
initial_room = response.json() #converts to object/dict.
print(f"initial room = {initial_room['room_id']}\n")
time.sleep(initial_room['cooldown']) #avoid movement penalty.

graph.dft_recursive(initial_room)

#pull out the resulting data
directions = graph.connections
rooms_dict = graph.rooms

#write the results to file, for longevity.
with open("graph.txt", mode='r+') as fd:
    fd.write(str(directions))

with open("rooms.txt", mode="r+") as rm:
    for i in rooms_dict:
        rm.write(f"{rooms_dict[i]} \n")

print(f"total time: {time.time() - start}")