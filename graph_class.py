from util import Queue, Stack
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
        TODO - pull bonus check out to a method.
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

            # check_bonus(current_room, exits[i], directions, payload)
            if current_room['room_id'] in self.connections:
                if direction in self.connections[current_room['room_id']]:
                    payload['next_room_id'] = f"{self.connections[current_room['room_id']][direction]}"
            else: 
                self.connections[current_room['room_id']] = {}

            r = requests.post(url=f"{api_url}move/", headers=headers, json=payload)
            print(r.status_code, r)
            side_room = r.json()
            self.connections[current_room['room_id']][direction] = side_room['room_id']
            print(f'moved to side room: {side_room["room_id"]}\nwaiting {side_room["cooldown"]}secs')
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
            print(f"back in main room: {main_again['room_id']}\ncooldown {main_again['cooldown']}secs")
            time.sleep(main_again['cooldown'])

    #TODO implement a bfs for finding shortest path.
    # def bfs(self, starting_vertex, destination_vertex):
    #     """
    #     Return a list containing the shortest path from
    #     starting_vertex to destination_vertex in
    #     breath-first order.
    #     """
    #      #instantiate queue and define starting vertex. 
    #     q = Queue()
    #     q.enqueue(starting_vertex)
    #     #create a way to track visted vertices.
    #     visited = []
    #     #create a way to track the overall path
    #     current_path = {
    #         starting_vertex: '1',
    #     }
    #     print(f"breadth first search")
    #     while q.size() > 0:
    #         #pop current node off the queue and add it to visited
    #         current_node = q.dequeue()
    #         #are we done searching?
    #         if current_node == destination_vertex:
    #             #start with an empty string
    #             path = f''
    #             #loop through the current path and generate overall path
    #             while current_path.get(current_node) is not '1':
    #                 path = f'{current_node} {path}'
    #                 current_node = current_path.get(current_node)
    #             #return the result
    #             return f'{starting_vertex} {path}'
    #         #if not done searching,
    #         else:
    #             #check the node for neighbors.
    #             for i in self.get_neighbors(current_node):
    #                 #enqueue the neighbors, assuming we havent visited
    #                 if i not in visited:
    #                     q.enqueue(i)
    #                     visited.append(i)
    #                 #if you havent reached the end or the target, mark your progress
    #                 if not current_path.get(i):
    #                     current_path[i] = current_node