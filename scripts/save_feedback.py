import json
import os

filepath = os.getcwd()

def save(data):
    # if not exists feedback_question.json, generate it
    if not os.path.exists(os.path.join(filepath, 'training_content/feedback', 'feedback_question.json')):
        os.system(r"touch {}".format('feedback_question.json'))

    with open(os.path.join(filepath, 'training_content/feedback', 'feedback_question.json'), 'r', encoding='utf8') as fp:
        file = json.load(fp)

    # if not repeat data, write it in the json file
    for i in range(len(data)):
        if data[i] not in file:
            file.append(data[i])
            with open(os.path.join(filepath, 'training_content/feedback', 'feedback_question.json'), 'w') as fp:
                json.dump(file, fp)
    return 'sava ok'

def save_survey(data):
    if not os.path.exists(os.path.join(filepath, 'training_content/feedback', 'feedback_survey_data.json')):
        os.system(r"touch {}".format('feedback_survey_data.json'))

    with open(os.path.join(filepath, 'training_content/feedback', 'feedback_survey_data.json'), 'r', encoding='utf8') as fp:
        file = json.load(fp)

    for i in range(len(data)):
        if data[i] not in file:
            file.append(data[i])
            with open(os.path.join(filepath, 'training_content/feedback', 'feedback_survey_data.json'), 'w') as fp:
                json.dump(file, fp)

    return 'sava survey ok'
