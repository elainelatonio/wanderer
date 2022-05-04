from tkinter import *
from game import *

IMG_SIZE = 72
WIDTH = 10 * IMG_SIZE
HEIGHT = 10.5 * IMG_SIZE


class Gui:

    def __init__(self):
        self.root = self.create_window()
        self.load_images()
        self.game = Game(self.root)

    def create_window(self):
        root = Tk()
        root.title('Wanderer Game')
        self.canvas = Canvas(root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        return root

    def draw_screen(self):
        self.canvas.delete("all")
        self.draw_map()
        self.canvas.create_rectangle(0, 10 * IMG_SIZE, 10 * IMG_SIZE, 10.5 * IMG_SIZE, fill="black")
        self.display_characters()
        self.display_text()

    def draw_map(self):
        line_num = 0
        for line in self.game.area.map_array:
            for index in range(len(line)):
                if line[index] == self.game.area.map.floor:
                    self.canvas.create_image(IMG_SIZE * index, IMG_SIZE * line_num, image=self.root.floor, anchor=NW)
                elif line[index] == self.game.area.map.wall:
                    self.canvas.create_image(IMG_SIZE * index, IMG_SIZE * line_num, image=self.root.wall, anchor=NW)
            line_num += 1

    def display_characters(self):
        for monster in Monster.monsters:
            self.canvas.create_image(monster.x * IMG_SIZE, monster.y * IMG_SIZE, image=getattr(self.root, monster.img),
                                     anchor=NW)
        self.canvas.create_image(self.game.hero.x * IMG_SIZE, self.game.hero.y * IMG_SIZE,
                                 image=getattr(self.root, self.game.hero.img), anchor=NW)

    def display_text(self):
        self.canvas.create_text(10, 10 * IMG_SIZE, fill="white",
                                text=f"{self.game.hero.name} (Level {self.game.hero.get_level()}) "
                                     f"HP: {self.game.hero.get_hp()}/{self.game.hero.maxhp} | "
                                     f"DP: {self.game.hero.dp} | SP: {self.game.hero.sp}",
                                anchor=NW)
        self.canvas.create_text(10, 10 * IMG_SIZE + 15, fill="deep sky blue",
                                text=f"LEVEL {self.game.area.level}", anchor=NW)
        self.canvas.create_text(70, 10 * IMG_SIZE + 15, fill="yellow",
                                text=f"{self.game.get_message()}", anchor=NW)
        if self.game.check_if_battle():
            self.canvas.create_text(470, 10 * IMG_SIZE, fill="white",
                                    text=f"{self.game.monster_to_fight.name} (Level {self.game.monster_to_fight.level}) "
                                         f"HP: {self.game.monster_to_fight.get_hp()}/{self.game.monster_to_fight.maxhp}"
                                         f" | DP: {self.game.monster_to_fight.dp} | "
                                         f"SP: {self.game.monster_to_fight.sp}", anchor=NW, width=240, justify=RIGHT)

    def load_images(self):
        dir = "images/"
        self.root.floor = PhotoImage(file=dir + "floor.png")
        self.root.wall = PhotoImage(file=dir + "wall.png")
        self.root.hero_down = PhotoImage(file=dir + "hero-down.png")
        self.root.hero_up = PhotoImage(file=dir + "hero-up.png")
        self.root.hero_right = PhotoImage(file=dir + "hero-right.png")
        self.root.hero_left = PhotoImage(file=dir + "hero-left.png")
        self.root.hero_fight = PhotoImage(file=dir + "hero-fight.png")
        self.root.hero_fight2 = PhotoImage(file=dir + "hero-fight2.png")
        self.root.hero_battle = PhotoImage(file=dir + "hero-battle.png")
        self.root.hero_dead = PhotoImage(file=dir + "hero-dead.png")
        self.root.hero_key = PhotoImage(file=dir + "hero-key.png")
        self.root.hero_heart = PhotoImage(file=dir + "hero-heart.png")
        self.root.hero_levelup = PhotoImage(file=dir + "hero-levelup.png")
        self.root.skeleton = PhotoImage(file=dir + "skeleton.png")
        self.root.boss = PhotoImage(file=dir + "boss.png")


if __name__ == "__main__":
    pass
