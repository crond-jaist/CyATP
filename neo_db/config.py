from py2neo import Graph

graph = Graph(
    "http://localhost:7474",
     username="neo4j",
     password="123456"
)

CA_LIST = {"level0": 0, "level1": 1, "level2": 2, "level3": 3, "level4": 4, "level5": 5, "level6": 6, 'level7': 7}
