import zope.interface


class CompareAlgorithm(zope.interface.Interface):

    def similarity(self, x, y):
        pass

    def calculate(self, x):
        pass