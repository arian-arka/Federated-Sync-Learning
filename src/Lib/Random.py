import string, random


class Random:
    @staticmethod
    def str(length=16, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def filename(length=16, extension=''):
        return Random.str(length) + '.' + extension if len(extension) > 0 else Random.str(length)

    @staticmethod
    def filenameWithRandomExt(length=16, lengthExtension=2):
        return Random.str(length) + '._' + Random.str(lengthExtension) + '_'
