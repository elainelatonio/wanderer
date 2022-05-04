from dice import Dice
import random


class Character:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.type = type(self).__name__
        self.has_key = False

    def get_hp(self):
        return self._hp

    def set_hp(self, value):
        self._hp = value if value > 0 else 0
        return self._hp

    def move(self, x, y):
        self.x += x
        self.y += y

    def get_position(self):
        position = (self.x, self.y)
        return position

    def strike(self, attacker, defender):
        attacker.sv = attacker.sp + Dice.roll() * 2
        if attacker.sv > defender.dp:
            defender.set_hp(defender.get_hp() - (attacker.sv - defender.dp))

    def defend(self, attacker, defender):
        self.strike(defender, attacker)


class Hero(Character):

    def __init__(self):
        super().__init__()
        self.img = "hero_down"
        self.hp = self.set_hp(20 + 3 * Dice.roll())
        self.maxhp = self.hp
        self.dp = 2 * Dice.roll()
        self.sp = 5 + Dice.roll()
        self.set_level(1)
        self.name = self.type
        self.move_count = 0
        self.strike_count = 0

    def get_level(self):
        return self._level

    def set_level(self, value):
        self._level = value
        return self._level

    def move(self, x, y):
        self.x += x
        self.y += y
        self.move_count += 1

    def get_key(self, monster):
        self.just_got_key = False
        if monster.has_key and monster.get_hp() == 0:
            self.level_up()
            self.img = "hero_key"
            monster.has_key = False
            self.has_key = True
            self.just_got_key = True

    def level_up(self):
        self.set_level(self.get_level() + 1)
        self.maxhp += Dice.roll()
        self.dp += Dice.roll()
        self.sp += Dice.roll()
        self.img = "hero_levelup"

    def restore_hp(self):
        chance = random.randint(1, 100)
        if chance <= 10:
            self.set_hp(self.maxhp)
        elif chance <= 50:
            self.set_hp(min(self.maxhp, int(self.get_hp() + self.maxhp * 0.30)))
        elif chance > 50:
            self.set_hp(min(self.maxhp, int(self.get_hp() + self.maxhp * 0.10)))


class Monster(Character):
    monsters = []

    def __init__(self, x, y, area_level):
        super().__init__()
        self.set_level(area_level)
        self.x = x
        self.y = y
        self.img = str(self.type).casefold()
        self.hp = self.set_hp(2 * self.get_level() * Dice.roll())
        self.maxhp = self.hp
        self.dp = int(max(self.get_level() / 2 * Dice.roll(), 1))
        self.sp = self.get_level() * Dice.roll()
        Monster.monsters.append(self)
        self.number = Monster.monsters.index(self) + 1
        self.name = f"{self.type}{self.number}"

    def set_hp(self, value):
        if value <= 0:
            Monster.monsters.remove(self)
        self._hp = value if value > 0 else 0
        return self._hp

    def get_level(self):
        return self._level

    def set_level(self, area_level):
        chance = random.randint(1, 10)
        if chance <= 5:
            self._level = area_level
        elif chance <= 9:
            self._level = area_level + 1
        elif chance == 10:
            self._level = area_level + 2
            return self._level


class Skeleton(Monster):

    def __init__(self, x, y, level):
        super().__init__(x, y, level)


class Boss(Monster):

    def __init__(self, x, y, level):
        super().__init__(x, y, level)
        self.name = self.type
        self.hp = self.set_hp(2 * self.get_level() * Dice.roll() + Dice.roll())
        self.maxhp = self.hp
        self.dp = int(round(self.get_level() / 2 * Dice.roll() + Dice.roll() / 2))
        self.sp = self.get_level() * Dice.roll() + self.get_level()
