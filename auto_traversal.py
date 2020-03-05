import requests
import json
import time
import random

rooms_dict = dict() #dictionary of room objects
directions = dict() #{0: {'n':'10', 's':'?', 'e':'?', 'w':'?'}, 10: {'n':'?', 's':'0', 'e':'?', 'w':'?'}, etc}
visited = set()  #tracks if we've stepped foot in a room.
traversal_path = [] #path taken from last root node
stack = [] #to track untraveled rooms

# makes init request, saves the first return object to initial_room
api_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"
token = 'c9916272fa1e2737b1850164ddf88e43280ad09c'
headers = {'Authorization': f'Token {token}',
           'Content-Type': 'application/json'}
           
response = requests.get(url=f"{api_url}init/", headers=headers)

initial_room = response.json() #converts to object/dict.
time.sleep(initial_room['cooldown']) #avoid movement penalty.
visited.add(initial_room['room_id']) #we've been here.
stack.append(initial_room) #to start the while loop.

previous_room = None #room_id of prev room for quick lookup.
last_move = None #last move, will be appended to path or used to reverse a current move.
last_move_opposite = None #solely for reversing a move.

while len(visited) < 500:

    current_room=stack.pop()
    print(f"current room: {current_room}")
    print(f"{visited}")

    if previous_room != None: #any pass other than the first
        print(f"previous_room = {previous_room}")
        
        #should i be doing the below on current room?
        if len(rooms_dict[current_room['room_id']]['messages']) < 1: #if there are no room messages (this only happens on /init/ calls)
            move = last_move
            print(f"last_move = {last_move}")

            if previous_room in directions:
                directions[current_room['room_id']][last_move] = current_room
                print(f"new value added to directions = {directions[current_room['room_id']]}")
            else:
                directions[current_room['room_id']] = {}
                print(f"directions entry instantiated = {directions[current_room['room_id']]}")
                directions[current_room['room_id']][last_move] = current_room
                print(f"new value added to directions = {directions[current_room['room_id']]}")
        else: #you successfully moved.
            movement_message = rooms_dict[current_room['room_id']]['messages'][0]
            print(f"message in rooms_dict[current_room['room_id']] = {movement_message}")
            
            d = movement_message.split(" ") #split the string
            move = d[-1] #grab the last index
            if move == "north":
                directions[previous_room]['n'] = previous_room
            elif move == "south":
                directions[previous_room]['s'] = previous_room
            elif move == "west":
                directions[previous_room]['w'] = previous_room
            elif move == "east":
                directions[previous_room]['e'] = previous_room
            print(f"directions dictionary = {directions}\n") 

    rooms_dict[current_room['room_id']] = current_room #cache the room data
    print(f" \n\n ROOMS_DICT: \n {rooms_dict} \n\n")

    exits = current_room['exits']
    opposites = []
    for i in range(len(exits)):
        print(f"current path traveled = {traversal_path}")
        print(f"iteration number: {i+1}")

        #generate opposites
        if exits[i] == "s":
            opposites.append("n")
        elif exits[i] == "n":
            opposites.append("s")
        elif exits[i] == "e":
            opposites.append('w')
        elif exits[i] == "w":
            opposites.append('e') 
 
        print(f"current_id: {current_room['room_id']}")
        print(f"previous_id: {previous_room}")
        print(f"exits: {exits}")
        print(f"opposites: {opposites}\n")

        previous_room = current_room['room_id']
        print(f"changed previous room to: {previous_room}") #adjusting value for the next loop
        
