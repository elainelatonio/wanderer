from characters import *
from area import *
import random


class Game:

    def __init__(self, root):
        self.root = root
        self.area = Area()
        self.hero = Hero()
        self.bind_arrow_keys()
        self.space_key_bound = False
        self.set_message("Game! Kill the Boss and get the key to advance!")

    def get_message(self):
        return self._message

    def set_message(self, value):
        self._message = value
        return self._message

    def bind_arrow_keys(self):
        self.left_bind = self.root.bind('<Left>', lambda event, key="left", axis="x",
                                                         step=-1: self.hit_arrow_keys(event, key, axis, step))
        self.right_bind = self.root.bind('<Right>', lambda event, key="right", axis="x",
                                                           step=1: self.hit_arrow_keys(event, key, axis, step))
        self.up_bind = self.root.bind('<Up>', lambda event, key="up", axis="y",
                                                     step=-1: self.hit_arrow_keys(event, key, axis, step))
        self.down_bind = self.root.bind('<Down>', lambda event, key="down", axis="y",
                                                         step=1: self.hit_arrow_keys(event, key, axis, step))

    def unbind_arrow_keys(self):
        self.root.unbind('<Left>', self.left_bind)
        self.root.unbind('<Right>', self.right_bind)
        self.root.unbind('<Up>', self.up_bind)
        self.root.unbind('<Down>', self.down_bind)

    def bind_space_key(self):
        self.space_id = self.root.bind('<space>', self.hit_space)
        self.space_key_bound = True

    def unbind_space_key(self):
        if self.space_key_bound:
            self.root.unbind('<space>', self.space_id)
            self.space_key_bound = False

    def hit_arrow_keys(self, event, key, axis, step):
        self.unbind_space_key()
        self.hero.img = "hero_" + key
        if self.allow_move(self.hero, (axis, step)):
            self.set_message("")
            self.take_step(self.hero, axis, step)
            self.random_move(Monster.monsters)
        if self.check_if_battle():
            self.start_battle()

    def allow_move(self, character, direction):
        possible_moves = self.area.get_floor_tiles(character.get_position())
        if direction in possible_moves:
            return True
        else:
            return False

    def take_step(self, character, axis, step):
        if axis == "x":
            x, y = step, 0
        else:
            x, y = 0, step
        character.move(x, y)

    def random_move(self, characters):
        if self.hero.move_count % 2 == 0:
            for monster in characters:
                possible_moves = self.area.get_floor_tiles(monster.get_position())
                (axis, step) = random.choice(possible_moves)
                self.take_step(monster, axis, step)

    def check_if_battle(self):
        battle = False
        for monster in Monster.monsters:
            if monster.get_position() == self.hero.get_position():
                self.monster_to_fight = monster
                battle = True
                return battle

    def start_battle(self):
        self.hero.img = "hero_battle"
        self.set_message(f"Battle with {self.monster_to_fight.name}, hit <space> to strike!")
        self.bind_space_key()

    def hit_space(self, event):
        self.hero.img = self.change_strike_img()
        self.hero.strike(self.hero, self.monster_to_fight)
        self.hero.get_key(self.monster_to_fight)
        self.end_battle()

    def end_battle(self):
        if self.monster_to_fight.get_hp() == 0 and self.hero.just_got_key:
            self.set_message("Level up! You got the key!")
            self.unbind_space_key()
        elif self.monster_to_fight.get_hp() == 0 and self.hero.just_got_key is False:
            self.hero.level_up()
            self.set_message("Level up!")
            self.unbind_space_key()
        if self.check_if_clear_level():
            pass
        elif self.monster_to_fight.get_hp() > 0:
            self.monster_to_fight.defend(self.hero, self.monster_to_fight)
        if self.hero.get_hp() == 0:
            self.end_game()

    def change_strike_img(self):
        self.hero.strike_count += 1
        if self.hero.strike_count % 2 == 0:
            return "hero_fight"
        else:
            return "hero_fight2"

    def check_if_clear_level(self):
        if "Boss" not in [monster.name for monster in Monster.monsters] and self.hero.has_key:
            self.clear_level()
            return True
        else:
            return False

    def end_game(self):
        self.set_message("GAME OVER")
        self.hero.img = "hero_dead"
        self.unbind_space_key()
        self.unbind_arrow_keys()

    def clear_level(self):
        del self.area
        Monster.monsters = []
        self.area = Area()
        self.hero.img = "hero_heart"
        self.hero.x, self.hero.y = 0, 0
        self.hero.has_key = False
        self.hero.restore_hp()
        self.set_message("Entered next level! Kill the Boss and get the key to advance!")

