"""
manage application logs
"""
import datetime

class Log:
    def __init__(self):
        pass

    def log(self, data):
        dt = datetime.datetime
        data = f'{dt} : {data}'
        print(data)