from characters import *
from area import *
import random


class Game:

    def __init__(self, root):
        self.area = Area()
        self.hero = Hero()
        self.boss = self.area.boss
        self.root = root
        self.bind_arrow_keys()
        self.strike_count = 0
        self.set_message(f"Game! Kill the Boss and get the key to advance!")

    def get_message(self):
        return self._message

    def set_message(self, value):
        self._message = value
        return self._message

    def bind_arrow_keys(self):
        self.left_bind = self.root.bind('<Left>', lambda event, key="left", direction="x",
                                                         step=-1: self.hit_arrow_keys(event, key, direction,
                                                                                      step))
        self.right_bind = self.root.bind('<Right>', lambda event, key="right", direction="x",
                                                           step=1: self.hit_arrow_keys(event, key, direction,
                                                                                       step))
        self.up_bind = self.root.bind('<Up>', lambda event, key="up", direction="y",
                                                     step=-1: self.hit_arrow_keys(event, key, direction,
                                                                                  step))
        self.down_bind = self.root.bind('<Down>', lambda event, key="down", direction="y",
                                                         step=1: self.hit_arrow_keys(event, key, direction,
                                                                                     step))

    def unbind_arrow_keys(self):
        self.root.unbind('<left>', self.left_bind)
        self.root.unbind('<right>', self.right_bind)
        self.root.unbind('<up>', self.up_bind)
        self.root.unbind('<down>', self.down_bind)

    def hit_arrow_keys(self, event, key, direction, step):
        self.space_id = self.root.bind('<space>', self.hit_space)
        self.root.unbind('<space>', self.space_id)
        self.hero.img = "hero_" + key
        if self.allow_move(self.hero, (direction, step)):
            self.set_message("")
            if direction == "x":
                x, y = step, 0
            else:
                x, y = 0, step
            self.hero.move(x, y)
            self.random_move(Monster.monsters)
            if self.check_if_battle():
                self.hero.img = "hero_battle"
                self.start_battle()

    def check_tiles(self, character):
        surrounding_tiles = self.area.get_surrounding_tiles(character.get_position())
        directions = [("x",-1), ("y",-1), ("x",1), ("y",1)]
        surrounding_tiles = dict(zip(directions, surrounding_tiles))
        return surrounding_tiles

    def allow_move(self, character, direction):
        surrounding_tiles = self.check_tiles(character)
        if surrounding_tiles.get(direction) == self.area.map.floor:
            return True
        else:
            return False

    def random_move(self, characters):
        for monster in characters:
            surrounding_tiles = self.check_tiles(monster)
            possible_moves = [key for key, value in surrounding_tiles.items() if value == self.area.map.floor]
            random_move = random.choice(possible_moves)
            if random_move[0] == "x":
                x = random_move[1]
                y = 0
            elif random_move[0] == "y":
                x = 0
                y = random_move[1]
            monster.move(self.hero, x, y)

    def check_if_battle(self):
        battle = False
        for monster in Monster.monsters:
            if monster.get_position() == self.hero.get_position():
                self.monster_to_fight = monster
                battle = True
                return battle

    def start_battle(self):
        self.set_message(f"Battle with {self.monster_to_fight.name}, hit <space> to strike!")
        self.space_id = self.root.bind('<space>', self.hit_space)

    def hit_space(self, event):
        self.hero.img = self.count_strikes()
        self.hero.strike(self.hero, self.monster_to_fight)
        self.hero.get_key(self.hero, self.monster_to_fight)
        if self.check_if_clear_level():
            pass
        elif self.monster_to_fight.get_hp() == 0 and self.hero.just_got_key:
            self.set_message(f"Level up! You got the key!")
            self.end_battle()
        elif self.monster_to_fight.get_hp() == 0 and self.hero.just_got_key is False:
            self.hero.level_up()
            self.set_message(f"Level up!")
            self.end_battle()
        elif self.monster_to_fight.get_hp() > 0:
            self.monster_to_fight.defend(self.hero, self.monster_to_fight)
        if self.hero.get_hp() == 0:
            self.end_game()

    def count_strikes(self):
        self.strike_count += 1
        if self.strike_count % 2 == 0:
            return "hero_fight"
        else:
            return "hero_fight2"

    def check_if_clear_level(self):
        if "Boss" not in [monster.name for monster in Monster.monsters] and self.hero.has_key:
            self.clear_level()
            return True
        else:
            return False

    def end_battle(self):
        self.root.unbind('<space>', self.space_id)

    def end_game(self):
        self.set_message("GAME OVER")
        self.hero.img = "hero_dead"
        self.root.unbind('<space>', self.space_id)
        self.unbind_arrow_keys()

    def clear_level(self):
        del self.area
        Monster.monsters = []
        self.area = Area()
        self.hero.img = "hero_heart"
        self.hero.x, self.hero.y = 0, 0
        self.hero.has_key = False
        self.hero.set_hp(self.hero.maxhp)
        self.set_message(f"Entered next level! Kill the Boss and get the key to advance!")


if __name__ == '__main__':
    pass
