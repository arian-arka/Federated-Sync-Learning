from src.Lib.Variable import Convert
import sys


class Cli:
    @staticmethod
    def actualArgs(actual=True):
        return sys.argv[1:] if actual else sys.argv

    @staticmethod
    def parseKeyVals(args):
        all = {}
        for arg in args:
            parsed = Cli.parseKeyVal(arg)
            k = parsed[0]
            v = Convert.tryAll(parsed[1])
            if k in all:
                if isinstance(all[k], list):
                    all[k].append(v)
                else:
                    all[k] = [all[k],v]
            else:
                all[k] = v


        return all

    @staticmethod
    def parseKeyVal(arg):
        index = -1
        for i in range(len(arg)):
            if arg[i] == ':':
                index = i
                break
        return (arg,True) if index == -1 else (arg[:index], arg[index + 1:])

    @staticmethod
    def parse():
        return Cli.parseKeyVals(Cli.actualArgs())

    @staticmethod
    def parseWithFirstAsCommand():
        args = sys.argv[1:]
        if not len(args):
            return {
                'command' : None,
                'args' : None
            }
        command = args[0]
        if len(args) == 1:
            return {
                'command': command,
                'args': None
            }

        return {
            'command': command,
            'args': Cli.parseKeyVals(args[1:])
        }

withCommand = Cli.parseWithFirstAsCommand()

args = Cli.parse()


