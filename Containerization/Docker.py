# docker inspect --type=image sample_node

import docker


class ImageBuilder:
    def __init__(self, client):
        self.client = client
        self.data = {
            'nocache': True,
            'rm': True,
            # 'timeout' : 3600,
            # 'buildargs': {},
            # 'container_limits': {},
        }

    def path(self, path):
        self.data['path'] = path
        return self

    def tag(self, tag):
        self.data['tag'] = tag
        return self

    def cache(self, status):
        self.data['nocache'] = not status
        return self

    def timeout(self, timeout):
        self.data['timeout'] = timeout
        return self

    def buildargs(self, buildargs):
        self.data['buildargs'] = buildargs
        return self

    def container_limits(self, container_limits):
        self.data['container_limits'] = container_limits
        return self

    def build(self):
        built = self.client.images.build(**self.data)
        return {
            'image': built[0],
            'logs': list(built[1]),
        }


class ContainerBuilder:
    def __init__(self, client):
        self.client = client
        self.data = {
            'image' : None,
            'args' : {}
        }


    def image(self, image):
        self.data['image'] = image
        return self

    def cpu(self, cpu_count=1):
        self.data['args']['cpu_count'] = cpu_count
        return self

    def network (self, network ):
        self.data['args']['network'] = network
        return self

    def ip(self, ip):
        self.data['args']['ip'] = ip
        return self

    def env(self,env):
        self.data['args']['environment'] = env
        return self

    def name (self,name ):
        self.data['args']['name'] = name
        return self

    def command (self,command ):
        self.data['args']['command'] = command
        return self

    def networkMode  (self,network_mode  ):
        self.data['args']['network_mode'] = network_mode
        return self

    def ports (self, ports ):
        self.data['args']['ports'] = ports
        return self

    def memory(self, mem_limit='128m'):
        self.data['args']['mem_limit'] = mem_limit
        return self

    def autoRemove(self, auto_remove):
        # enable auto-removal of the container on daemon side when the container’s process exits.
        self.data['args']['auto_remove'] = auto_remove
        return self

    def detach(self,detach =True):
        self.data['args']['detach'] = detach
        return self

    def create(self,command=None):
        _command = [] if command is None else command
        print('creating')
        print('   ',self.data['image'])
        print('   ',self.data['args'])
        return self.client.containers.create(self.data['image'],_command,**self.data['args'])

class NetworkBuilder:
    def __init__(self, client):
        self.client = client
    def create(self,name,subnet):
        ipam_pool = docker.types.IPAMPool(
            subnet=subnet,
        )
        ipam_config = docker.types.IPAMConfig(
            pool_configs=[ipam_pool]
        )
        return self.client.networks.create(name,driver="bridge",ipam=ipam_config)

class DockerHelper:
    def __init__(self):
        self.client = docker.from_env()

    def getImage(self, name):
        try:
            return self.client.images.get(name)
        except:
            return None

    def getNetwork(self,name):
        try:
            return self.client.networks.get(name)
        except:
            return None

    def getContainer(self, name):
        try:
            return self.client.containers.get(name)
        except:
            return None

    def imageBuilder(self):
        return ImageBuilder(self.client)

    def networkBuilder(self):
        return NetworkBuilder(self.client)

    def containerBuilder(self):
        return ContainerBuilder(self.client)

    def removeContainer(self,name):
        container = self.getContainer(name)
        if container is None:
            return
        container.stop()
        container.remove()

    def runContainer(self,name,**args):
        pass


