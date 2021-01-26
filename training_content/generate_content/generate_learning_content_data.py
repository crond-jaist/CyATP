import re
from SPARQLWrapper import SPARQLWrapper, JSON
import json
import wikipedia
import time
import requests
import sys
import importlib
importlib.reload(sys)


class Query_children:
    __doc__ = '''use SPARQL to query children from DBpedia'''

    def __init__(self, keyword):
        self.keyword = keyword

    def query_children(self, keyword):
        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        queryString = """
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                    PREFIX category: <http://dbpedia.org/resource/Category:>


                    SELECT DISTINCT ?child  ?childlabel  
                    WHERE{
                        ?child skos:broader <http://dbpedia.org/resource/Category:keyword>;
                                rdfs:label   ?childname.
                        FILTER (LANG(?childname) = 'en')
                        BIND (?childname AS ?childlabel)
                    }
                    """.replace("keyword", self.keyword)
        sparql.setQuery(queryString)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        childlist = []
        for result in results["results"]["bindings"]:
            childlist.append(result["childlabel"]["value"].replace(" ", "_"))
        return childlist




def getKeywordText(data_level):
    no_define_word = []
    for i in range(len(data_level)):
        keyword = data_level[i]['Keyword']
        try:
            temp = wikipedia.summary(keyword)
            text = re.sub(u"\\(.*?\\)", "", temp).replace('\n', '')
            data_level[i].update({'Text': text})
            print(i, keyword)

        except wikipedia.DisambiguationError as a:
            no_define_word.append(keyword)

        except wikipedia.PageError as e:
            no_define_word.append(keyword)

        except requests.exceptions.ConnectionError:
            time.sleep(5)
            print('continue..')
            continue
        except UnicodeEncodeError:
            continue

    filename = 'DATA_3_KLT.json'
    with open(filename, 'w') as file_obj:
        json.dump(data_level, file_obj)
    print("\tFile DATA_3_KLT.json generated.")

    filename = 'no_text_keyword.json'
    with open(filename, 'w') as file_obj:
        json.dump(no_define_word, file_obj)
    print("\tFile no_text_keyword.json generated.")


