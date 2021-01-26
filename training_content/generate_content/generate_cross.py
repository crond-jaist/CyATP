# -*- coding: utf-8 -*-
import random, pprint, subprocess, tempfile, os, shutil, time, argparse
import json

# from file get words
def read_word_list(filename,word_len_limit):
    words = []
    with open(filename) as words_file:

        for line in words_file:
            if len(line)<=word_len_limit:
                words.append(line.strip())
    return words

# whether words can put into the grid
def is_valid(possibility, grid, words ,counts, length):
    i = possibility["location"][0]
    j = possibility["location"][1]
    word = possibility["word"]
    D = possibility["D"]

    # Is this word length over the grid
    if (D == "E" and j + len(word) > len(grid[0])) or (D == "S" and i + len(word) > len(grid)):
        return [False, []]

    for k, letter in enumerate(list(word)):
        if D is "E":
            if grid[i][j+k] != 0 and grid[i][j+k] != letter:
                return [False, []]
        if D is "S":
            if grid[i+k][j] != 0 and grid[i+k][j] != letter:
                return [False, []]


    if D is "E":
        if j > 0 and grid[i][j-1] != 0:
            return [False, []]
        if j+len(word) < len(grid[0]) and grid[i][j+len(word)] != 0:
            return [False, []]
    if D is "S":
        if i > 0 and grid[i-1][j] != 0:
            return [False, []]
        if i+len(word) < len(grid) and grid[i+len(word)][j] != 0:
            return [False, []]

    new_words = []
    for k, letter in enumerate(list(word)):
        if D is "E":
            if grid[i][j+k] == 0 and (i > 0 and grid[i-1][j+k] != 0 or i < len(grid)-1 and grid[i+1][j+k]):
                poss_word  = [letter]
                l = 1
                while i+l < len(grid[0]) and grid[i+l][j+k] != 0:
                    poss_word.append(grid[i+l][j+k])
                    l+=1
                l = 1
                while i-l > 0 and grid[i-l][j+k] != 0:
                    poss_word.insert(0, grid[i-l][j+k])
                    l+=1
                poss_word = ''.join(poss_word)
                if poss_word not in words:
                    return [False, []]
                new_words.append({"D": "S", "word":poss_word, "location": [i-l+1,j+k]})

        if D is "S":
            if grid[i+k][j] == 0 and (j > 0 and grid[i+k][j-1] != 0 or j < len(grid[0])-1 and grid[i+k][j+1]):
                poss_word  = [letter]
                l = 1
                while j+l < len(grid) and grid[i+k][j+l] != 0:
                    poss_word.append(grid[i+k][j+l])
                    l+=1
                l = 1
                while j-l > 0 and grid[i+k][j-l] != 0:
                    poss_word.insert(0, grid[i+k][j-l])
                    l+=1
                poss_word = ''.join(poss_word)
                if poss_word not in words:
                    return [False, []]
                new_words.append({"D": "E", "word":poss_word, "location": [i+k,j-l+1]})

    if len(words) == length:
        return [True, new_words]
    else:
        for k, letter in enumerate(list(word)):
            if D is "E":
                if grid[i][j+k] == letter:
                    return [True, new_words]
            if D is "S":
                if grid[i+k][j] == letter:
                    return [True, new_words]

    return [False, []]

# add the word into the grid
def add_word_to_grid(possibility, grid):
    """ Adds a possibility to the given grid, which is modified in-place.
    (see generate_grid)
    """
    # Import possibility to local vars, for clarity
    i = possibility["location"][0]
    j = possibility["location"][1]
    word = possibility["word"]

    # Word is left-to-right
    if possibility["D"] == "E":
        grid[i][j:len(list(word))+j] = list(word)
    # Word is top-to-bottom
    if possibility["D"] == "S":
        for index, a in enumerate(list(word)):
            grid[i+index][j] = a

# print the grid
def write_grid(grid, screen=False):
    print('\n')
    if screen is True:
        # Print grid to the screen
        for line in grid:
            for element in line:
                print(" {}".format(element), end="")
            print()
 

