import Containers
from Node import nodes,Node
from Workflow import workflow

def run():
    Node.printList(nodes)

    Containers.make(nodes)

    workflow(nodes)

    Containers.finish(nodes)
    pass

if __name__ == '__main__':
    run()