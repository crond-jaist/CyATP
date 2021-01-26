from py2neo import Graph, Node, Relationship
from config import graph

with open("../data/create_map.txt") as f:
    for line in f.readlines():
        rela_array = line.strip("\n").split(",")
        print(rela_array)
        graph.run("MERGE(p: Keyword{level:'%s',Name: '%s'})" % (rela_array[3], rela_array[0]))
        graph.run("MERGE(p: Keyword{level:'%s',Name: '%s'})" % (rela_array[4], rela_array[1]))
        graph.run(
            "MATCH(e: Keyword), (cc: Keyword) \
            WHERE e.Name='%s' AND cc.Name='%s'\
            CREATE(e)-[r:%s{relation: '%s'}]->(cc)\
            RETURN r" % (rela_array[0], rela_array[1], rela_array[2], rela_array[2])

        )
        
