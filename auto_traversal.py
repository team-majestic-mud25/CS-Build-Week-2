import requests
import json
import time
import random

#done. #TODO implement bonuses for every move if the room is in the directions cache. 
#done. #TODO implement skipping of four-corner searches for every room that is in the visited set. 
#done. #TODO write a script that takes the result of the traversal and generates an ascii map representation of the graph. 

#TODO change this traversal from a "random selection" traversal to either a depth first, or breadth first traversal.
#TODO once traversal is complete, create a function that returns the shortest path from current_room to target_room.

#rooms_dict, directions and visited are hard coded with rescued values from prints on a run that crashed due to a server 503

#dictionary of room objects
rooms_dict = {
    112: {'room_id': 112, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,54)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    141: {'room_id': 141, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,53)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    140: {'room_id': 140, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(66,54)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['small treasure', 'amazing treasure', 'great treasure'], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    100: {'room_id': 100, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,54)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    106: {'room_id': 106, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,53)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    68: {'room_id': 68, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,54)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    111: {'room_id': 111, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,52)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['User 20694'], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    135: {'room_id': 135, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,53)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    150: {'room_id': 150, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,52)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    166: {'room_id': 166, 'title': 'Mt. Holloway', 'description': 'You are at the base of a large, looming mountain.', 'coordinates': '(62,52)', 'elevation': 1, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    198: {'room_id': 198, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,51)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    117: {'room_id': 117, 'title': 'Mt. Holloway', 'description': 'You are on the side of a steep incline.', 'coordinates': '(61,52)', 'elevation': 2, 'terrain': 'MOUNTAIN', 'players': ['User 20663'], 'items': [], 'exits': ['n', 's', 'e', 'w'], 'cooldown': 20.0, 'errors': [], 'messages': ['You have walked west.', 'Uphill Penalty: 5s CD']}, 
    367: {'room_id': 367, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,51)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    158: {'room_id': 158, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,52)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    52: {'room_id': 52, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,55)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    35: {'room_id': 35, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,56)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    75: {'room_id': 75, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,55)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    85: {'room_id': 85, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,55)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure'], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    156: {'room_id': 156, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(66,53)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    168: {'room_id': 168, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(66,52)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    164: {'room_id': 164, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(67,53)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['raj kamali'], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    217: {'room_id': 217, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(67,54)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    298: {'room_id': 298, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(68,53)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    247: {'room_id': 247, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(68,54)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    324: {'room_id': 324, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(68,52)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['harliquinn'], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    340: {'room_id': 340, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(67,52)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    261: {'room_id': 261, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(69,54)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    277: {'room_id': 277, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(69,53)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    322: {'room_id': 322, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(70,54)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    382: {'room_id': 382, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(70,55)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['emmargherd'], 'items': [], 'exits': ['s', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    435: {'room_id': 435, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(71,54)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure'], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    388: {'room_id': 388, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(71,55)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    477: {'room_id': 477, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(72,55)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    483: {'room_id': 483, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(73,55)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    167: {'room_id': 167, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,51)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['josh_fowlkes'], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    262: {'room_id': 262, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['mary'], 'items': ['spectacular treasure'], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    260: {'room_id': 260, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(66,51)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'amazing treasure'], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    370: {'room_id': 370, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,49)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    358: {'room_id': 358, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(66,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['spectacular treasure', 'shiny treasure', 'great treasure'], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    401: {'room_id': 401, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(67,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure', 'great treasure'], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    434: {'room_id': 434, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,48)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    407: {'room_id': 407, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(66,49)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    496: {'room_id': 496, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(66,48)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    154: {'room_id': 154, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(66,55)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    193: {'room_id': 193, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(67,55)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    251: {'room_id': 251, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(68,55)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    315: {'room_id': 315, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(69,55)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    34: {'room_id': 34, 'title': 'Mt. Holloway', 'description': 'You are at the base of a large, looming mountain.', 'coordinates': '(62,56)', 'elevation': 1, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 20.0, 'errors': [], 'messages': ['You have walked north.', 'Uphill Penalty: 5s CD']}, 
    14: {'room_id': 14, 'title': 'Mt. Holloway', 'description': 'You are on the side of a steep incline.', 'coordinates': '(62,57)', 'elevation': 2, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 20.0, 'errors': [], 'messages': ['You have walked north.', 'Uphill Penalty: 5s CD']}, 
    50: {'room_id': 50, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,55)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    37: {'room_id': 37, 'title': 'Mt. Holloway', 'description': 'You are at the base of a large, looming mountain.', 'coordinates': '(63,57)', 'elevation': 1, 'terrain': 'MOUNTAIN', 'players': [], 'items': ['spectacular treasure'], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    12: {'room_id': 12, 'title': 'Mt. Holloway', 'description': 'You are on the side of a steep incline.', 'coordinates': '(61,57)', 'elevation': 3, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['n', 's', 'e', 'w'], 'cooldown': 20.0, 'errors': [], 'messages': ['You have walked west.', 'Uphill Penalty: 5s CD']}, 
    9: {'room_id': 9, 'title': 'Mt. Holloway', 'description': 'You are on the side of a steep incline.', 'coordinates': '(61,58)', 'elevation': 2, 'terrain': 'MOUNTAIN', 'players': ['LindseyCason'], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 20.0, 'errors': [], 'messages': ['You have walked south.', 'Uphill Penalty: 5s CD']}, 
    18: {'room_id': 18, 'title': 'Mt. Holloway', 'description': 'You are on the side of a steep incline.', 'coordinates': '(61,56)', 'elevation': 4, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['n', 's', 'w'], 'cooldown': 20.0, 'errors': [], 'messages': ['You have walked south.', 'Uphill Penalty: 5s CD']}, 
    21: {'room_id': 21, 'title': 'Mt. Holloway', 'description': 'You are on the side of a steep incline.', 'coordinates': '(60,57)', 'elevation': 2, 'terrain': 'MOUNTAIN', 'players': [], 'items': ['great treasure'], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    3: {'room_id': 3, 'title': 'Mt. Holloway', 'description': 'You are at the base of a large, looming mountain.', 'coordinates': '(61,59)', 'elevation': 1, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 20.0, 'errors': [], 'messages': ['You have walked east.', 'Uphill Penalty: 5s CD']}, 
    11: {'room_id': 11, 'title': 'Mt. Holloway', 'description': 'You are at the base of a large, looming mountain.', 'coordinates': '(62,58)', 'elevation': 1, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    5: {'room_id': 5, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    2: {'room_id': 2, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(60,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    0: {'room_id': 0, 'title': 'A brightly lit room', 'description': 'You are standing in the center of a brightly lit room. You notice a shop to the west and exits to the north, south and east.', 'coordinates': '(60,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['JonathanJAM', 'STRAIGHT DmICK DEMERY', "['BUM']", 'chupacabra', 'Krishan the Quail', 'User 20657', '[Blake-G-CS25]', '[Jon-Solari]', 'User 20725', 'User 20723', 'User 20717', 'User 20711', 'User 20710', 'User 20705', 'User 20692', 'User 20688', 'User 20664'], 'items': [], 'exits': ['n', 's', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    6: {'room_id': 6, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(60,58)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    7: {'room_id': 7, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(59,58)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['am&a'], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    8: {'room_id': 8, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(59,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    56: {'room_id': 56, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(58,58)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    16: {'room_id': 16, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(58,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    58: {'room_id': 58, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(58,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    67: {'room_id': 67, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(57,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    162: {'room_id': 162, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(56,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    65: {'room_id': 65, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(57,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    74: {'room_id': 74, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(57,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    139: {'room_id': 139, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(56,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    188: {'room_id': 188, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(55,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    87: {'room_id': 87, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(57,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    161: {'room_id': 161, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(56,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    335: {'room_id': 335, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(54,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    366: {'room_id': 366, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(53,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    89: {'room_id': 89, 'title': 'Mt. Holloway', 'description': 'You are at the base of a large, looming mountain.', 'coordinates': '(62,54)', 'elevation': 1, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['n', 's'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    93: {'room_id': 93, 'title': 'Mt. Holloway', 'description': 'You are on the side of a steep incline.', 'coordinates': '(62,53)', 'elevation': 2, 'terrain': 'MOUNTAIN', 'players': [], 'items': ['spectacular treasure'], 'exits': ['n', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    108: {'room_id': 108, 'title': 'Mt. Holloway', 'description': 'You are on the side of a steep incline.', 'coordinates': '(61,53)', 'elevation': 3, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    239: {'room_id': 239, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    199: {'room_id': 199, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,51)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    230: {'room_id': 230, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    307: {'room_id': 307, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,49)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    297: {'room_id': 297, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    373: {'room_id': 373, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,48)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure'], 'exits': ['n', 's'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    371: {'room_id': 371, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,49)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'great treasure', 'great treasure'], 'exits': ['s', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    321: {'room_id': 321, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,49)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    475: {'room_id': 475, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,48)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    484: {'room_id': 484, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,47)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure', 'great treasure'], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    480: {'room_id': 480, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,47)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure'], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    413: {'room_id': 413, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,48)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure', 'amazing treasure', 'amazing treasure', 'spectacular treasure', 'amazing treasure', 'shiny treasure', 'amazing treasure'], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    244: {'room_id': 244, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(61,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure'], 'exits': ['n', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    131: {'room_id': 131, 'title': 'Mt. Holloway', 'description': 'You are at the base of a large, looming mountain.', 'coordinates': '(61,51)', 'elevation': 1, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['n', 's', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    138: {'room_id': 138, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(60,51)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    133: {'room_id': 133, 'title': 'Mt. Holloway', 'description': 'You are at the base of a large, looming mountain.', 'coordinates': '(60,52)', 'elevation': 1, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    211: {'room_id': 211, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(60,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure'], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    195: {'room_id': 195, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(59,51)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    78: {'room_id': 78, 'title': 'Mt. Holloway', 'description': 'You are on the side of a steep incline.', 'coordinates': '(61,54)', 'elevation': 4, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['n', 's'], 'cooldown': 20.0, 'errors': [], 'messages': ['You have walked north.', 'Uphill Penalty: 5s CD']}, 
    22: {'room_id': 22, 'title': 'The Peak of Mt. Holloway', 'description': 'You are standing at the zenith of Mt. Holloway. You see before you a holy shrine erected in the image of a magnificent winged deity.', 'coordinates': '(61,55)', 'elevation': 5, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['n', 's', 'w'], 'cooldown': 20.0, 'errors': [], 'messages': ['You have walked north.', 'Uphill Penalty: 5s CD']}, 
    323: {'room_id': 323, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(70,53)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    433: {'room_id': 433, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(71,53)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'amazing treasure', 'spectacular treasure'], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    349: {'room_id': 349, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(68,51)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    354: {'room_id': 354, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(69,52)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    173: {'room_id': 173, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(59,52)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 7.5, 'errors': [], 'messages': ['You have walked east.', 'Wise Explorer: -50% CD']}, 
    214: {'room_id': 214, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(58,52)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['[Ryan the Quail]'], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    352: {'room_id': 352, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(68,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    384: {'room_id': 384, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(69,51)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['[ HERO ]'], 'items': ['amazing treasure', 'great treasure'], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    356: {'room_id': 356, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(67,51)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'shiny treasure', 'amazing treasure', 'amazing treasure'], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    362: {'room_id': 362, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(68,49)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['The Chicken Killer', 'The Great and Knowledgeable Icculus'], 'items': [], 'exits': ['n', 's', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    485: {'room_id': 485, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(69,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'spectacular treasure', 'great treasure', 'spectacular treasure'], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    399: {'room_id': 399, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(68,48)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    463: {'room_id': 463, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(67,49)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    468: {'room_id': 468, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(67,48)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['daniel'], 'items': ['great treasure'], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    467: {'room_id': 467, 'title': "Pirate Ry's", 'description': "You see a sign before you that reads:\n\n'You have found Pirate Ry's. Send a `change_name` request and I'll change your identity to whatever you wish... for a price.'", 'coordinates': '(68,47)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['[TayBic]'], 'items': ['spectacular treasure'], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    194: {'room_id': 194, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(58,53)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    226: {'room_id': 226, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(57,52)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    300: {'room_id': 300, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(57,51)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'great treasure'], 'exits': ['n', 's', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    377: {'room_id': 377, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(57,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['[Heorhii Siburov]'], 'items': ['great treasure', 'shiny treasure', 'great treasure', 'amazing treasure', 'amazing treasure', 'great treasure', 'amazing treasure'], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    389: {'room_id': 389, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(56,51)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    36: {'room_id': 36, 'title': 'Mt. Holloway', 'description': 'You are on the side of a steep incline.', 'coordinates': '(60,55)', 'elevation': 4, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    25: {'room_id': 25, 'title': 'Mt. Holloway', 'description': 'You are on the side of a steep incline.', 'coordinates': '(60,56)', 'elevation': 3, 'terrain': 'MOUNTAIN', 'players': [], 'items': ['amazing treasure', 'amazing treasure', 'amazing treasure', 'great treasure', 'amazing treasure', 'amazing treasure', 'great treasure'], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    48: {'room_id': 48, 'title': 'Mt. Holloway', 'description': 'You are on the side of a steep incline.', 'coordinates': '(60,54)', 'elevation': 3, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['n', 's', 'w'], 'cooldown': 20.0, 'errors': [], 'messages': ['You have walked east.', 'Uphill Penalty: 5s CD']}, 
    60: {'room_id': 60, 'title': 'Mt. Holloway', 'description': 'You are on the side of a steep incline.', 'coordinates': '(59,55)', 'elevation': 3, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 20.0, 'errors': [], 'messages': ['You have walked south.', 'Uphill Penalty: 5s CD']}, 
    45: {'room_id': 45, 'title': 'Mt. Holloway', 'description': 'You are on the side of a steep incline.', 'coordinates': '(59,56)', 'elevation': 2, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['n', 's'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    70: {'room_id': 70, 'title': 'Mt. Holloway', 'description': 'You are on the side of a steep incline.', 'coordinates': '(58,55)', 'elevation': 2, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 20.0, 'errors': [], 'messages': ['You have walked north.', 'Uphill Penalty: 5s CD']}, 
    29: {'room_id': 29, 'title': 'Mt. Holloway', 'description': 'You are at the base of a large, looming mountain.', 'coordinates': '(59,57)', 'elevation': 1, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    49: {'room_id': 49, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(58,57)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    79: {'room_id': 79, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(58,56)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    136: {'room_id': 136, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(57,57)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['AceMouty'], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    163: {'room_id': 163, 'title': 'Mt. Holloway', 'description': 'You are at the base of a large, looming mountain.', 'coordinates': '(58,54)', 'elevation': 1, 'terrain': 'MOUNTAIN', 'players': [], 'items': ['great treasure', 'great treasure', 'great treasure', 'small treasure'], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    98: {'room_id': 98, 'title': 'Mt. Holloway', 'description': 'You are at the base of a large, looming mountain.', 'coordinates': '(57,55)', 'elevation': 1, 'terrain': 'MOUNTAIN', 'players': [], 'items': [], 'exits': ['n', 's', 'e', 'w'], 'cooldown': 20.0, 'errors': [], 'messages': ['You have walked south.', 'Uphill Penalty: 5s CD']}, 
    102: {'room_id': 102, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(57,56)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    126: {'room_id': 126, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(57,54)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    109: {'room_id': 109, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(56,55)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    185: {'room_id': 185, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(56,54)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    175: {'room_id': 175, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(55,55)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    129: {'room_id': 129, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(57,53)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    142: {'room_id': 142, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(56,56)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    159: {'room_id': 159, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(55,56)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    170: {'room_id': 170, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(56,53)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure', 'great treasure', 'amazing treasure', 'amazing treasure', 'great treasure'], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    148: {'room_id': 148, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(56,57)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    105: {'room_id': 105, 'title': 'Mt. Holloway', 'description': 'You are on the side of a steep incline.', 'coordinates': '(60,53)', 'elevation': 2, 'terrain': 'MOUNTAIN', 'players': ['Elan'], 'items': ['amazing treasure'], 'exits': ['n', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    149: {'room_id': 149, 'title': 'Mt. Holloway', 'description': 'You are on the side of a steep incline.', 'coordinates': '(59,54)', 'elevation': 2, 'terrain': 'MOUNTAIN', 'players': [], 'items': ['shiny treasure', 'great treasure'], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    202: {'room_id': 202, 'title': 'Mt. Holloway', 'description': 'You are at the base of a large, looming mountain.', 'coordinates': '(59,53)', 'elevation': 1, 'terrain': 'MOUNTAIN', 'players': [], 'items': ['amazing treasure'], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    420: {'room_id': 420, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(52,55)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['[treasure_hunter_x0x]'], 'items': ['amazing treasure', 'great treasure'], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    444: {'room_id': 444, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(52,54)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    213: {'room_id': 213, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(53,55)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    437: {'room_id': 437, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(51,55)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    179: {'room_id': 179, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(54,55)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    233: {'room_id': 233, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(54,54)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    238: {'room_id': 238, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(53,54)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    183: {'room_id': 183, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(55,54)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['theDABicorn'], 'items': [], 'exits': ['n', 's'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    229: {'room_id': 229, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(55,53)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    250: {'room_id': 250, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(55,52)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['[Cameron-Avacado]'], 'items': ['amazing treasure'], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    236: {'room_id': 236, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(54,53)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    294: {'room_id': 294, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(55,51)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    289: {'room_id': 289, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(56,52)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    334: {'room_id': 334, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(55,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    393: {'room_id': 393, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(55,49)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['small treasure', 'amazing treasure', 'great treasure', 'amazing treasure', 'amazing treasure', 'great treasure'], 'exits': ['n', 's'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    341: {'room_id': 341, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(56,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['sarah-riley'], 'items': ['amazing treasure'], 'exits': ['s', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    391: {'room_id': 391, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(54,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure'], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    449: {'room_id': 449, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(56,49)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure'], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    482: {'room_id': 482, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(55,48)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['spectacular treasure', 'shiny treasure', 'great treasure', 'spectacular treasure'], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    396: {'room_id': 396, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(54,49)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'amazing treasure'], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    428: {'room_id': 428, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(53,50)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['lccarrier'], 'items': ['amazing treasure', 'amazing treasure', 'amazing treasure', 'great treasure', 'spectacular treasure', 'amazing treasure', 'shiny treasure'], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    264: {'room_id': 264, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(54,52)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['Zach Young - SON OF TROY'], 'items': [], 'exits': ['n', 's', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    274: {'room_id': 274, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(54,51)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    273: {'room_id': 273, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(53,52)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    196: {'room_id': 196, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(54,56)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure'], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    222: {'room_id': 222, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(54,57)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    197: {'room_id': 197, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(53,56)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    305: {'room_id': 305, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(54,58)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['shiny treasure'], 'exits': ['n', 's'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    232: {'room_id': 232, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(53,57)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure'], 'exits': ['n', 's', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    276: {'room_id': 276, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(52,56)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    272: {'room_id': 272, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(53,58)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['ebcitron'], 'items': [], 'exits': ['n', 's'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    235: {'room_id': 235, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(52,57)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    295: {'room_id': 295, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(53,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    330: {'room_id': 330, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(52,58)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    355: {'room_id': 355, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(51,57)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    369: {'room_id': 369, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(52,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    383: {'room_id': 383, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(51,58)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure'], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    495: {'room_id': 495, 'title': 'The Transmogriphier', 'description': 'A strange machine stands in this room.  There is a large opening on the top.  A placard reads, "Test your luck!  One item and one Lambdacoin!"', 'coordinates': '(50,58)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['Min_Huang', '[Tai 510]', 'Juliette the Quail'], 'items': [], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    365: {'room_id': 365, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(54,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure'], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    400: {'room_id': 400, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(52,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    376: {'room_id': 376, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(51,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    419: {'room_id': 419, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(51,56)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure'], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    17: {'room_id': 17, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,58)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    24: {'room_id': 24, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure'], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    42: {'room_id': 42, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,58)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    44: {'room_id': 44, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'spectacular treasure', 'great treasure'], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    80: {'room_id': 80, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,57)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    118: {'room_id': 118, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,58)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'spectacular treasure'], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    137: {'room_id': 137, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(66,58)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    81: {'room_id': 81, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,56)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    86: {'room_id': 86, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,57)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    10: {'room_id': 10, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(60,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    4: {'room_id': 4, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(61,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    1: {'room_id': 1, 'title': 'Shop', 'description': "You are standing in a small shop. A sign behind the mechanical shopkeeper says 'WILL PAY FOR TREASURE'.", 'coordinates': '(59,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['The Cajoling Man', 'CO_NERD'], 'items': [], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    23: {'room_id': 23, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(61,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure'], 'exits': ['s', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    13: {'room_id': 13, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['spectacular treasure'], 'exits': ['e', 'w'], 'cooldown': 7.5, 'errors': [], 'messages': ['You have walked east.', 'Wise Explorer: -50% CD']}, 
    26: {'room_id': 26, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['James Starks'], 'items': ['amazing treasure'], 'exits': ['e', 'w'], 'cooldown': 7.5, 'errors': [], 'messages': ['You have walked east.', 'Wise Explorer: -50% CD']}, 
    15: {'room_id': 15, 'title': 'JKMT Donuts', 'description': "A glass display case separates you from fried, yummy goodness. Behind the stacks of pink boxes, you hear a worker yelling. A sign reads, 'Donuts for sale!'", 'coordinates': '(63,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure', 'amazing treasure'], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.', 'Grumpy Tommy welcomes you to the shop and says, "What do you want? I have a raid in 15 minutes."']}, 
    55: {'room_id': 55, 'title': 'Wishing Well', 'description': "You are standing besides a large well. A sign next the well reads 'EXAMINE WELL, FIND WEALTH'.", 'coordinates': '(63,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['Krishan the Quail', 'samlili'], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    19: {'room_id': 19, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(60,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    43: {'room_id': 43, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(59,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    20: {'room_id': 20, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(60,63)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['chupacabra'], 'items': [], 'exits': ['n', 's', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    77: {'room_id': 77, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(59,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    63: {'room_id': 63, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(60,64)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['spectacular treasure'], 'exits': ['n', 's', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    27: {'room_id': 27, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(61,63)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    46: {'room_id': 46, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(59,63)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    62: {'room_id': 62, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(58,63)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['User 20721'], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    64: {'room_id': 64, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(58,64)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    84: {'room_id': 84, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(57,63)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['spectacular treasure', 'amazing treasure'], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    82: {'room_id': 82, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(57,64)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    40: {'room_id': 40, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(61,64)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure'], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    28: {'room_id': 28, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(61,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    30: {'room_id': 30, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,63)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'amazing treasure', 'spectacular treasure', 'amazing treasure'], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    31: {'room_id': 31, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure', 'amazing treasure', 'amazing treasure', 'amazing treasure'], 'exits': ['n', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    32: {'room_id': 32, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,63)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'amazing treasure'], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    39: {'room_id': 39, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,64)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'amazing treasure'], 'exits': ['n', 's', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    54: {'room_id': 54, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,63)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'amazing treasure'], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    53: {'room_id': 53, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,65)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['spectacular treasure'], 'exits': ['n', 's', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    51: {'room_id': 51, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,64)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    41: {'room_id': 41, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,64)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'amazing treasure', 'shiny treasure'], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    69: {'room_id': 69, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,65)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['spectacular treasure', 'great treasure'], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    57: {'room_id': 57, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,64)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    145: {'room_id': 145, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(66,64)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure'], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    94: {'room_id': 94, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,66)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure', 'amazing treasure', 'amazing treasure'], 'exits': ['n', 's'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    103: {'room_id': 103, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,65)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'great treasure', 'great treasure', 'great treasure', 'amazing treasure'], 'exits': ['n', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    95: {'room_id': 95, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,66)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure'], 'exits': ['n', 's', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    88: {'room_id': 88, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,65)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['shiny treasure'], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    122: {'room_id': 122, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(61,65)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure', 'great treasure'], 'exits': ['n', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    160: {'room_id': 160, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,66)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'spectacular treasure', 'amazing treasure', 'spectacular treasure', 'amazing treasure', 'shiny treasure'], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    174: {'room_id': 174, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(66,65)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    220: {'room_id': 220, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(67,64)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    192: {'room_id': 192, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(66,66)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    224: {'room_id': 224, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(67,65)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    33: {'room_id': 33, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    152: {'room_id': 152, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,67)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'spectacular treasure'], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    201: {'room_id': 201, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(66,67)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['shiny treasure', 'tiny treasure', 'amazing treasure'], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    223: {'room_id': 223, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(67,66)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    283: {'room_id': 283, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(67,67)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['spectacular treasure'], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    331: {'room_id': 331, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(67,68)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['spectacular treasure'], 'exits': ['s', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    313: {'room_id': 313, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(68,67)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    446: {'room_id': 446, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(68,68)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure'], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    466: {'room_id': 466, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(69,68)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    486: {'room_id': 486, 'title': "Arron's Athenaeum", 'description': "Before you lies a radiant book of knowledge, on a pedestal inlaid with Lambda Coins. Below, a plaque reads:  Herin exists knowledge gathered by Arron of Web19/CS21. Always seek to learn. Ask questions. Don't panic, bring a towel.", 'coordinates': '(69,67)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['matthewJAM'], 'items': [], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    472: {'room_id': 472, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(70,68)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure'], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    72: {'room_id': 72, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(60,65)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['Mastin'], 'items': ['spectacular treasure', 'spectacular treasure'], 'exits': ['s', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    73: {'room_id': 73, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(59,64)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure', 'amazing treasure', 'amazing treasure', 'amazing treasure', 'amazing treasure', 'great treasure', 'spectacular treasure', 'amazing treasure', 'great treasure'], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    76: {'room_id': 76, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(59,65)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    119: {'room_id': 119, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,67)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['[Mario]'], 'items': ['amazing treasure'], 'exits': ['n', 's'], 'cooldown': 7.5, 'errors': [], 'messages': ['You have walked north.', 'Wise Explorer: -50% CD']}, 
    115: {'room_id': 115, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(62,66)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'amazing treasure'], 'exits': ['n', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    134: {'room_id': 134, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(63,68)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    124: {'room_id': 124, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(61,66)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure'], 'exits': ['n', 's'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    91: {'room_id': 91, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(56,63)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['spectacular treasure', 'great treasure'], 'exits': ['n', 's', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    180: {'room_id': 180, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(56,64)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'amazing treasure', 'amazing treasure', 'spectacular treasure', 'amazing treasure'], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    101: {'room_id': 101, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(56,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'great treasure'], 'exits': ['n', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    99: {'room_id': 99, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(55,63)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    190: {'room_id': 190, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(55,64)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure'], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    146: {'room_id': 146, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(54,63)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['LORD_DEREK'], 'items': [], 'exits': ['n', 's', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    215: {'room_id': 215, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(54,64)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    177: {'room_id': 177, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(54,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    257: {'room_id': 257, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(53,63)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['AmazingLippe'], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    113: {'room_id': 113, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(55,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    114: {'room_id': 114, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(55,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure'], 'exits': ['n', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    176: {'room_id': 176, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(54,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    191: {'room_id': 191, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(57,65)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    246: {'room_id': 246, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(54,65)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    346: {'room_id': 346, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(53,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    402: {'room_id': 402, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(53,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    451: {'room_id': 451, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(52,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 7.5, 'errors': [], 'messages': ['You have walked east.', 'Wise Explorer: -50% CD']}, 
    453: {'room_id': 453, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(51,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']},
    83: {'room_id': 83, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(59,66)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    110: {'room_id': 110, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(58,65)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    130: {'room_id': 130, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(60,66)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['User 20646', 'Duraan'], 'items': ['amazing treasure'], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    125: {'room_id': 125, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(58,66)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    165: {'room_id': 165, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(58,67)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['zoverlvx'], 'items': [], 'exits': ['n', 's', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    237: {'room_id': 237, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(57,66)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 7.5, 'errors': [], 'messages': ['You have walked east.', 'Wise Explorer: -50% CD']}, 
    245: {'room_id': 245, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(56,66)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    320: {'room_id': 320, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(53,64)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    364: {'room_id': 364, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(52,63)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    348: {'room_id': 348, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(53,65)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    429: {'room_id': 429, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(52,64)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    381: {'room_id': 381, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(52,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    448: {'room_id': 448, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(51,63)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['tree'], 'items': [], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    394: {'room_id': 394, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(51,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    38: {'room_id': 38, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['shiny treasure'], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    59: {'room_id': 59, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure', 'amazing treasure', 'spectacular treasure', 'amazing treasure', 'spectacular treasure'], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    66: {'room_id': 66, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure', 'amazing treasure', 'amazing treasure', 'amazing treasure', 'amazing treasure'], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    104: {'room_id': 104, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(64,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'amazing treasure'], 'exits': ['n', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    92: {'room_id': 92, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure', 'amazing treasure', 'great treasure', 'amazing treasure', 'amazing treasure', 'great treasure'], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    169: {'room_id': 169, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,63)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    123: {'room_id': 123, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(66,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['great treasure', 'amazing treasure', 'amazing treasure', 'great treasure', 'amazing treasure', 'amazing treasure'], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    107: {'room_id': 107, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['spectacular treasure'], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    120: {'room_id': 120, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(65,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    121: {'room_id': 121, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(66,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    128: {'room_id': 128, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(66,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    143: {'room_id': 143, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(67,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    189: {'room_id': 189, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(67,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    212: {'room_id': 212, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(68,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    255: {'room_id': 255, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(68,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    186: {'room_id': 186, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(66,63)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    205: {'room_id': 205, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(67,63)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    241: {'room_id': 241, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(67,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    479: {'room_id': 479, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(68,63)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['azra-was-here]'], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    266: {'room_id': 266, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(68,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    127: {'room_id': 127, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(66,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': ['amazing treasure'], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    184: {'room_id': 184, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(67,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    221: {'room_id': 221, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(68,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    253: {'room_id': 253, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(68,58)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    240: {'room_id': 240, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(69,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    249: {'room_id': 249, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(69,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['Manju KC'], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    386: {'room_id': 386, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(70,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    414: {'room_id': 414, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(71,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    265: {'room_id': 265, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(69,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 's', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    282: {'room_id': 282, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(70,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    258: {'room_id': 258, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(69,58)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    306: {'room_id': 306, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(70,58)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    397: {'room_id': 397, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(71,58)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked east.']}, 
    279: {'room_id': 279, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(69,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    270: {'room_id': 270, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(70,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    416: {'room_id': 416, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(70,62)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['s'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    338: {'room_id': 338, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(71,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['[Daniel Jones]'], 'items': [], 'exits': ['s', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    379: {'room_id': 379, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(71,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    395: {'room_id': 395, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(72,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ["['DESNACIA']"], 'items': [], 'exits': ['s', 'e', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}, 
    403: {'room_id': 403, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(72,59)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    421: {'room_id': 421, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(73,60)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['n', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked south.']}, 
    440: {'room_id': 440, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(73,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': ['STRAIGHT DmICK DEMERY'], 'items': [], 'exits': ['s', 'w'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked north.']}, 
    476: {'room_id': 476, 'title': 'A misty room', 'description': 'You are standing on grass and surrounded by a dense mist. You can barely make out the exits in any direction.', 'coordinates': '(72,61)', 'elevation': 0, 'terrain': 'NORMAL', 'players': [], 'items': [], 'exits': ['e'], 'cooldown': 15.0, 'errors': [], 'messages': ['You have walked west.']}
}

directions =  {
    112: {'s': 141, 'e': 140, 'w': 100}, 
    141: {'n': 112, 'e': 156}, 
    140: {'w': 112}, 
    100: {'e': 112, 's': 106, 'w': 68}, 
    106: {'n': 100, 's': 111, 'w': 135}, 
    68: {'e': 100, 'n': 52}, 
    111: {'n': 106, 's': 367, 'e': 158}, 
    135: {'e': 106, 's': 150}, 
    150: {'n': 135, 'w': 166}, 
    166: {'e': 150, 's': 198, 'w': 117}, 
    198: {'n': 166, 's': 239, 'e': 199}, 
    117: {'e': 166, 's': 131, 'n': 108, 'w': 133}, 
    367: {'n': 111}, 
    158: {'w': 111, 's': 167},
    52: {'s': 68, 'n': 35, 'e': 75}, 
    35: {'s': 52, 'w': 34}, 
    75: {'w': 52, 'e': 85}, 
    85: {'w': 75, 'e': 154}, 
    156: {'w': 141, 's': 168, 'e': 164}, 
    168: {'n': 156, 'e': 340}, 
    164: {'w': 156, 'n': 217, 'e': 298}, 
    217: {'s': 164, 'e': 247}, 
    298: {'w': 164, 's': 324}, 
    247: {'w': 217, 'e': 261}, 
    324: {'n': 298, 's': 349, 'e': 354}, 
    340: {'w': 168}, 
    261: {'w': 247, 's': 277, 'e': 322}, 
    277: {'n': 261, 'e': 323}, 
    322: {'w': 261, 'n': 382, 'e': 435}, 
    382: {'s': 322, 'e': 388}, 
    435: {'w': 322}, 
    388: {'w': 382, 'e': 477}, 
    477: {'w': 388, 'e': 483}, 
    483: {'w': 477}, 
    167: {'n': 158, 's': 262, 'e': 260}, 
    262: {'n': 167, 's': 370, 'e': 358}, 
    260: {'w': 167}, 
    370: {'n': 262, 's': 434, 'e': 407}, 
    358: {'w': 262, 'e': 401}, 
    401: {'w': 358}, 
    434: {'n': 370}, 
    407: {'w': 370, 's': 496}, 
    496: {'n': 407}, 
    154: {'w': 85, 'e': 193}, 
    193: {'w': 154, 'e': 251}, 
    251: {'w': 193, 'e': 315}, 
    315: {'w': 251}, 
    34: {'e': 35, 'n': 14, 's': 50}, 
    14: {'s': 34, 'e': 37, 'w': 12}, 
    50: {'n': 34, 's': 89}, 
    37: {'w': 14},
    12: {'e': 14, 'n': 9, 's': 18, 'w': 21}, 
    9: {'s': 12, 'n': 3, 'e': 11}, 
    18: {'n': 12, 's': 22, 'w': 25}, 
    21: {'e': 12, 'w': 29}, 
    3: {'s': 9, 'e': 5, 'w': 2}, 
    11: {'w': 9, 'e': 17}, 
    5: {'w': 3}, 
    2: {'e': 3, 'n': 0, 's': 6}, 
    0: {'s': 2, 'n': 10, 'e': 4, 'w': 1}, 
    6: {'n': 2, 'w': 7}, 
    7: {'e': 6, 'n': 8, 'w': 56}, 
    8: {'s': 7, 'w': 16}, 
    56: {'e': 7}, 
    16: {'e': 8, 'n': 58, 'w': 67}, 
    58: {'s': 16, 'w': 65}, 
    67: {'e': 16, 'w': 162}, 
    162: {'e': 67}, 
    65: {'e': 58, 'n': 74, 'w': 139}, 
    74: {'s': 65, 'n': 87, 'w': 161}, 
    139: {'e': 65, 'w': 188}, 
    188: {'e': 139, 'w': 335}, 
    87: {'s': 74}, 
    161: {'e': 74},
    335: {'e': 188, 'w': 366}, 
    366: {'e': 335}, 
    89: {'n': 50, 's': 93}, 
    93: {'n': 89, 'w': 108}, 
    108: {'e': 93, 's': 117, 'n': 78}, 
    239: {'n': 198, 'w': 244}, 
    199: {'w': 198, 's': 230}, 
    230: {'n': 199, 's': 307, 'e': 297}, 
    307: {'n': 230, 's': 373, 'e': 371, 'w': 321}, 
    297: {'w': 230}, 
    373: {'n': 307, 's': 480}, 
    371: {'w': 307, 's': 475}, 
    321: {'e': 307, 's': 413}, 
    475: {'n': 371, 's': 484}, 
    484: {'n': 475}, 
    480: {'n': 373}, 
    413: {'n': 321}, 
    244: {'e': 239, 'n': 131}, 
    131: {'s': 244, 'n': 117, 'w': 138}, 
    138: {'e': 131, 's': 211, 'w': 195},
    133: {'e': 117, 'w': 173}, 
    211: {'n': 138}, 
    195: {'e': 138}, 
    78: {'s': 108, 'n': 22}, 
    22: {'s': 78, 'n': 18, 'w': 36}, 
    323: {'w': 277, 'e': 433}, 
    433: {'w': 323}, 
    349: {'n': 324, 's': 352, 'e': 384, 'w': 356}, 
    354: {'w': 324}, 
    173: {'e': 133, 'w': 214}, 
    214: {'e': 173, 'n': 194, 'w': 226}, 
    352: {'n': 349, 's': 362, 'e': 485}, 
    384: {'w': 349}, 
    356: {'e': 349}, 
    362: {'n': 352, 's': 399, 'w': 463}, 
    485: {'w': 352}, 
    399: {'n': 362, 's': 467}, 
    463: {'e': 362, 's': 468}, 
    468: {'n': 463}, 
    467: {'n': 399}, 
    194: {'s': 214, 'w': 129}, 
    226: {'e': 214, 's': 300}, 
    300: {'n': 226, 's': 377, 'w': 389}, 
    377: {'n': 300}, 
    389: {'e': 300}, 
    36: {'e': 22, 's': 48, 'w': 60}, 
    25: {'e': 18}, 
    48: {'n': 36, 's': 105, 'w': 149}, 
    60: {'e': 36, 'n': 45, 'w': 70}, 
    45: {'s': 60, 'n': 29}, 
    70: {'e': 60, 's': 163, 'w': 98}, 
    29: {'s': 45, 'e': 21, 'w': 49}, 
    49: {'e': 29, 's': 79, 'w': 136}, 
    79: {'n': 49}, 
    136: {'e': 49, 'w': 148}, 
    163: {'n': 70}, 
    98: {'e': 70, 'n': 102, 's': 126, 'w': 109}, 
    102: {'s': 98, 'w': 142}, 
    126: {'n': 98, 's': 129}, 
    109: {'e': 98, 's': 185, 'w': 175}, 
    185: {'n': 109}, 
    175: {'e': 109, 'w': 179, 's': 183}, 
    129: {'n': 126, 'e': 194, 'w': 170}, 
    142: {'e': 102, 'w': 159}, 
    159: {'e': 142, 'w': 196}, 
    170: {'e': 129}, 
    148: {'e': 136}, 
    105: {'n': 48, 'w': 202}, 
    149: {'e': 48}, 
    202: {'e': 105}, 
    420: {'s': 444, 'e': 213, 'w': 437}, 
    444: {'n': 420}, 
    213: {'w': 420, 'e': 179}, 
    437: {'e': 420}, 
    179: {'w': 213, 's': 233, 'e': 175}, 
    233: {'n': 179, 'w': 238}, 
    238: {'e': 233}, 
    183: {'n': 175, 's': 229}, 
    229: {'n': 183, 's': 250, 'w': 236}, 
    250: {'n': 229, 's': 294, 'e': 289}, 
    236: {'e': 229, 's': 264}, 
    294: {'n': 250, 's': 334}, 
    289: {'w': 250}, 
    334: {'n': 294, 's': 393, 'e': 341, 'w': 391}, 
    393: {'n': 334, 's': 482}, 
    341: {'w': 334, 's': 449}, 
    391: {'e': 334, 's': 396, 'w': 428}, 
    449: {'n': 341}, 
    482: {'n': 393}, 
    396: {'n': 391}, 
    428: {'e': 391}, 
    264: {'n': 236, 's': 274, 'w': 273}, 
    274: {'n': 264}, 
    273: {'e': 264}, 
    196: {'e': 159, 'n': 222, 'w': 197}, 
    222: {'s': 196, 'n': 305}, 
    197: {'e': 196, 'n': 232, 'w': 276}, 
    305: {'s': 222, 'n': 365}, 
    232: {'s': 197, 'n': 272, 'w': 235}, 
    276: {'e': 197, 'w': 419}, 
    272: {'s': 232, 'n': 295}, 
    235: {'e': 232, 'n': 330, 'w': 355}, 
    295: {'s': 272}, 
    330: {'s': 235, 'n': 369, 'w': 383}, 
    355: {'e': 235}, 
    369: {'s': 330, 'n': 400, 'w': 376}, 
    383: {'e': 330, 'w': 495}, 
    495: {'e': 383}, 
    365: {'s': 305}, 
    400: {'s': 369}, 
    376: {'e': 369}, 
    419: {'e': 276}, 
    17: {'w': 11, 'n': 24, 'e': 42}, 
    24: {'s': 17}, 
    42: {'w': 17, 'n': 44, 's': 80, 'e': 118}, 
    44: {'s': 42}, 
    80: {'n': 42, 's': 81, 'e': 86}, 
    118: {'w': 42, 'e': 137}, 
    137: {'w': 118}, 
    81: {'n': 80}, 
    86: {'w': 80}, 
    10: {'s': 0, 'n': 19, 'w': 43}, 
    4: {'w': 0, 'n': 23, 'e': 13}, 
    1: {'e': 0}, 
    23: {'s': 4, 'e': 26}, 
    13: {'w': 4, 'e': 15}, 
    26: {'w': 23, 'e': 55}, 
    15: {'w': 13}, 
    55: {'w': 26}, 
    19: {'s': 10, 'n': 20, 'w': 77}, 
    43: {'e': 10}, 
    20: {'s': 19, 'n': 63, 'e': 27, 'w': 46}, 
    77: {'e': 19}, 
    63: {'s': 20, 'n': 72, 'w': 73}, 
    27: {'w': 20, 'n': 40, 's': 28, 'e': 30}, 
    46: {'e': 20, 'w': 62}, 
    62: {'e': 46, 'n': 64, 'w': 84}, 
    64: {'s': 62, 'w': 82}, 
    84: {'e': 62, 'w': 91}, 
    82: {'e': 64, 'n': 191}, 
    40: {'s': 27}, 
    28: {'n': 27}, 
    30: {'w': 27, 's': 31, 'e': 32}, 
    31: {'n': 30, 'e': 33}, 
    32: {'w': 30, 'n': 39, 'e': 54}, 
    39: {'s': 32, 'n': 53, 'e': 51, 'w': 41}, 
    54: {'w': 32}, 
    53: {'s': 39, 'n': 95, 'w': 88}, 
    51: {'w': 39, 'n': 69, 'e': 57}, 
    41: {'e': 39}, 
    69: {'s': 51, 'n': 94, 'e': 103}, 
    57: {'w': 51, 'e': 145}, 
    145: {'w': 57, 'n': 174, 'e': 220}, 
    94: {'s': 69, 'n': 152}, 
    103: {'w': 69, 'n': 160}, 
    95: {'s': 53, 'n': 119, 'w': 115}, 
    88: {'e': 53, 'w': 122}, 
    122: {'e': 88, 'n': 124}, 
    160: {'s': 103}, 
    174: {'s': 145, 'n': 192, 'e': 224}, 
    220: {'w': 145}, 
    192: {'s': 174, 'n': 201, 'e': 223}, 
    224: {'w': 174}, 
    33: {'w': 31, 'e': 38}, 
    152: {'s': 94}, 
    201: {'s': 192}, 
    223: {'w': 192, 'n': 283}, 
    283: {'s': 223, 'n': 331, 'e': 313}, 
    331: {'s': 283, 'e': 446}, 
    313: {'w': 283}, 
    446: {'w': 331, 'e': 466}, 
    466: {'w': 446, 's': 486, 'e': 472}, 
    486: {'n': 466}, 
    472: {'w': 466}, 
    72: {'s': 63, 'w': 76}, 
    73: {'e': 63}, 
    76: {'e': 72, 'n': 83, 'w': 110}, 
    119: {'s': 95, 'n': 134}, 
    115: {'e': 95}, 
    134: {'s': 119}, 
    124: {'s': 122}, 
    91: {'e': 84, 'n': 180, 's': 101, 'w': 99}, 
    180: {'s': 91}, 
    101: {'n': 91, 'w': 113}, 
    99: {'e': 91, 'n': 190, 'w': 146}, 
    190: {'s': 99}, 
    146: {'e': 99, 'n': 215, 's': 177, 'w': 257}, 
    215: {'s': 146, 'n': 246}, 
    177: {'n': 146, 'w': 346}, 
    257: {'e': 146, 'n': 320, 'w': 364}, 
    113: {'e': 101, 's': 114},
    114: {'n': 113, 'w': 176}, 
    176: {'e': 114, 'w': 402}, 
    191: {'s': 82}, 
    246: {'s': 215}, 
    346: {'e': 177}, 
    402: {'e': 176, 'w': 451}, 
    451: {'e': 402, 'w': 453}, 
    453: {'e': 451}, 
    83: {'s': 76, 'e': 130, 'w': 125}, 
    110: {'e': 76}, 
    130: {'w': 83}, 
    125: {'e': 83, 'n': 165, 'w': 237}, 
    165: {'s': 125}, 
    237: {'e': 125, 'w': 245}, 
    245: {'e': 237}, 
    320: {'s': 257, 'n': 348}, 
    364: {'e': 257, 'n': 429, 's': 381, 'w': 448}, 
    348: {'s': 320}, 
    429: {'s': 364}, 
    381: {'n': 364, 'w': 394}, 
    448: {'e': 364}, 
    394: {'e': 381}, 
    38: {'w': 33, 's': 59, 'e': 66}, 
    59: {'n': 38, 's': 104, 'e': 92}, 
    66: {'w': 38, 'n': 169, 'e': 123}, 
    104: {'n': 59, 'e': 107}, 
    92: {'w': 59}, 
    169: {'s': 66, 'e': 186}, 
    123: {'w': 66}, 
    107: {'w': 104, 's': 120, 'e': 121}, 
    120: {'n': 107, 'e': 127}, 
    121: {'w': 107, 'n': 128, 'e': 143}, 
    128: {'s': 121, 'e': 189}, 
    143: {'w': 121, 'e': 212}, 
    189: {'w': 128, 'e': 255}, 
    212: {'w': 143}, 
    255: {'w': 189}, 
    186: {'w': 169, 'e': 205}, 
    205: {'w': 186, 's': 241, 'e': 479}, 
    241: {'n': 205, 'e': 266}, 
    479: {'w': 205}, 
    266: {'w': 241}, 
    127: {'w': 120, 'e': 184}, 
    184: {'w': 127, 'e': 221}, 
    221: {'w': 184, 's': 253, 'e': 240}, 
    253: {'n': 221, 'e': 258}, 
    240: {'w': 221, 'n': 249, 'e': 386}, 
    249: {'s': 240, 'n': 265, 'e': 282}, 
    386: {'w': 240, 'e': 414}, 
    414: {'w': 386}, 
    265: {'s': 249, 'n': 279, 'e': 270}, 
    282: {'w': 249}, 
    258: {'w': 253, 'e': 306}, 
    306: {'w': 258, 'e': 397}, 
    397: {'w': 306}, 
    279: {'s': 265}, 
    270: {'w': 265, 'n': 416, 'e': 338}, 
    416: {'s': 270}, 
    338: {'w': 270, 's': 379}, 
    379: {'n': 338, 'e': 395}, 
    395: {'w': 379, 's': 403, 'e': 421}, 
    403: {'n': 395}, 
    421: {'w': 395, 'n': 440}, 
    440: {'s': 421, 'w': 476}, 
    476: {'e': 440}
}
#tracks if we've fully explored a room.
visited = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 44, 45, 46, 48, 49, 50, 51, 52, 53, 54, 57, 58, 59, 60, 62, 63, 64, 65, 66, 67, 68, 69, 70, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 87, 88, 89, 91, 92, 93, 94, 95, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 117, 118, 119, 120, 121, 122, 123, 125, 126, 127, 128, 129, 131, 133, 135, 136, 137, 138, 139, 140, 141, 142, 143, 145, 146, 149, 150, 152, 154, 156, 158, 159, 160, 161, 162, 163, 164, 166, 167, 168, 169, 173, 174, 175, 176, 177, 179, 180, 183, 184, 185, 186, 188, 189, 190, 191, 192, 193, 194, 196, 197, 198, 199, 201, 202, 205, 211, 212, 213, 214, 215, 217, 220, 221, 222, 223, 224, 226, 229, 230, 232, 233, 235, 236, 237, 238, 239, 240, 241, 244, 246, 247, 249, 250, 251, 253, 255, 257, 258, 260, 261, 262, 264, 265, 266, 270, 272, 276, 277, 279, 282, 283, 289, 294, 295, 297, 298, 300, 305, 306, 307, 313, 315, 320, 321, 322, 323, 324, 330, 331, 334, 335, 338, 340, 341, 346, 348, 349, 352, 354, 355, 356, 358, 362, 364, 365, 366, 367, 369, 370, 371, 373, 376, 377, 379, 381, 382, 383, 384, 386, 388, 389, 391, 393, 394, 395, 396, 397, 399, 400, 401, 402, 407, 413, 414, 416, 419, 420, 421, 428, 429, 434, 435, 440, 446, 448, 449, 451, 463, 466, 467, 468, 472, 475, 476, 477, 479, 480, 482, 483, 484, 485, 495, 496}
traversal_path = [] #path taken from last root node
stack = [] #to track untraveled rooms

#check for wise explorer bonus
def check_bonus(room, move, directions, payload):
    #if the current room, in directions, has a key for the move we're making
    if room['room_id'] in directions:
        if move in directions[room['room_id']]:
                payload['directions'] = directions[room['room_id']][move]
                return
    else:
        return    
    #add a ['directions'] key to the request's payload with the value

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
    print(f"{len(visited)} rooms explored. {500 - len(visited)} left to discover")

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

    previous_room = current_room['room_id'] #adjusting value for the next loop

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
            print(f"exits: {exits}")
            print(f"opposites: {opposites}\n")

            #move to a side room and wait
            payload = {f'direction': f'{exits[i]}'} 
            check_bonus(current_room, exits[i], directions, payload)
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
            check_bonus(new_room, opposites[i], directions, payload)
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
    check_bonus(current_room, rand_selection, directions, last_data)
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
        print(f"moved to room {next_move['room_id']}")
        print(f"waiting {next_move['cooldown']} seconds")
        time.sleep(next_move['cooldown'])

        #choose a new room to explore
        new_rand = random.randint(0, (len(next_move['exits'])-1))
        other_data = {'direction':f"{exits[rand]}"}
        check_bonus(next_move, exits[rand], directions, other_data)
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