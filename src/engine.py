import json

def run():
    with open("tests/System Test/Data/Basic Story.json") as json_data:
        json_object = json.load(json_data)
        json_data.close()
        json_list = list(json_object)
        index_lookup = { key: index for index, key in enumerate(json_list)}
        CURRENT_INDEX = 0
        while CURRENT_INDEX < len(json_list):
            current_node = json_object[json_list[CURRENT_INDEX]]

            if json_list[CURRENT_INDEX][:5] == "SCENE":            
                for i in current_node["TEXT"]: # Print all the text
                    print(i)
    
            if json_list[CURRENT_INDEX][:8] == "DECISION":
                for i in current_node["TEXT"]: # Print all the text
                    print(i)
                ans = int(input(""))
                CURRENT_INDEX = index_lookup[current_node["GOTO"][ans - 1]] - 1


            if json_list[CURRENT_INDEX][:6] == "COMBAT":
                for i in current_node["TEXT"]: # Print all the text
                    print(i)

            
            # Progress to next node
            CURRENT_INDEX += 1

        print(json_list[CURRENT_INDEX - 1])

        

if __name__ == "__main__":
    run()