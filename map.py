import random

class Map:
    def __init__(self):
        self.map_array = ['fffffwwfff',
                          'fwwwfffffw',
                          'ffwwfwwwff',
                          'fwwwfffffw',
                          'fffffwwwff',
                          'fffwfwwwfw',
                          'fwwffwfffw',
                          'fwwwfffwfw',
                          'fffwffwfff',
                          'fffwfwwffw']
        random.shuffle(self.map_array)
        self.floor = "f"
        self.wall = "w"
