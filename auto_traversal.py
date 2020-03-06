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
print(f"{response.status_code}")
initial_room = response.json() #converts to object/dict.
print(f"initial room = {initial_room['room_id']}\n")
time.sleep(initial_room['cooldown']) #avoid movement penalty.
stack.append(initial_room) #to start the while loop.

previous_room = None #room_id of prev room for quick lookup.
last_move = None #last move, will be appended to path or used to reverse a current move.
last_move_opposite = None #solely for reversing a move.

while len(visited) < 500:

    current_room=stack.pop()
    print(f"current room: {current_room}, top of the while loop")
    print(f"{visited}")

    if previous_room != None: #any pass other than the first
        print(f"previous_room = {previous_room}")
        
        if len(rooms_dict[current_room['room_id']]['messages']) < 1: #if there are no room messages (this only happens on /init/ calls)
            move = last_move

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
            print(f"\ndirections dictionary = {directions}\n") 

    rooms_dict[current_room['room_id']] = current_room #cache the room data
    print(f" \n\n ROOMS_DICT: \n {rooms_dict} \n\n")

    exits = current_room['exits']
    opposites = []

    if current_room['room_id'] not in visited:
        for i in range(len(exits)):
            print(f"iteration number: {i+1}")

            #generate opposites
            if exits[i] == "s":
                opposites.append("n")
            if exits[i] == "n":
                opposites.append("s")
            if exits[i] == "e":
                opposites.append('w')
            if exits[i] == "w":
                opposites.append('e') 
    
            print(f"current_id: {current_room['room_id']}")
            print(f"previous_id: {previous_room}")
            print(f"exits: {exits}")
            print(f"opposites: {opposites}\n")

            previous_room = current_room['room_id'] #adjusting value for the next loop
            
    ######################################################################################
    #i will need to simplify and adjust everything below this to get a working traversal 
    ######################################################################################

            #move to a side room and wait
            payload = {f'direction': f'{exits[i]}'} 
            print(f"\n############### moving to side room => {payload}")
            last_move = exits[i]
            r = requests.post(url=f"{api_url}move/", headers=headers, json=payload)
            yet_another_room = r.json()
            print(f"id: {yet_another_room['room_id']}")
            print(f"waiting {yet_another_room['cooldown']} seconds\n")
            time.sleep(yet_another_room['cooldown'])
            
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

            #move back
            payload = {'direction':f'{opposites[i]}', 'next_room_id':f'{previous_room}'}
            print(f"\n############ moving back --> {payload}")
            post = requests.post(f"{api_url}move/", headers=headers, json=payload)
            print(f"back in main room, id: {post.json()['room_id']}")
            room_num = post.json()['room_id']
            rooms_dict[room_num] = post.json()
            last_move = opposites[i]
            print(f"waiting {post.json()['cooldown']} seconds\n")
            time.sleep(post.json()['cooldown'])

        visited.add(previous_room)
        print(f"added main room to visted. \n  visited= {visited}\nmoving to next room...\n")

    #move to the next room to be evaluated
    rand = random.randint(0, (len(exits)-1)) #chooses random index
    rand_selection = exits[rand] #seee?
    last_data = {'direction':f'{rand_selection}'} #where we're about to move
    last_move = rand_selection #update last_move, so we can get back
    traversal_path.append(last_move)
    
    move_back = requests.post(f"{api_url}move/", headers=headers, json=last_data)
    print(f"moved to room {move_back.json()['room_id']}")
    print(f"waiting {move_back.json()['cooldown']} seconds\n")
    time.sleep(move_back.json()['cooldown'])
    next_room = move_back.json()
    
    #if exits are greater than 1 -> we move it to the stack
    if next_room["room_id"] not in visited and len(next_room['exits']) > 1:
        stack.append(next_room)

    #if less than one, we've just explored it.
    if next_room["room_id"] not in visited and len(next_room['exits']) < 2: 
        visited.add(next_room["room_id"])
        print(f"only one door, updated visited to {visited}")

    #if it has already been evaluated 
    if next_room["room_id"] in visited:
        print(f"hallway, backing out.")
        #room is already explored 
        print_var = next_room["room_id"]
        print(f"exits to be reversed = {next_room['exits']}")
        way_back = None
        if rand_selection == "s":
            way_back = "n"
        if rand_selection == "n":
            way_back = "s" 
        if rand_selection == "e":
            way_back = "w"
        if rand_selection == "w":
            way_back = "e"
        print(f'just before moving back to main room. direction outta here = {way_back}\n')

        #move back to initial/current_room (the one popped off the stack)
        data = {'direction':f'{way_back}', 'next_room_id':f"{previous_room}"}
        step = requests.post(f"{api_url}move/", headers=headers, json=data)
        next_move = step.json()
        print(f"moved to room {previous_room}")
        print(f"waiting {next_move['cooldown']} seconds")
        print(f"^^^if this is 20, you messed up.^^^")
        time.sleep(next_move['cooldown'])

        #choose a new room to explore
        new_rand = random.randint(0, (len(next_move['exits'])-1))
        other_data = {'direction':f"{exits[rand]}"}
        step_2 = requests.post(f"{api_url}move/", headers=headers, json=other_data)
        next_try = step_2.json()

        #add the new room to the stack and rest
        stack.append(next_try)
        print(f"\nchose to explore new room, id: {next_try['room_id']}")
        print(f"waiting {next_try['cooldown']} seconds\n")
        time.sleep(next_try['cooldown'])
        
    print(f"bottom of while loop\ndirections: {directions}\nbottom of while loop")

#after the while loop - write the resulting graph to a file.
with open("graph.txt", mode='r+') as fd:
    fd.write(str(directions))

with open("rooms.txt", mode="r+") as rm:
    for i in rooms_dict:
        rm.write(f"{rooms_dict[i]} \n")