import os
import json

filepath = os .getcwd()

with open(os.path.join(filepath, 'data', 'concept_text.json'), 'r', encoding='utf-8') as f:
    data = json.load(f)


def get_keyword_profile(o_name):
    s = ''
    name = o_name.replace(' ', '_')
    try:
        for i in data[name]:
            dir = {}
            st = "<dt class = \"basicInfo-item name\" >" + str(i)+"</dt>"+" \
            <dd class = \"basicInfo-item value\" >" + str(data[name][i])+"</dd >"
            s += st
            dir[str(i)] = str(data[name][i])
            text = str(data[name][i])
    except:
        text = 'nodefine'

    return {'data': [o_name], 'define': [text]}