######################################################################################
#i will need to simplify and adjust everything below this to get a working traversal 
######################################################################################

        #move to room and wait
        payload = {f'direction': f'{exits[i]}'} 
        print(f"about to move => {payload}")
        last_move = exits[i]
        r = requests.post(url=f"{api_url}move/", headers=headers, json=payload)
        yet_another_room = r.json()
        print(f"waiting {yet_another_room['cooldown']} seconds")
        time.sleep(yet_another_room['cooldown'])
        print(f"\n{r.status_code} {r.reason} \n response cooldown: {yet_another_room['cooldown']}\n new_room: \n {yet_another_room}")
        
        #add main room information to directions
        if current_room["room_id"] in directions:
            directions[current_room["room_id"]][exits[i]] = yet_another_room["room_id"]
        else:
            directions[current_room["room_id"]] = {}
            directions[current_room["room_id"]][exits[i]] = yet_another_room["room_id"]

        #add side room information to directions
        if yet_another_room["room_id"] in directions:
            directions[yet_another_room["room_id"]][opposites[i]] = current_room["room_id"]
        else:
            directions[yet_another_room["room_id"]] = {}
            directions[yet_another_room["room_id"]][opposites[i]] = current_room["room_id"]

        #push the new_room onto the stack
        new_room = yet_another_room
        room_num = new_room['room_id']
        rooms_dict[room_num] = new_room
        print(f"\n rooms_dict post move \n {rooms_dict} \n")

        #move back
        payload = {'direction':f'{opposites[i]}', 'next_room_id':f'{previous_room}'}
        print(f"\nmoving back --> {payload}")
        post = requests.post(f"{api_url}move/", headers=headers, json=payload)
        print(f"\nreturned to main room \nresponse= {post.json()}\n")
        room_num = post.json()['room_id']
        rooms_dict[room_num] = post.json()
        last_move = opposites[i]
        print(f"waiting {post.json()['cooldown']} seconds")
        time.sleep(post.json()['cooldown'])

    visited.add(previous_room)
    print(f"added previous room to visted. \n visited= {visited}")

    #move to the next room to be evaluated
    last_data = {'direction':f'{exits[-1]}'}
    last_move = exits[-1]
    traversal_path.append(exits[-1])

    move_back = requests.post(f"{api_url}move/", headers=headers, json=last_data)
    print(f"waiting {move_back.json()['cooldown']} seconds")
    time.sleep(move_back.json()['cooldown'])
    next_room = move_back.json()
    
    #if exits are greater than 1 -> we move it to the stack
    if next_room["room_id"] not in visited and len(next_room['exits']) > 1:
        stack.append(next_room)

    #if it has already been evaluated (it's in visited OR exits are less than 2), dont do that.
    elif len(next_room['exits']) < 2:

        #room is already explored (one exit means we just came from the only door)
        visited.add(next_room["room_id"])
        print_var = next_room["room_id"]
        print(f"added room {print_var} to visited \nvisited: {visited}\n")
        
        #move back to initial/current_room (the one popped off the stack)
        data = {'direction':f'{opposites[-1]}', 'next_room_id':f"{previous_room}"}
        step = requests.post(f"{api_url}move/", headers=headers, json=data)
        next_move = step.json()
        print(f"waiting {next_move['cooldown']} seconds")
        time.sleep(next_move['cooldown'])

        #choose a new room to explore
        other_data = {'direction':f"{exits[-2]}", 'next_room_id':f"{previous_room}"}
        step_2 = requests.post(f"{api_url}move/", headers=headers, json=other_data)
        next_try = step_2.json()

        #add the new room to the stack and rest
        stack.append(next_try)
        print(f"waiting {next_try['cooldown']} seconds")
        time.sleep(next_try['cooldown'])
    
    elif next_room["room_id"] in visited and len(next_room['exits']) > 1:

        #move back to initial/current_room (the one popped off the stack)
        data = {'direction':f'{opposites[-1]}', 'next_room_id':f"{previous_room}"}
        step = requests.post(f"{api_url}move/", headers=headers, json=data)
        next_move = step.json()
        print(f"waiting {next_move['cooldown']} seconds")
        time.sleep(next_move['cooldown'])

        #randomly choose a new room to explore
        rand = random.randint(0, (len(next_move['exits'])-1))
        print("randomly selected index", rand)
        print("randomly selected move", next_move['exits'][rand])
        other_data = {'direction':f"{next_move['exits'][rand]}"}
        step_2 = requests.post(f"{api_url}move/", headers=headers, json=other_data)
        next_try = step_2.json()
        
        #add the new room to the stack and rest
        stack.append(next_try)
        print(f"waiting {next_try['cooldown']} seconds")
        time.sleep(next_try['cooldown'])
    print(f"\ndirections: {directions}\n")

#after the while loop - write the resulting graph to a file.
with open("graph.txt", mode='r+') as fd:
    fd.write(str(directions))

with open("rooms.txt", mode="r+") as rm:
    for i in rooms_dict:
        rm.write(f"{rooms_dict[i]} \n")