def getContent(keyword):

    # 1. from DBpedia get keywords and edges
    # 2. generate concept map
    # 3. from wikipedia get texts

    print("Start build the \"Computer Security\" Concept map. Please waiting...")

    # store concept in keys
    keys = []
    keys.append(keyword)
    # store relationship in edges
    edges = []

    # query children of the keyword, store in childlist
    children = Query_children(keyword)
    childlist = children.query_children(keyword)
    # print("childlist:", childlist)

    for child in childlist:
        if re.findall('\(.*?\)', child):
            continue
        elif re.findall('\'', child):
            continue
        elif re.findall('\+', child):
            continue
        elif re.findall('\/', child):
            continue
        elif re.findall('\&', child):
            continue
        elif re.findall('\.', child):
            continue
        elif re.findall('\!', child):
            continue
        elif re.findall('：', child):
            continue
        elif re.findall('\"', child):
            continue
        else:
            edges.append((child, keyword))

    # for i in range(len(childlist)) doesn't work
    # since the length of childlist keep changing
    i = 0
    while i < len(childlist):
        # print(i)

        if re.findall('\(.*?\)', childlist[i]):
            continue
        elif re.findall('\'', childlist[i]):
            continue
        elif re.findall('\+', childlist[i]):
            continue
        elif re.findall('\/', child):
            continue
        elif re.findall('\&', child):
            continue
        elif re.findall('\.', child):
            continue
        elif re.findall('\!', child):
            continue
        elif re.findall('：', child):
            continue
        elif re.findall('\"', child):
            continue
        else:
            child = childlist[i]
            if child not in keys:
                keys.append(child)

            # query children of the children
            grand_children = Query_children(child.replace(" ", "_"))
            results = grand_children.query_children(
                child.replace(" ", "_"))
            # print('reselts', child, results)
            for result in results:
                if re.findall('\(.*?\)', result):
                    continue
                elif re.findall('\'', result):
                    continue
                elif re.findall('\+', result):
                    continue
                elif re.findall('\/', result):
                    continue
                elif re.findall('\&', result):
                    continue
                elif re.findall('\.', result):
                    continue
                elif re.findall('\!', result):
                    continue
                elif re.findall('\"', result):
                    continue
                else:
                    grandchild = result
                    if grandchild not in childlist:
                        if grandchild not in keys:
                            # change the size of concept of here.len(keys) < total number + 1
                            # !TODO improve the concept map size control method
                            # - [x] 0:  1, 1
                            # - [x] 1:  22, 23
                            # - [x] 2 : 103, 126
                            # - [x] 3 :205, 331
                            # - [x] 4: 287， 618
                            # - [x] 5: 266， 884
                            # - [x] 6: 463, 1347
                            # - [x] 7: 1293, 2640
                            if len(keys) < 1348:
                                childlist.append(grandchild)
                                edges.append((grandchild, child))
            i = i + 1
            # print("edges", edges)
            # print("keys", keys)
            #print('Number ', len(keys), ' keyword was added.')
    print('\tNumber of ', len(keys), 'keywords was added.')

    data_KL = []
    for key_level in range(len(keys)):
        if key_level == 0:
            d1 = {"Keyword": keys[key_level].replace('_', ' ')}
            d2 = {"Level": 0}
            d1.update(d2)
            data_KL.append(d1)

        if key_level > 0  and key_level <23:
            d1 = {"Keyword": keys[key_level].replace('_', ' ')}
            d2 = {"Level": 1}
            d1.update(d2)
            data_KL.append(d1)
        if key_level >= 23  and key_level <126:
            d1 = {"Keyword": keys[key_level].replace('_', ' ')}
            d2 = {"Level": 2}
            d1.update(d2)
            data_KL.append(d1)

        if key_level >= 126  and key_level <331:
            d1 = {"Keyword": keys[key_level].replace('_', ' ')}
            d2 = {"Level": 3}
            d1.update(d2)
            data_KL.append(d1)

        if key_level >=331  and key_level <618:
            d1 = {"Keyword": keys[key_level].replace('_', ' ')}
            d2 = {"Level": 4}
            d1.update(d2)
            data_KL.append(d1)

        if key_level >=618  and key_level <884:
            d1 = {"Keyword": keys[key_level].replace('_', ' ')}
            d2 = {"Level": 5}
            d1.update(d2)
            data_KL.append(d1)

        if key_level >=884  and key_level <1347:
            d1 = {"Keyword": keys[key_level].replace('_', ' ')}
            d2 = {"Level": 6}
            d1.update(d2)
            data_KL.append(d1)

        if key_level >=1347  and key_level <2640:
            d1 = {"Keyword": keys[key_level].replace('_', ' ')}
            d2 = {"Level": 7}
            d1.update(d2)
            data_KL.append(d1)


    # save keyword and level information
    filename = 'tDATA_2_KL.json'
    with open(filename, 'w') as file_obj:
        json.dump(data_KL, file_obj)
    print('\tFile DATA_2_KL.json generated.')

    # generate computer_security.txt
    temp = []
    l0 = {"0": keys[:1]}
    temp.append(l0)
    l1 = {"1": keys[1:23]}
    temp.append(l1)
    l2 = {"2": keys[23:126]}
    temp.append(l2)
    l3 = {"3": keys[126:331]}
    temp.append(l3)
    l4 = {"4": keys[331:618]}
    temp.append(l4)
    l5 = {"5": keys[618:884]}
    temp.append(l5)
    l6 = {"6": keys[884:1347]}
    temp.append(l6)
    l7 = {"7": keys[1347:2640]}
    temp.append(l7)
    #print(temp)
    with open("Computer_security.txt", "w") as f:
        f.write(str(temp))
    print('\tFile Computer_security.txt generated.')


    all_KL = []
    for index, cont in enumerate(temp):
        for j in cont[str(index)]:
            d1 = {'name': j}
            d2 = {'category': index}
            d1.update(d2)
            all_KL.append(d1)
    nodes = {"data": all_KL}

    all_edges = []
    for index, cont in enumerate(edges):
        value = 'level' + str(index)
        dd = {"source": cont[1], "target": cont[0], "value": value}
        all_edges.append(dd)

    link = []
    for each_eage_index in range(len(all_edges)):
        source = all_edges[each_eage_index]['source'].replace("_", " ")
        target = all_edges[each_eage_index]['target'].replace("_", " ")
        value = all_edges[each_eage_index]['value'].replace("_", " ")

        for idd in range(len(data_KL)):
            if (source == data_KL[idd]['Keyword']):
                source = idd
                value = "level" + str(data_KL[idd]['Level'])
                break

        for ttt in range(len(data_KL)):
            if (target == data_KL[ttt]['Keyword']):
                target = ttt
                break
        sm_dic = {"source": source, "target": target, "value": value}
        link.append(sm_dic)

    Link = {"links": link}

    map = []
    map.append(nodes)
    map.append(Link)


    filename = 'concept_map.json'
    with open(filename, 'w') as file_obj:
        json.dump(map, file_obj)
    print("\tConcept map generate.")

    print("Start get each keywords text")
    getKeywordText(data_KL)
    print("Content prepare finished.")




if __name__ == '__main__':
    keyword = 'Computer_security'
    concept_map = getContent(keyword)

