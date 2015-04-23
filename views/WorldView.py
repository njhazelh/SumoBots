from Tkconstants import ALL
from models import WORLD_STATES

class WorldView:
    def __init__(self, world, canvas, width, height):
        self.world = world
        self.canvas = canvas
        self.width = width
        self.height = height

    def render(self):
        c = self.canvas
        c.delete(ALL)

        c.create_rectangle(0, 0,
                           self.width, self.height,
                           fill="#555")

        c.create_text(self.width / 2, self.height / 8,
                      text="SumoBot Arena",
                      tag="title", fill="#eee",
                      font=("Helvetica", 18, "bold"))

        c.create_oval(120, 120, 480, 480, width=5, fill="#333", outline="")

        self.draw_grid(c)
        
	c.create_text(self.width - 80, self.height - 100,
                      text="[r] = restart\n[m] = main menu",
                      fill="#eee",
                      font=("Helvetica", 10))
        
        c.create_rectangle(0, self.height - 60,
                           self.width, self.height,
                           fill="#333")

        c.create_text(50, self.height - 30,
                      text="Turn:",
                      fill="#aaa",
                      font=("Helvetica", 14, "bold"))

        if self.world.current_player == 1:
            bot = self.world.bot1
        else:
            bot = self.world.bot2

        player_text = "Player %d (%s)" % (self.world.current_player, bot.get_type_name())
        c.create_text(100, self.height - 30,
                          anchor="w",
                          text=player_text,
                          fill=bot.color,
                          font=("Helvetica", 14, "normal"))

        if self.world.state == WORLD_STATES.GAME_OVER:
            c.create_text(self.width / 2,
                          self.height / 2 - 40,
                          text="Game Over!",
                          fill="#eee",
                          font=("Helvetica", 32, "bold"))
            winner = self.world.bot1 if self.world.winner == 1 else self.world.bot2
            c.create_text(self.width / 2,
                          self.height / 2 + 30,
                          text="Player %d wins" % (winner.id),
                          fill=winner.color,
                          font=("Helvetica", 16, "bold"))
        elif self.world.state == WORLD_STATES.COUNT_DOWN:
            text = self.world.count if self.world.count != 0 else "FIGHT!"
            c.create_text(self.width / 2,
                          self.height / 2,
                          text=text,
                          fill="#c22",
                          font=("Helvetica", 32, "bold"))
        c.update()

    def draw_grid(self, canvas):
        for row in xrange(self.world.rows):
            for col in xrange(self.world.cols):
                self.draw_sumo_cell(canvas, row, col)

    def draw_sumo_cell(self, canvas, row, col):
        cellSize = self.width / self.world.cols
        left = col * cellSize
        right = left + cellSize
        top = row * cellSize
        bottom = top + cellSize

        grid = self.world.sumo_grid
        bot1 = self.world.bot1
        bot2 = self.world.bot2
        debug = self.world.debug

        # For debugging: color background and draw cell values.
        if debug:
            # color the cells where the robots are intending to go
            buff = 3
            if bot1.intended_at(col,row) and self.world.current_player == 2:
              canvas.create_rectangle(left-buff, top-buff, right+buff, bottom+buff, fill="yellow")
            if bot2.intended_at(col,row) and self.world.current_player == 1:
              canvas.create_rectangle(left-buff, top-buff, right+buff, bottom+buff, fill="yellow")

            if (grid[row][col] == -9):
                # draw out-of-bounds
                canvas.create_rectangle(left, top, right, bottom, fill="#c22")
            else:
                # draw in-bounds
                canvas.create_rectangle(left, top, right, bottom)
            # Draw the text in the cell
            canvas.create_text(left + cellSize / 2, top + cellSize / 2,
                               text=str(grid[row][col]), font=("Helvetica", 14, "bold"))

        if (bot1.is_at(col, row)):
            # Draw the Bot
            canvas.create_rectangle(left, top, right, bottom, fill=bot1.color)
        elif (bot2.is_at(col, row)):
            # Draw the Enemy Bot
            canvas.create_rectangle(left, top, right, bottom, fill=bot2.color)
