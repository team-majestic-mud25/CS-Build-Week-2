import json
import ast

connections = {}#dictionary of dictionaries containing n,s,e,w connections, so
rooms = {}#dictionary of room-id keys that have a dictionary of the corresponding room's connecting vertices

#open up the file and add all connections to connections
with open("graph.txt", mode="r+") as gr:
    connections = ast.literal_eval(gr.read())
    print(connections)
#do the same for rooms
with open("rooms.txt", mode ="r") as rm:
    for line in rm:
        stringy = line.strip('\n') #strips out newline and white space
        force_dict = ast.literal_eval(stringy) 
        dict_key = force_dict['room_id']
        rooms[dict_key] = force_dict

#150x150 grid should leave enough space
grid_row = ["   "] * 250 #mark a spot a room COULD be.
grid = []

#generate map (sans room numbers)
for x in range(250):
    grid.append(grid_row[:]) #pass by value to instantiate the grid

#add coordinate tuples to appropriate connection

for i in connections:  #each room evaluated should reset all vars, i is a room ID in connections
    x=None
    y=None
    room = i
    arr = []
    
    connections[room]["coordinates"] = rooms[room]['coordinates'] #adjust entries by index, for rooms, which should correspond to coordinates.

    #connections[room]["coordinates"] is a stringified tuple '(68,47)'
    arr = connections[room]["coordinates"].split(",") # ["(68", "47)"]
    
    #cast to int after pulling out parens
    x = int(arr[0][1:]) #highest possible X is 73
    y = int(arr[1][:2]) #highest possible Y is 60
    connections[room]["coordinates"] = (x, y) #basically just to force the type to int for any future fiddling.

    #multiplying by 2 ensures only even columns get room #s
    y_index = y*2 
    x_index = x*2

    #print formatting. ensures a room always has three chars/spaces accounted for.
    new_string = ""
    if len(str(room)) == 3:
        new_string = str(room)
    if len(str(room)) == 2:
        new_string = " " + str(room)
    if len(str(room)) == 1:
        new_string = " " + str(room) + " "
    grid[y_index][x_index] = new_string 
    

    if 'e' in connections[room]:
        grid[y_index][(x_index)+1] = "---" #odd X index east
    if 'w' in connections[room]:
        grid[y_index][(x_index)-1] = "---" #odd X index west
    if 'n' in connections[room]:
        grid[(y_index)+1][x_index] = " | " #odd Y index north
    if 's' in connections[room]:
        grid[(y_index)-1][x_index] = " | " #odd Y index south

#need to trim the map, since we generated an arbitrarily large one
first = 0
last = 0
for row in grid:
    #check how many spaces to shave off
    count = 0
    row_index = 0
    searching = True
    while searching:
        if count >= len(row)-1: 
            searching = False
        if row[count] != "   ":
            searching = False
        else:
            count+= 1

    if first == 0:
        first = count
    else:
        if count < first:
            first = count

    #do the same check, except from the end.
    end_index = len(row)-1
    end_count = 0 #length from room to end index of the array
    index_not_found = True
    while index_not_found:
        if end_index < 0:
            index_not_found = False
        if row[end_index] != "   ":
            index_not_found = False
        else:
            end_index-= 1
            end_count+= 1

    if last == 0:
        last = end_index
    else:
        if end_index > last:
            last = end_index
for row in grid:
    y_coord = row[first:last+1]
    grid[grid.index(row)] = y_coord

kill_it=[] #gathering list of grids to remove. is there a faster way to check for arrays of like items?
for r in range(len(grid)):
    keep = False
    for i in range(len(grid[r])):
        if grid[r][i] != "   ":
            keep = True
    if keep == False:
        kill_it.append(grid[r])
for item in kill_it:        
    grid.remove(item)

grid.reverse() #ensures the grid doesnt print out mirrored n/s 
    #should check if this is faster than O(n) -> my guess is o(log(n))

with open("ascii_map.txt", mode="r+") as am:
    for row in grid:
        print_string = ""
        for item in row:
            print_string+= str(item)
        am.write(print_string + "\n")

        print(print_string)
