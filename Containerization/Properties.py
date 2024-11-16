import json

def loadProperties():
    f = open('nodes.json', 'r')
    nodes = json.loads(f.read())
    f.close()

    return nodes


properties = loadProperties()