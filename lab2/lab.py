# NO IMPORTS ALLOWED!

import json

# print colored text, the colors are defined below
W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple


def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
    """
        return true if actor_1 and actor_2 did act together
        return false if they did not
        data: list of records containing the actor ids and the film they acted
              together
    """
    # iterate over every record
    for record in data:
        if (actor_id_1 in record) & (actor_id_2 in record):
            return True

    # the function didn't return true over every records
    return False

# I have tried to solved the algorithms problem myself
# , however I can't.

# Dynamic Programming: the method stores every actor
# who has acted with specific actor,
# more generally, stores the data that is already or
# has to be computed for future use.


def find_neighbors(data):
    """
    return a dictonary, whose keys are the specific actor and whose values are\
    the set of actors the specific actor has acted with.
    """
    acted_with = {}
    for actor_id_1, actor_id_2, _ in data:
        # dictonary.setdefault(key,[default]): if key
        # is in the dictionar, return the key's value;\
        # if not, insert the key, and return the default.
        # In this case, return the actors set specific to actor_id_1
        if actor_id_1 != actor_id_2:
            acted_with.setdefault(actor_id_1, set()).add(actor_id_2)
            acted_with.setdefault(actor_id_2, set()).add(actor_id_1)
    return acted_with


def expand(acted_with, current_level, parents):
    """
    Expand the current_level to its next bacon number actors
    Arguments:
        acted_with: the output from neighbors(data)
        current_level: a set of actor IDs of the current bacon numbers
        parents: all sets of actor IDs of the previous Bacon numbers

    Returns:
    the set of actor IDs of the next Bacon numbers.`
    """
    new_level = set()
    for actor in current_level:
        for neighbor in acted_with[actor]:
            # if the neighbor was already assigned a Bacon number,
            # pass, if not then the neighbor can be added to next
            # Bacon number set
            if all(neighbor not in actors for actors in parents.values()):
                new_level.add(neighbor)
    return new_level


# globals to store the computed results and to check update.
DATA = []
ACTED_WITH = find_neighbors(DATA)
KNOWN_RESULTS = {0: {4724}}


def get_actors_with_bacon_number(data, n):
    """
    I use dynamic programming technique:
    three global var to represent data, acted_with dictionary
    and computed bacon number and its sets which are stored in a dictionary.
    first look up in the dictionary,
    if the key is not in the dictionary, then recures.
    """
    # declare the globals
    global DATA
    global ACTED_WITH
    global KNOWN_RESULTS
    # if the data is a new data set then the KNOW_RESULTS has to be reseted
    # ACTED_WITH has to be updated, otherwise two are the same as before
    if data != DATA:
        DATA = data
        ACTED_WITH = find_neighbors(DATA)
        KNOWN_RESULTS = {0: {4724}}

    # first look up in the KNOWN_RESULTS dictionary
    if n in KNOWN_RESULTS:
        return KNOWN_RESULTS[n]
    #  recurse: expand from the previous Bacon number
    else:
        cur_lev = expand(
            ACTED_WITH, get_actors_with_bacon_number(data, n - 1), KNOWN_RESULTS)
        KNOWN_RESULTS[n] = cur_lev
        return cur_lev


def get_bacon_path(data, actor_id):
    """
    return the path from bacon to actor_id
    """
    Bacon_id = 4724
    return get_path(data, Bacon_id, actor_id)


def two_points_path(data):
    """
    return the path dictionary
    {(actor_id_1,actor_id_2):[actor_id_1,actor_id_2]}
    """
    path = {}
    for actor_id_1, actor_id_2, _ in data:
        if actor_id_2 != actor_id_1:
            path[(actor_id_1, actor_id_2)] = [actor_id_1, actor_id_2]
            path[(actor_id_2, actor_id_1)] = [actor_id_2, actor_id_1]
    return path


# global to store the path,
# a dictionary whose keys are (start point, end point),
# in other words, (actor_id_1, actor_id_2)
PATH = {}


def add_path(actor_id_1, actor_id_2, path):
    """add two reverse paths to the PATH dicitonary"""
    global PATH

    PATH[(actor_id_1, actor_id_2)] = path
    PATH[(actor_id_2, actor_id_1)] = path.reverse()


