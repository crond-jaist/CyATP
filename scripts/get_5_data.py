import json
import os

filepath = os.getcwd()
with open(os.path.join(filepath, 'data', 'DATA_6_KLTQCP.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)

def get_all_info(name):
    info = []
    try:
        for i in range(len(data)):
            if(data[i]['Keyword'] == name):
                info = data[i]
    except:
        info = 'not find this information'
    return {'Keyword': [name], 'info': [info]}

def get_all_keywords():
    keywords = []
    for i in range(len(data)):
        keywords.append(data[i]['Keyword'])
    return keywords


def get_word_question(name):
    question = []
    try:
        for i in range(len(data)):
            if(data[i]['Keyword']==name):
                question = data[i]['Question']
    except:
        question = 'this keyword has not quesion'
    return {'Keyword': [name], 'question': [question]}


def get_all_question():
    All_Question = []
    for i in range(len(data)):
        try:
            for q in data[i]['Questions']:
                All_Question.append(q)
        except:
            continue
    return All_Question



def get_puzzle():
    All_puzzle = []
    for i in range(len(data)):
        try:
            for pu in data[i]['Puzzle']:
                All_puzzle.append(pu)
        except:
            continue

    return All_puzzle

