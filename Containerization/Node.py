import json
from Properties import properties

def gather(dictionary,keys):
    data = {}
    for key in keys:
        if key in dictionary:
            data[key] = dictionary[keys]
    return data

class Node:
    def __init__(self,name=None,env={},args={},containerOptions={},initialization=[]):
        self.name = name
        self.neighbors = []
        self.env = env.copy()
        self.args = args.copy()
        self.initialization = initialization.copy()
        self.containerOptions = containerOptions.copy()

    def addNeighbor(self,n):
        self.neighbors.append(n)
        return self

    def setContainerOption(self,key,val):
        self.containerOptions[key] = val
        return self

    def mergeContainerOption(self,options):
        for k in options:
            self.setContainerOption(k,options[k])
        return self

    def setEnv(self,key,val):
        if val is None:
            self.env[key] = ''
        elif val is True:
            self.env[key] = 'True'
        elif val is False:
            self.env[key] = 'False'
        else : self.env[key] = str(val)
        return self

    def mergeEnv(self,envs):
        for k in envs:
            self.setEnv(k,envs[k])
        return self

    def setArgs(self,key,val):
        if key not in self.args:
            self.args[key] = []

        if isinstance(val,list):
            for v in val: self.setArgs(key,v)
            return self
        if val is None or val is False:
            self.args[key].append(False)
        elif val is True:
            self.args[key].append(True)
        else:
            self.args[key].append(val)

        return self

    def mergeArgs(self, args):
        for k in args:
            self.setArgs(k, args[k])
        return self

    def printNeighbors(self):
        print('Name:',self.name)
        print('Env:',self.env)
        print('Cont:',self.containerOptions)
        print('Args:',self.args)
        print('Init:',self.initialization)

        for n in self.neighbors:
            print('   name:',n.name)
            print('   env:',n.env)
            print('   cont:',n.containerOptions)
            print('   args:',n.args)
            print('   init:',n.initialization)

    @staticmethod
    def generate(properties):

        topology = properties['topology']
        nodes = [Node('{}{}'.format(properties['container_name_prefix'],i)) for i in range(len(topology))]

        for key in properties['containers']:
            node = nodes[int(key)]

            containerProperties = properties['containers'][key]

            node.initialization = containerProperties['initialization']

            node.mergeEnv(containerProperties['env'])

            node.setEnv('rounds',properties['rounds'])

            node.setEnv('instance_name',node.name)

            node.setEnv('self_url','http://localhost:{}'.format(node.env['port']))

            node.setEnv('container_url','http{}://{}:{}'.format('s' if properties['network']['https'] else '',containerProperties['container']['ip'],containerProperties['container']['port']))

            node.mergeContainerOption(containerProperties['container'])

            node.mergeArgs(containerProperties['args'])


        for i in range(len(topology)):
            row = topology[i]
            for j in range(len(row)):
                if row[j]:
                    nodes[i].addNeighbor(nodes[j])
                    nodes[i].setArgs('neighbors','http{}://{}:{}'.format('s' if properties['network']['https'] else '',nodes[j].containerOptions['ip'],nodes[j].containerOptions['port']))


        return nodes

    @staticmethod
    def generateFromPath(path):
        f = open(path, 'r')
        data = f.read()
        f.close()

        return Node.generate(json.loads(data))

    @staticmethod
    def printList(l):
        for n in l:
            n.printNeighbors()
            print('-------------------------')
    @staticmethod
    def network(path):
        f = open(path, 'r')
        data = f.read()
        f.close()
        return json.loads(data)['network']

nodes = Node.generate(properties)
