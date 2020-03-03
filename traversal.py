import requests
import json
import time
import json
from stack import Stack

# what the response from the server looks like.
# i think i'll want to store all room details in a hashtable where the key is the room number and the value is the following room object

# rooms_dict = {
# 0: {
#   "room_id": 0, 
#   "title": "A brightly lit room", 
#   "description": "You are standing in the center of a brightly lit room. You notice a shop to the west and exits to the north, south and east.", 
#   "coordinates": "(60,60)", 
#   "elevation": 0,
#   "terrain": "NORMAL", 
#   "players": ["User 20500", "User 20502", "brady - cs24", "User 20503", "User 20471", "User 20509", "User 20510", "User 20514", "User 20483", "User 20485", "User 20516", "User 20517", "User 20490", "User 20519", "User 20491", "User 20521", "User 20495", "User 20496", "User 20528", "User 20529", "User 20533", "User 20534", "User 20581", "User 20540", "User 20546", "User 20547", "Jason_Prince", "User 20553", "User 20556", "User 20559", "User 20560", "User 20563", "User 20565", "User 20566", "lavon_mejia", "User 20568", "[George H]", "Khaled>", "User 20570", "Sean Wu", "User 20576", "User 20577", "DRK"], 
#   "items": [], 
#   "exits": ["n", "s", "e", "w"], 
#   "cooldown": 15.0, "errors": [], 
#   "messages": ["You have walked south."]
#   }, 
# 10: {
#   "room_id": 10, 
#   "title": "A misty room", 
#   "description": "You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.", 
#   "coordinates": "(60,61)", 
#   "elevation": 0, 
#   "terrain": "NORMAL", 
#   "players": ["User 20481"], 
#   "items": [], 
#   "exits": ["n", "s", "w"], 
#   "cooldown": 15.0, 
#   "errors": [], 
#   "messages": ["You have walked north."]
#   },
# }
rooms_dict = dict()

# dictionary that contains dictionaries of each available cardinal direction, key is room number.
# ex directions = {0: {'n':'10', 's':'?', 'e':'?', 'w':'?'}, 
#               10: {'n':'?', 's':'0', 'e':'?', 'w':'?'},}
directions = dict()

visited = set()

#waits the correct number of seconds before making the next call.
def wait(current_dict):
    movement_message = None
    #splits the second message in the messages list into a list of words
    #if the bonus is present it will be ["Wise", "explorer", etc]
    if len(current_dict[previous_room]['messages']) >= 1:
        movement_message = current_dict[previous_room]['messages'][1].split()
    #evaluates first word to see if "Wise"
    if movement_message and movement_message[0] == "Wise":
        time.sleep(current_dict[previous_room]['cooldown']/2 +1) #takes advantage of bonus
    else:
        time.sleep(current_dict[previous_room]['cooldown'] +1) #standard cooldown

#makes init request, saves the first return object to initial_room
#    translates this request -> curl -X GET -H 'Authorization: Token 5ef1d5be3070afa793bd9dae10aa65a48e224264' -H "Content-Type: application/json" https://lambda-treasure-hunt.herokuapp.com/api/adv/init/
api_url = "https://lambda-treasure-hunt.herokuapp.com/api/adv/"
token = 'fa4e18d45e95555aa7e8a9cda009274fab0c316e'
init = requests.get(f"{api_url}init/")
headers = {'Authorization': 'Token '+token,
           'Content-Type': 'application/json'}
           
response = requests.get(url=f"{api_url}init/", headers=headers)
initial_room = response.json()
print("INITIAL ROOM", initial_room["room_id"])
visited.add(initial_room['room_id']) #ADDS ROOM ID TO THE VISITED DICT
print("VISITED", visited)


#adds that first room to the stack,
stack = Stack()
stack.push(initial_room)

previous_room = None
#while the stack is not empty
while stack.len() > 0:
    #pop a room off the stack, 
    current_room = stack.pop()
    print(f"CURRENT ROOOOOOOOMMMMMMMMM {current_room}")
    #if previous room is not None:
    if previous_room != None:
    #   if it's not our first move evaluate messages[0] within the rooms_dict[previous_room]->
        print("PRINTING", rooms_dict[previous_room])
        movement_message = rooms_dict[previous_room].messages[0]
        print
          #split the string, grab the last index, that should match "north", "south", "east", or "west"
        d = movement_message.split(" ")
        if (d[-1]):
            move = d[-1]
            if move == "north":
                directions["previous_room"]['n'] = previous_room
            elif move == "south":
                directions["previous_room"]['s'] = previous_room
            elif move == "west":
                directions["previous_room"]['w'] = previous_room
            elif move == "east":
                directions["previous_room"]['e'] = previous_room
        else:
            print("NO MESSAGES HERE, TRY AGAIN")
        
    previous_room = current_room['room_id'] #adjusting value for the next loop

    if previous_room not in visited: #check if we've added this to the visited set
        visited.add(previous_room['room_id'])
    
    rooms_dict[previous_room] = current_room #cache the room data
    wait(rooms_dict)

    print(f" \n\n ROOMS:{rooms_dict} \n\n")

    #adds all the adjacent rooms to the stack
    exits = rooms_dict[previous_room]['exits']
    print("EXITSSSS", exits)
    opposites = []

    for i in range(len(exits)):
        print(f"iteration number: {i+1}")
        #generate opposites
        if exits[i] == "s":
            opposites.append("n")
        elif exits[i] == "n":
            print(f"NORTH HIT")
            opposites.append("s")
        elif exits[i] == "e":
            opposites.append('w')
        elif exits[i] == "w":
            opposites.append('e')
        print(f"exits: {exits}")
        print(f"opposites: {opposites}")

        #move to room and push that room to the stack
        payload = {f'direction': f'{exits[i]}'} 
        print(f"about to move => {payload}")
        time.sleep(1)
        yet_another_room = requests.post(url=f"{api_url}move/", headers=headers, json=payload)
        print(f"{yet_another_room.status_code} {yet_another_room.reason} \n response cooldown: {yet_another_room.json()['cooldown']}\n will be saved into the new_room var: {yet_another_room.json()}")
        time.sleep(yet_another_room.json()['cooldown'])

        #push the variable onto the stack 
        new_room = yet_another_room.json()
        room_num = new_room['room_id']
        print(f"**************contents of rooms_dict, unchanged****************\n{rooms_dict}")        

        if room_num not in visited:
            rooms_dict[room_num] = new_room
            visited.add(new_room['room_id'])

        # print(f"HECK {new_room}")
        # print("HECKIN HECK, ", rooms_dict[room_id])
        
        if new_room == rooms_dict[room_num]:
            continue
        else:
            print(f"NEW ROOM: \n {new_room}")
            stack.push(new_room)

        #move back
        payload = {'direction':f'{opposites[i]}'}
        post = requests.post(f"{api_url}move/", headers=headers, json=payload)
        time.sleep(post.json()['cooldown'])
        #wait again
        wait(rooms_dict)

    #move to the next room to be evaluated
    last_data = {'direction':f'{opposites[-1]}'}
    move_back = requests.post(f"{api_url}move/", headers=headers, json=last_data)
    time.sleep(move_back.json()['cooldown'])

#after the while loop - write the resulting graph to a file.
with open("graph.txt", 'wb') as fd:
    fd.write(f"{rooms_dict}" + "\n" + f"{directions}")
