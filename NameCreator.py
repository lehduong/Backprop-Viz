class NameCreator:
    __instance = None
    def __init__(self):
        """ Virtually private constructor. """
        if NameCreator.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            NameCreator.__instance = self
            self.count = 0
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if NameCreator.__instance == None:
            NameCreator()
        return NameCreator.__instance
    @staticmethod
    def getName():
        i = NameCreator.getInstance()
        c = i.count
        i.count += 1
        return "@temp_"+str(c)
    @staticmethod
    def resetCounter():
        i = NameCreator.getInstance()
        c = i.count
        i.count = 0