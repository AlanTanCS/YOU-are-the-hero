import json

class Story():
    def __init__(self, json_story, nodes, node_indexes):
        self.data = json_story
        self.nodes = nodes
        self.node_indexes = node_indexes

# class Player():
#     def __init__(self, json_object, nodes, node_indexes):
#         self.data = json_object
#         self.nodes = nodes
#         self.node_indexes = node_indexes

def update_current_node(path: str, new_node: int) -> None:
    with open(path) as json_data:
        json_object = json.load(json_data)

    json_object["CURRENT_NODE"] = new_node

    with open(path, "w") as json_data:
        json.dump(json_object, json_data, indent=4)

def read_json(path: str) -> Story:
    with open(path) as json_data:
        json_object = json.load(json_data)
        json_data.close()
        json_story = json_object["STORY"]
        nodes = list(json_story)

        # node_indexes used to efficiently jump between the scenes in decision nodes
        node_indexes = { key: index for index, key in enumerate(nodes)}

        return Story(json_story, nodes, node_indexes)
