from pynput import keyboard
import os

gameover = False
UP = "w"
DOWN = "s"
LEFT = "a"
RIGHT = "d"
QUIT = "p"

PATH = "　"
WALL = "Ｘ"
PLAYER = "Ｏ"
EXIT = "門"


def load_map(file="map.txt"):
    """load map data from file"""
    m = []
    s = None
    with open(file, mode="r") as f:
        i = 0
        for ln in f:
            if ln.startswith("//"):
                continue
            row = []
            for j, square in enumerate(ln.strip()):
                if square == "#":
                    square = PATH
                elif square == "S":
                    assert not s, "only one start point allowed"
                    s = (i, j)
                    square = PATH
                elif square == "X":
                    square = WALL
                elif square == "E":
                    square = EXIT
                row.append(square)

            m.append(row)
            i += 1
    return m, s


class DungeonCrawler:
    up = keyboard.KeyCode.from_char(UP)
    down = keyboard.KeyCode.from_char(DOWN)
    left = keyboard.KeyCode.from_char(LEFT)
    right = keyboard.KeyCode.from_char(RIGHT)
    quit = keyboard.Key.esc

    def __init__(self):
        self.map, (self.x, self.y) = load_map()
        self.gameover = False
        self.game_render()

    world_map, start = load_map()

    def travel(self, x, y):
        new_x, new_y = self.x + x, self.y + y
        try:
            pos = self.map[new_x][new_y]

            if pos == PATH:
                self.x = new_x
                self.y = new_y

        except IndexError:
            return

    def game_render(self):
        os.system('cls' if os.name == 'nt' else 'clear')  # clear console to allow redraw
        for i, row in enumerate(self.map):
            for j, char in enumerate(row):
                if i == self.x and j == self.y:
                    print(PLAYER, end="")
                else:
                    print(char, end="")
            print("")
        print("Press esc to leave game")

    def on_press(self, key):
        """Processes player input"""
        if key == DungeonCrawler.quit:
            self.gameover = True
        elif key == DungeonCrawler.up:
            self.travel(-1, 0)
        elif key == DungeonCrawler.down:
            self.travel(1, 0)
        elif key == DungeonCrawler.left:
            self.travel(0, -1)
        elif key == DungeonCrawler.right:
            self.travel(0, 1)
        self.game_render()


if __name__ == '__main__':
    new_game = DungeonCrawler()
    while not new_game.gameover:
        with keyboard.Listener(on_press=new_game.on_press, on_release=lambda x: False, suppress=True) as listener:
            listener.join()
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"DK = {DungeonCrawler}, keyboard = {type(keyboard)}, keycode = {type(keyboard.KeyCode)}")
