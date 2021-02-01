

class BaseAnalyzer(object):
    
    def shift(self, data):
        raise NotImplementedError()

    def get_signal(self):
        raise NotImplementedError()