import json

class Story():
    def __init__(self, json_object, nodes, node_indexes):
        self.data = json_object
        self.nodes = nodes
        self.node_indexes = node_indexes

def read_json(path: str) -> Story:
    with open(path) as json_data:
        json_object = json.load(json_data)
        json_data.close()
        nodes = list(json_object)

        # node_indexes used to efficiently jump between the scenes in decision nodes
        node_indexes = { key: index for index, key in enumerate(nodes)}

        return Story(json_object, nodes, node_indexes)
