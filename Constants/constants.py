import configparser

class Constant:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.STUDENT_PATH = config['PATHS']['STUDENT_PATH']
        self.PROFESSOR_PATH = config['PATHS']['PROFESSOR_PATH']
