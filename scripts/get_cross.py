import json
import os
from random import choice
filepath = os.getcwd()

def get_crossword():
    with open(os.path.join(filepath, 'data', 'crossword_puzzle_data.json'), 'r', encoding='utf-8') as f:
        cross_all = json.load(f)
    cross = choice(cross_all)

    tempx = []
    tempy = []
    final_cross =[]
    for i in cross:
        if(i['orientation']=='across'):
            tempx.append(i)

        else:
            tempy.append(i)

    for xitem in tempx:
        final_cross.append(xitem)
    for yitem in tempy:
        final_cross.append(yitem)


    return final_cross
