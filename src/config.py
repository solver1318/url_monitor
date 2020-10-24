import json


class Config:
    """
    Provide configurations from configJsonPath.
    """
    def __init__(self, configJsonPath):
        with open(configJsonPath) as data:
            self.__config = json.load(data)

    def getTargets(self):
        '''
        Get target URLs from config.
        :return: list: [target urls]
        '''
        return self.__config['TARGETS'] if 'TARGETS' in self.__config else []