def get_path(data, actor_id_1, actor_id_2, count=0):
    """
    first check the data is same before, if not update all
    then look up in the PATH, return path, if it was computed before
    if not recurse and stores the pathes computed in the PATH.
    However, the maxium recursion depth is set to be 8 becuse of the 6 
    degree of seperation. In this case, the function will return None
    to donote that the two actors are not connected by any path.
    Normally, the fourth argument should not be input but the initail zero.
    """
    # declare the globals
    global DATA
    global ACTED_WITH
    global PATH

    # keep track of the recursion depth
    # return None if recursed to the max depth
    # the two actor are not connected by any path
    count = +1
    if count == 8:
        return None

    # udpate the globals, if DATA is not same as data
    # or PATH are the initial empty dictionary
    if data != DATA or PATH == {}:
        print('yes')
        DATA = data
        PATH = two_points_path(DATA)
        ACTED_WITH = find_neighbors(DATA)
    print(PATH)
    print(ACTED_WITH)

    # look it up in the PATH dictionary
    if (actor_id_1, actor_id_2) in PATH:
        return PATH[(actor_id_1, actor_id_2)]
    # recurse and store
    else:
        shortest_path = []
        for neighbor1 in ACTED_WITH[actor_id_1]:
            for neighbor2 in ACTED_WITH[actor_id_2]:
                # find the path between neighbors,
                # the shorted path is chosen
                if neighbor1 != neighbor2:
                    path = get_path(data, neighbor1, neighbor2, count)
                    # if the path is shorter then the current shortest_path
                    # shortest_path is undated to be path
                    # or shorted_path = [], still initials,
                    # the shortesst_path is updated to be first path
                    print(path)
                    if len(path) < len(shortest_path) or shortest_path == []:
                        shortest_path = path
                else:
                    new_path = [actor_id_1, neighbor1, neighbor2, actor_id_2]
                    add_path(actor_id_1, actor_id_2, new_path)
                    return new_path
        # no sequitial neibors
        new_path = [actor_id_1] + shortest_path.append(actor_id_2)
        add_path(actor_id_1, actor_id_2, new_path)
        return new_path


if __name__ == '__main__':
    with open('resources/small.json') as f:
        smalldb = json.load(f)

    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass


# def setUp(filename):
#     with open(filename, 'r') as f:
#         return json.load(f)


# # to global list to store name_to_ID and ID_to_name mappings
# NAME_ID = setUp('resources/names.json')
# ID_NAME = {}
# for NAME, ID in NAME_ID.items():
#     ID_NAME[ID] = NAME


# def id(val):
#     """
#     If input the Actor's name, return the id of the actor
#     If input the Actor Id number, return the name of the actor.
#     """
#     global NAME_ID
#     global ID_NAME
#     if type(val) == int:
#         # input is ID number
#         ID = val
#         return ID_NAME[ID]

#     if type(val) == str:
#         # input is name
#         NAME = val
#         return NAME_ID[NAME]


# #  anwsers to questions in  3)ACTING TOGATHER
# data_1 = setUp('resources/small.json')

# # Question Set 1
# print(R + "\n QUESITON SET 1 \n")

# # Question 1
# print(B + 'According to the small.json database, have Christopher Showerman and Dan Warry-Smith acted together? \n ' + O)

# if did_x_and_y_act_together(data_1, id("Christopher Showerman"), id("Dan Warry-Smith")):
#     print('Yes, they have.' + B)
# else:
#     print('No, they haven\'t' + B)

# # Question 2
# print('According to the small.json database, have Christopher Showerman and Dan Warry-Smith acted together? \n ' + O)

# if did_x_and_y_act_together(data_1, id("Christopher Showerman"), id("Dan Warry-Smith")):
#     print('Yes, they have.' + B)
# else:
#     print('No, they haven\'t' + B)

# # Question 3
# print('According to the small.json database, have Scott Subiono and Christian Campbell acted together? \n ' + O)

# if did_x_and_y_act_together(data_1, id("Scott Subiono"), id("Christian Campbell")):
#     print('Yes, they have.' + B)
# else:
#     print('No, they haven\'t' + B)

# # Question 4
# print('According to the small.json database, have Stephen Blackehart and Lew Knopp acted together?\n ' + O)

# if did_x_and_y_act_together(data_1, id("Stephen Blackehart"), id("Lew Knopp")):
#     print('Yes, they have.' + B)
# else:
#     print('No, they haven\'t' + B)

# # Question 5
# print('According to the small.json database, have Philip Bosco and Paul Bru acted together? \n ' + O)

# if did_x_and_y_act_together(data_1, id("Philip Bosco"), id("Paul Bru")):
#     print(O + 'Yes, they have.' + W)
# else:
#     print(O + 'No, they haven\'t' + W)


# # Question Set 2
# print(R + "\n QUESITON SET 2 \n")

# # Question 1
# print(O + "In the small.json database, what is the list of actors with Bacon number 3? Enter your answer below, as a Python list of actor names: \n")
# names_3 = []
# for actor_id in get_actors_with_bacon_number(data_1, 3):
#     names_3.append(id(actor_id))
# print(B + str(names_3), "\n")

# # Question 2
# print(O + "In the small.json database, what is the list of actors with Bacon number 4? Enter your answer below, as a Python list of actor names: \n")
# names_4 = []
# for actor_id in get_actors_with_bacon_number(data_1, 4):
#     names_4.append(id(actor_id))
# print(B + str(names_4), "\n")

# # Change from small.json to large.json
# data_2 = setUp('resources/large.json')

# # Question 3
# print(O + "In the large.json database, what is the list of actors with Bacon number 5? Enter your answer below, as a Python list of actor names: \n")
# names_5 = []
# for actor_id in get_actors_with_bacon_number(data_2, 5):
#     names_5.append(id(actor_id))
# print(B + str(names_5), "\n")


# # Question 4
# print(O + "In the large.json database, what is the list of actors with Bacon number 6? Enter your answer below, as a Python list of actor names: \n")
# names_6 = []
# for actor_id in get_actors_with_bacon_number(data_2, 6):
#     names_6.append(id(actor_id))
# print(B + str(names_6), "\n" + W)
