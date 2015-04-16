from World import World
from Bot import Bot
from trash import SumoArena

rows = cols = 30
canvas = 1
bot1 = Bot(cols / 2 - 5, rows / 2, 1, 1, "blue", canvas)
bot2 = Bot(cols / 2 + 5, rows / 2, 1, 1, "green", canvas)
world = World(rows, cols, bot1, bot2)
arena = SumoArena(world)
