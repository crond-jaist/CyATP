from neo_db.config import graph, CA_LIST
import difflib
from scripts.get_5_data import get_all_keywords

# load all the keyword to a directory
# if can not query the keyword, recommend a similar keyword
keywords = get_all_keywords()

def query(name):
    # print(name)
    name_ = name.capitalize()
    data = graph.run(
    "match(p )-[r]->(n:Keyword{Name:'%s'}) return  p.Name,r.relation,n.Name,p.level,n.level\
        Union all\
    match(p:Keyword{Name:'%s'}) -[r]->(n) return p.Name, r.relation, n.Name, p.level, n.level" % (name_, name_)
    )
    data = list(data)
    # print(data)
    # json_data = get_json_data(data)
    return get_json_data(data, name)


def get_json_data(data, name):
    json_data = {'data': [], "links": []}
    d = []

    if(data == []):
        try:
            close_item = difflib.get_close_matches(name, keywords, 5, cutoff = 0.5)
            # print(close_item)
            #query(close_item)
        except:
            close_item = []

        return close_item
    else:
        for i in data:
            #print(i["p.Name"], i["r.relation"], i["n.Name"], i["p.level"], i["n.level"])
            d.append(i['p.Name'] + "/" + i['p.level'])
            d.append(i['n.Name'] + "/" + i['n.level'])
            d = list(set(d))
        name_dict = {}
        count = 0
        for j in d:
            j_array = j.split("/")

            data_item = {}
            name_dict[j_array[0]] = count
            count += 1
            data_item['name'] = j_array[0]
            data_item['category'] = CA_LIST[j_array[1]]
            json_data['data'].append(data_item)
        for i in data:
            link_item = {}

            link_item['source'] = name_dict[i['p.Name']]

            link_item['target'] = name_dict[i['n.Name']]
            link_item['value'] = i['r.relation']
            json_data['links'].append(link_item)
    #print(json_data)
        return json_data


