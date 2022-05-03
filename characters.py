from dice import Dice

class Character:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.level = 1
        self.move_count = 0
        self.type = type(self).__name__
        self.has_key = False

    def get_hp(self):
        return self._hp

    def set_hp(self, value):
        self._hp = value if value > 0 else 0
        return self._hp

    def move(self, x=0, y=0):
        self.x += x
        self.y += y
        self.move_count += 1

    def get_position(self):
        position = (self.x, self.y)
        return position

    def strike(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender
        self.attacker.sv = self.attacker.sp + Dice.roll() * 2
        if self.attacker.sv > self.defender.dp:
            self.defender.set_hp(self.defender.get_hp() - (self.attacker.sv - self.defender.dp))

    def defend(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender
        self.strike(self.defender, self.attacker)


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

    def get_level(self):
        return self._level

    def set_level(self, value):
        self._level = value
        return self._level

    def get_key(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender
        self.just_got_key = False
        if self.defender.has_key and self.defender.get_hp() == 0:
            self.level_up()
            self.attacker.img = "hero_key"
            self.defender.has_key = False
            self.attacker.has_key = True
            self.just_got_key = True

    def level_up(self):
        self.set_level(self.get_level() + 1)
        self.maxhp += Dice.roll()
        self.dp += Dice.roll()
        self.sp += Dice.roll()
        self.img = "hero_levelup"


class Monster(Character):
    monsters = []

    def __init__(self, x, y, area_level):
        super().__init__()
        self.level = area_level
        self.x = x
        self.y = y
        self.img = str(self.type).casefold()
        self.hp = self.set_hp(50)  # 2 * self.level * Dice.roll())
        self.maxhp = self.hp
        self.dp = round(self.level / 2 * Dice.roll())
        self.sp = self.level * Dice.roll()
        Monster.monsters.append(self)
        self.number = Monster.monsters.index(self) + 1
        self.name = f"{self.type}{self.number}"

    def set_hp(self, value):
        if value <= 0:
            Monster.monsters.remove(self)
        self._hp = value if value > 0 else 0
        return self._hp

    def move(self, hero, x, y):
        if hero.move_count % 2 == 0:
            self.x += x
            self.y += y


class Skeleton(Monster):

    def __init__(self, x, y, level):
        super().__init__(x, y, level)


class Boss(Monster):

    def __init__(self, x, y, level):
        super().__init__(x, y, level)
        self.name = self.type
        self.hp = self.set_hp(2 * self.level * Dice.roll() + Dice.roll())
        self.dp = self.level / 2 * Dice.roll() + Dice.roll() / 2
        self.sp = self.level * Dice.roll() + self.level
        self.maxhp = self.hp