# generate the grid
def generate_grid_occupancy_max(words, dim, index,timeout=60, occ_goal=1):
    print("Generating {} grid with {} words.".format(dim, len(words)))
    temp_word = [word for word in words]
    start_time = time.time()
    occupancy = 0
    letter_counter = 0
    inter_counter = 1
    occupancy_max = 0
    occupancy_min = 1
    grid_with_max_occupancy = []
    while not(not words) and time.time() - start_time < timeout:
        added_words = []
        words = [word for word in temp_word]
        grid = [x[:] for x in [[0]*dim[1]]*dim[0]]
        try_state = True
        word_index = 0

        # first word is random, try to put the remaining words in the grid in order
        while word_index<len(words):
            counts = 0
            new_words = []
            valid = False
            while (not valid) and counts < 2*dim[0]*dim[1]:
                if len(words) == len(temp_word):
                    new = {"word": words[random.randint(0, len(words)-1)],
                            "location": [random.randint(0, dim[0]-1), random.randint(0, dim[1]-1)],
                            "D": "S" if random.random() > 0.5 else "E"}
                else:
                    new = {"word": words[word_index],
                            "location": [[counts % dim[0], counts // dim[1]] if counts<dim[0]*dim[1] else [(counts-dim[0]*dim[1]) % dim[0], (counts-dim[0]*dim[1]) // dim[1]]][0],
                            "D": "S" if counts > (dim[0]*dim[1])-1 else "E"}
                valid, new_words = is_valid(new, grid, words, counts, len(temp_word))
                counts += 1
            if valid:
                word_index = 0
                add_word_to_grid(new, grid)
                added_words.append(new)
                for word in new_words:
                    added_words.append(word)
                words.remove(new["word"])
                for word in new_words:
                    words.remove(word["word"])
                if len(words) == 0:
                    try_state = False
            else:
                word_index += 1
        occupancy = sum(x.count(0) for x in grid) / (dim[0]*dim[1])
        if occupancy < occupancy_min and occupancy > 0:
            occupancy_min = occupancy
            grid_with_min_occupancy = grid
            word_with_min_occupancy = added_words
        print("\rEmpty_rate: {:2.6f}.  Min_Empty_rate: {:2.6f}.  Number_of_attempts: {}".format(occupancy, occupancy_min, inter_counter), end='')
        inter_counter += 1

    # Report and return the grid
    # print("Built a grid of occupancy {}.".format(occupancy))
    return occupancy_min, occupancy, {"grid": grid, "words": added_words}, grid_with_min_occupancy, word_with_min_occupancy







#----------------------------------------------------------------------------------------------
# set the grid size
dd = 15
words = []

filepath = os.getcwd()
# Extract words with clue from the data
with open(os.path.join(filepath, '../../data', 'DATA_6_KLTQCP.json'), 'r', encoding='utf-8') as f:
    All_data = json.load(f)

for i in range(len(All_data)):
    try:
        if All_data[i]['Puzzle'] !=[]:
            for pu in All_data[i]['Puzzle']:
                words.append(pu['answer'])
    except:
        continue
words = list(dict.fromkeys(words))
print(len(words))
print(words)

#----------------------------------------------------------------------------------------------

words, dim= [x for x in words if len(x) > 2] , [dd, dd]
O_max, O__current, grid, grid_with_min_occupancy, word_with_min_occupancy = generate_grid_occupancy_max(words, dim, 1)

# 'E' means horizontal placement,'S' means vertical placement
write_grid(grid_with_min_occupancy, screen=True)
pprint.pprint(word_with_min_occupancy)

weizhi = sorted(word_with_min_occupancy,key=lambda t: t['location'], reverse=False)
print(weizhi)

puzzledata = []
position = 0
for i in weizhi:
    for item in word_with_min_occupancy:
        if(i == item['location']):

            if (item['D'] == 'E'):
                item['D'] = 'across'
            else:
                item['D'] = 'down'
            temp = {}

            # x coordinate
            # startx = item['location'][0] + 1
            startx = item['location'][1] + 1
            # y coordinate
            # starty = item['location'][1] + 1
            starty = item['location'][0] + 1

            # word
            answer = item['word']
            # information
            for i_temp in range(len(All_data)):
                if ((All_data[i_temp]['Level'] < 3 )and (All_data[i_temp]['Puzzle']!=[])):
                    for puzzle_info in All_data[i_temp]['Puzzle']:
                        if (answer == puzzle_info['answer']):
                            clue = str(puzzle_info['clue'])
            # clue = " "
            # Horizontal or vertical
            orientation = item['D']
            # position
            position = position + 1

            temp.update({'clue': clue})
            temp.update({'answer': answer})
            temp.update({'position': position})
            temp.update({'orientation': orientation})
            temp.update({'startx': startx})
            temp.update({'starty': starty})
            puzzledata.append(temp)

            print(temp)

print(puzzledata)



filename = 'crossword_puzzle_data.json'
with open(os.path.join(filepath, '../../data', filename), 'w') as file_obj:
    json.dump(puzzledata, file_obj)