

class Enum(object):
    def __eq__(self, obj):
        return type(self) is obj