class Model:
    def __init__(self, props):
        self._props = props

    def get(self, key):
        return self._props[key]

    def set(self, key, value):
        self._props[key] = value
        return self

    def remove(self, key):
        if key in self._props:
            del self._props[key]
        return self
    def hasKey(self,key):
        return key in self._props


model = Model({})
