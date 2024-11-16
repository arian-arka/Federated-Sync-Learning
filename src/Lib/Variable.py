class Convert:
    @staticmethod
    def toFloat(val):
        try :
            return float(val)
        except:
            return None
    @staticmethod
    def toInt(val):
        try :
            return int(val)
        except:
            return None

    @staticmethod
    def tryNumber(val):
        try :return int(val)
        except:pass
        try:return float(val)
        except:pass
        return val

    @staticmethod
    def tryAll(val):
        try :return int(val)
        except:pass
        try:return float(val)
        except:pass
        if val == 'True' or val == 'true':
            return True
        if val == 'False' or val == 'false':
            return False
        if val == '':
            return None
        return val

    @staticmethod
    def toNumber(val):
        val = Convert.toInt(val)
        return Convert.toFloat(val) if val is None else val


def gather(dictionary,keys):
    data = {}
    for key in keys:
        if key in dictionary:
            data[key] = dictionary[key]
    return data

def gatherExcept(dictionary,keys):
    data = {}
    for key in keys:
        if key not in dictionary:
            data[key] = dictionary[key]
    return data

def merge(d1,*args):
    d = d1.copy()
    for arg in args:
        d.update(arg)
    return d
