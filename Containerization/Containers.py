from Docker import DockerHelper
from Properties import properties
from Node import Node

dHelper = DockerHelper()


def runMongodbContainer():
    name = 'node_mongo'
    dHelper.removeContainer(name)
    container = dHelper.containerBuilder() \
        .name(name) \
        .image('mongo') \
        .ports({'27017/tcp': 27018}) \
        .detach() \
        .create()
    container.stop()
    container.start()


def removeOldCOntainers(nodes):
    print('Removing old containers')
    for node in nodes:
        dHelper.removeContainer(node.name)


def createImage():
    name = properties['image_name']
    path = '../'
    print('creating image')

    preImg = dHelper.getImage(name)

    newImg = dHelper.imageBuilder() \
        .tag(name) \
        .path(path) \
        .cache(True) \
        .build()

    # if preImg is not None:
    #     print('removing old image')
    #     preImg.remove()

    return newImg


def createNetwork():
    print('creating network')
    network = dHelper.getNetwork(properties['network']['name'])

    return dHelper.networkBuilder().create(properties['network']['name'],
                                           properties['network']['subnet']) if network is None else network


def createContainers(nodes):
    print('creating containers')
    network = dHelper.getNetwork(properties['network']['name'])
    imageName = properties['image_name']

    for node in nodes:
        containerOptions = node.containerOptions

        portKey = '{}/tcp'.format(containerOptions['port'])
        portValue = containerOptions['port']

        command = ['python', 'src/main.py']

        command.append('command')

        for k in node.args:
            for v in node.args[k]:
                command.append('{}:{}'.format(k, v))

        builder = dHelper.containerBuilder() \
            .image(imageName) \
            .name(node.name) \
            .ports({portKey: portValue}) \
            .networkMode('bridge') \
            .env(node.env) \
            .detach() \
            .cpu(containerOptions['cpu']) \
            .memory(containerOptions['memory'])

        print('option', builder.data)
        print('command', command)

        builder.create(command)

        network.connect(node.name, ipv4_address=containerOptions['ip'])


def runContainers(nodes):
    for node in nodes:
        container = dHelper.getContainer(node.name)
        print('running ', node.name, 'container')
        print('node', node.name)
        container.stop()
        container.start()


def make(nodes):
    print('making containers')
    runMongodbContainer()

    removeOldCOntainers(nodes)

    createImage()

    createNetwork()

    createContainers(nodes)

    runContainers(nodes)

def finish(nodes):
    for node in nodes:
        container = dHelper.getContainer(node.name)
        print('finishing ', node.name, 'container')
        print('node', node.name)
        container.stop()
