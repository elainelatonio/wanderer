from characters import *
from map import Map
import random


class Area:
    level = 1

    def __init__(self):
        self.level = Area.level
        self.map = Map()
        self.map_array = self.map.map_array
        self.generate_monsters()
        Area.level += 1

    def generate_monsters(self):
        for num_of_skeletons in range(random.randint(2, 5)):
            row = random.randint(0, 9)
            column = random.choice([index for index, tile in enumerate(self.map_array[row]) if tile == self.map.floor])
            Skeleton(column, row, self.level)
        row = random.randint(0, 9)
        column = random.choice([index for index, tile in enumerate(self.map_array[row]) if tile == self.map.floor])
        self.boss = Boss(column, row, self.level)
        self.hide_key(Monster.monsters)

    def hide_key(self, monsters):
        skeletons = [monster for monster in monsters if type(monster).__name__ == "Skeleton"]
        random.choice(skeletons).has_key = True

    def get_floor_tiles(self, position):
        x = position[0]
        y = position[1]
        left_tile = self.map_array[y][x - 1] if x - 1 >= 0 else None
        right_tile = self.map_array[y][x + 1] if x + 1 < 10 else None
        up_tile = self.map_array[y - 1][x] if y - 1 >= 0 else None
        down_tile = self.map_array[y + 1][x] if y + 1 < 10 else None
        surrounding_tiles = [left_tile, up_tile, right_tile, down_tile]
        directions = [("x", -1), ("y", -1), ("x", 1), ("y", 1)]
        surrounding_tiles = dict(zip(directions, surrounding_tiles))
        possible_moves = [key for key, value in surrounding_tiles.items() if value == self.map.floor]
        return possible_moves


