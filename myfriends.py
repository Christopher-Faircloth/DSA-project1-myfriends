"""Assignment 1: Friend of a Friend

Please complete these functions, to answer queries given a dataset of
friendship relations, that meet the specifications of the handout
and docstrings below.

Notes:
- you should create and test your own scenarios to fully test your functions, 
  including testing of "edge cases"
"""
from collections import deque

from py_friends.friends import Friends

"""
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************
************** READ THIS ***************

If you worked in a group on this project, please type the EIDs of your groupmates below (do not include yourself).
Leave it as TODO otherwise.
Groupmate 1: TODO
Groupmate 2: TODO
"""

def load_pairs(filename):
    """
    Args:
        filename (str): name of input file

    Returns:
        List of pairs, where each pair is a Tuple of two strings

    Notes:
    - Each non-empty line in the input file contains two strings, that
      are separated by one or more space characters.
    - You should remove whitespace characters, and skip over empty input lines.
    """
    list_of_pairs = []
    with open(filename, 'rt') as infile:

# ------------ BEGIN YOUR CODE ------------

        for line in infile:
            names = tuple(line.strip().split(" "))
            list_of_pairs.append(names)


# ------------ END YOUR CODE ------------

    return list_of_pairs 

def make_friends_directory(pairs):
    """Create a directory of persons, for looking up immediate friends

    Args:
        pairs (List[Tuple[str, str]]): list of pairs

    Returns:
        Dict[str, Set] where each key is a person, with value being the set of 
        related persons given in the input list of pairs

    Notes:
    - you should infer from the input that relationships are two-way: 
      if given a pair (x,y), then assume that y is a friend of x, and x is 
      a friend of y
    - no own-relationships: ignore pairs of the form (x, x)
    """
    directory = dict()

    # ------------ BEGIN YOUR CODE ------------

    
    for pair in pairs:
        firstName = pair[0]
        secondName = pair[1]
        if firstName != secondName:
            if firstName not in directory:
                directory[firstName] = set()
            if secondName not in directory:
                directory[secondName] = set()
            directory[firstName].add(secondName)
            directory[secondName].add(firstName)

    # ------------ END YOUR CODE ------------

    return directory


def find_all_number_of_friends(my_dir):
    """List every person in the directory by the number of friends each has

    Returns a sorted (in decreasing order by number of friends) list 
    of 2-tuples, where each tuples has the person's name as the first element,
    the the number of friends as the second element.
    """
    friends_list = []

    # ------------ BEGIN YOUR CODE ------------

    for person, friends in my_dir.items():
        friends_list.append((person, len(friends)))

    friends_list.sort(key=lambda x: (-x[1], x[0]))
    

    # ------------ END YOUR CODE ------------

    return friends_list


def make_team_roster(person, my_dir):
    """Returns str encoding of a person's team of friends of friends
    Args:
        person (str): the team leader's name
        my_dir (Dict): dictionary of all relationships

    Returns:
        str of the form 'A_B_D_G' where the underscore '_' is the
        separator character, and the first substring is the 
        team leader's name, i.e. A.  Subsequent unique substrings are 
        friends of A or friends of friends of A, in ASCII order
        and excluding the team leader's name (i.e. A only appears
        as the first substring)

    Notes:
    - Team is drawn from only within two circles of A -- friends of A, plus 
      their immediate friends only
    """
    assert person in my_dir
    label = person

    # ------------ BEGIN YOUR CODE ------------
    #add all the friends and freinds of freinds to the list,
    #sort the set, then add them to the string
    visitedFriends = []
    for friend in my_dir[person]:
        if friend not in visitedFriends:
            visitedFriends.append(friend)
        for friendOfFriend in my_dir[friend]:
            if friendOfFriend != person:
                if friendOfFriend not in visitedFriends:
                    visitedFriends.append(friendOfFriend)

    visitedFriends.sort()
    for firend in visitedFriends:
        label += "_" + firend



    # ------------ END YOUR CODE ------------

    return label


def find_smallest_team(my_dir):
    """Find team with smallest size, and return its roster label str
    - if ties, return the team roster label that is first in ASCII order
    """
    smallest_teams = []

    # ------------ BEGIN YOUR CODE
    '''
        my plan:
    loop through the entire dictionary, backwards (this can make it faster)
    add team members to the set and check for the length of the set
    if the length of the current is less then the current min replace
    the min leader with current person, if there is a tie check who's
    name is first in ASCII
    '''
    teamRoaster = set()
    minLeader = ""
    minLength = float('inf')
    for person in reversed(my_dir):
        #only checks if the original friends list isnt more than the current min
        if len(my_dir[person]) < minLength:
            for friend in my_dir[person]:
                if friend not in teamRoaster:
                    teamRoaster.add(friend)
                for friendOfFriend in my_dir[friend]:
                    if friendOfFriend not in teamRoaster:
                        teamRoaster.add(friendOfFriend)
            if minLeader == "": #if its the first person
                minLeader = person
                minLength = len(teamRoaster)
            elif minLength > len(teamRoaster): #if the length of the team is the new min
                minLeader = person
                minLength = len(teamRoaster)
            elif minLength == len(teamRoaster): # if they equal
                if minLeader > person: # check for alphabetical
                    minLeader = person
                    minLength = len(teamRoaster)
    if minLeader != "":
        smallest_teams.append(make_team_roster(minLeader, my_dir))

    # ------------ END YOUR CODE

    return smallest_teams[0] if smallest_teams else ""



if __name__ == '__main__':
    # To run and examine your function calls

    print('\n1. run load_pairs')
    my_pairs = load_pairs('myfriends.txt')
    print(my_pairs)

    print('\n2. run make_friends_directory')
    my_dir = make_friends_directory(my_pairs)
    print(my_dir) 

    print('\n3. run find_all_number_of_friends')
    print(find_all_number_of_friends(my_dir))

    print('\n4. run make_team_roster')
    my_person = 'DARTHVADER'   # test with this person as team leader
    team_roster = make_team_roster(my_person, my_dir)
    print(team_roster) 

    print('\n5. run find_smallest_team')
    print(find_smallest_team(my_dir))

    print('\n6. run Friends iterator')
    friends_iterator = Friends(my_dir)
    for num, pair in enumerate(friends_iterator):
        print(num, pair)
        if num == 10:
            break
    # since index 0 we read 11 elements
    print(len(list(friends_iterator)) + num + 1)
