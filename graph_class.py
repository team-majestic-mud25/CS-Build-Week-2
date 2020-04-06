from util import Queue, Stack
from ast import literal_eval
import requests
import json
import time

api_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"
token = 'c9916272fa1e2737b1850164ddf88e43280ad09c' #TODO should move this to a env file.
headers = {'Authorization': f'Token {token}',
           'Content-Type': 'application/json'}

class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.connections = {} #dictionary of room connection objects stored by room id
        self.rooms = {} #dictionary of room response objects stored by room id

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.connections[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if self.connections.get(v1) == None or self.connections.get(v2) == None:
            raise IndexError(f"{v1} is not in the graph, bruh. try running add_vertex({v1} first.) ")
        self.connections[v1].add(v2)

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if self.connections.get(vertex_id) == None:
            raise IndexError(f"{vertex_id} is not in the graph, mah dood.")
        return self.connections[vertex_id]

    def dft_recursive(self, current_room, visited=None):
        """
        store each vertex in self.connections
        beginning from the initial room.
        TODO - pull move requests out to a method.
        TODO - skip previously explored rooms.
        """
        print("DFT CALLED")
        #BASE CASE: when we've explored every adjacent room, return up the chain
        if current_room['room_id'] in self.connections:
            if len(current_room['exits']) == len(self.connections[current_room['room_id']]) and current_room['room_id'] in visited:
                return

        #first pass? if so, instantiate the set
        if not visited:
            visited=set()
        visited.add(current_room['room_id']) #add first room
            
        #move to all available neighbors, filling out connections
        for direction in current_room['exits']:
            
            #move request to side room, 
            payload = {f'direction': f'{direction}'}

            # check_bonus(self, current_room, exits[i], directions, payload)
            if current_room['room_id'] in self.connections:
                if direction in self.connections[current_room['room_id']]:
                    payload['next_room_id'] = f"{self.connections[current_room['room_id']][direction]}"
            else: 
                self.connections[current_room['room_id']] = {}

            r = requests.post(url=f"{api_url}move/", headers=headers, json=payload)
            print(r.status_code, r)
            side_room = r.json()
            self.connections[current_room['room_id']][direction] = side_room['room_id']
            print(f'moved to side room: {side_room["room_id"]}\nwaiting {side_room["cooldown"]}secs\n')
            time.sleep(side_room['cooldown'])

            if side_room['room_id'] not in visited:
                self.dft_recursive(side_room, visited)

            if side_room['room_id'] not in self.rooms:
                #store info - change connections, and add room to self.rooms
                self.rooms[side_room['room_id']] = side_room

            if side_room['room_id'] not in self.connections:
                self.connections[side_room['room_id']] = {}
            
            opposite_move = ""

            #adds opposite direction to self.connections if it doesnt already exist
            if direction == "n":
                opposite_move = "s"
                if opposite_move not in self.connections[side_room['room_id']]:
                    self.connections[side_room['room_id']][opposite_move] = current_room['room_id']
            if direction == "s":
                opposite_move = "n"
                if opposite_move not in self.connections[side_room['room_id']]:
                    self.connections[side_room['room_id']][opposite_move] = current_room['room_id']
            if direction == "e":
                opposite_move = "w"
                if opposite_move not in self.connections[side_room['room_id']]:
                    self.connections[side_room['room_id']][opposite_move] = current_room['room_id']
            if direction == "w":
                opposite_move = "e"
                if opposite_move not in self.connections[side_room['room_id']]:
                    self.connections[side_room['room_id']][opposite_move] = current_room['room_id']

            #move request back to current_room (with bonus)
            payload = {f'direction': f'{opposite_move}'}
            r = requests.post(url=f"{api_url}move/", headers=headers, json=payload)
            print(r.status_code)
            main_again= r.json()
            print(f"back in main room: {main_again['room_id']}\ncooldown {main_again['cooldown']}secs\n")
            time.sleep(main_again['cooldown'])

    def bfs(self, starting_room_id, destination_room_id):
        """
        Return a list containing the shortest path from
        starting_room_id to destination_room_id 
        """

        with open("graph.txt", mode='r+') as dd:
            connections = literal_eval(dd.read())
        self.connections = connections

        #create a way to track visted vertices.
        visited = set()
        
        #create a way to track the overall path.
        current_path = []

        #instantiate queue and define starting vertex. 
        q = Queue()
        q.enqueue((starting_room_id, current_path))

        while q.size() > 0:
            #pop current node off the queue and add it to visited.
            toople = q.dequeue()
            current_node = toople[0]
            path_so_far = toople[1]
            visited.add(current_node)

            #are we done searching?
            if current_node == destination_room_id:
                return path_so_far[:]

            #if not done searching,
            else:
                #check the node for neighbors.
                for i in self.connections[current_node]:
                    path = path_so_far[:]
                    #enqueue the neighbors, assuming we havent visited
                    if self.connections[current_node][i] not in visited:
                        path.append(i)
                        q.enqueue((self.connections[current_node][i], path))