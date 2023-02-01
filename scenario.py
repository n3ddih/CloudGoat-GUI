import json

class Scenario:
    def __init__(self, name, summary, size, difficulty):
        self.name = name
        self.summary = summary
        self. size = size
        self.difficulty = difficulty

    def get_detail_info(self):
        return self.__dict__