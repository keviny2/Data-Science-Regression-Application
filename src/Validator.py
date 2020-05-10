import os

class Validator:
    @staticmethod
    def validateFilePath(inputFilePath):
        # checks for valid file path
        if not os.path.exists(inputFilePath):
            raise(Exception('File path invalid'))   