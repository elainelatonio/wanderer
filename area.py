from tkinter import *
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

    def draw_map(self, canvas, IMG_SIZE, root):
        line_num = 0
        for line in self.map_array:
            for index in range(len(line)):
                if line[index] == self.map.floor:
                    canvas.create_image(IMG_SIZE * index, IMG_SIZE * line_num, image=root.floor, anchor=NW)
                elif line[index] == self.map.wall:
                    canvas.create_image(IMG_SIZE * index, IMG_SIZE * line_num, image=root.wall, anchor=NW)
            line_num += 1

    def generate_monsters(self):
        for num_of_skeletons in range(random.randint(2, 5)):
            row = random.randint(0, 9)
            column = random.choice([index for index, tile in enumerate(self.map_array[row]) if tile == self.map.floor])
            Skeleton(column, row, self.level)
        row = random.randint(0, 9)
        column = random.choice([index for index, tile in enumerate(self.map_array[row]) if tile == self.map.floor])
        self.boss = Boss(column, row, self.level)
        self.hide_key(Monster.monsters)
        # delete this - printing out monster list in interpreter to check
        for monster in Monster.monsters:
            print(f"{monster.name}(Level {monster.level}) HP: {monster.get_hp()} | DP: {monster.dp} | "
                  f"SP: {monster.sp} has_key: {monster.has_key}")

    def hide_key(self, monsters):
        skeletons = [monster for monster in monsters if type(monster).__name__ == "Skeleton"]
        random.choice(skeletons).has_key = True

    def place_characters(self, canvas, IMG_SIZE, root, hero):
        for monster in Monster.monsters:
            canvas.create_image(monster.x * IMG_SIZE, monster.y * IMG_SIZE, image=getattr(root, monster.img),
                                anchor=NW)
        canvas.create_image(hero.x * IMG_SIZE, hero.y * IMG_SIZE,
                            image=getattr(root, hero.img), anchor=NW)

    def get_surrounding_tiles(self, position):
        x = position[0]
        y = position[1]
        left_tile = self.map_array[y][x - 1] if x - 1 >= 0 else None
        right_tile = self.map_array[y][x + 1] if x + 1 < 10 else None
        up_tile = self.map_array[y - 1][x] if y - 1 >= 0 else None
        down_tile = self.map_array[y + 1][x] if y + 1 < 10 else None
        surrounding_tiles = [left_tile, up_tile, right_tile, down_tile]
        return surrounding_tiles


if __name__ == '__main__':
    pass
