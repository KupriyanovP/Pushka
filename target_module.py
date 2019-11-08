from random import randrange as rnd


class target():
    def __init__(self,canv):
        self.points = 0
        self.live = 1
        self.id = canv.create_oval(0, 0, 0, 0)
        self.new_target(canv)
        self.v = rnd(0, 5)

    def new_target(self, canv):
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = 'red'
        canv.coords(self.id, x-r, y-r, x+r, y+r)
        canv.itemconfig(self.id, fill=color)

    def hit(self, canv, points=1):
        canv.coords(self.id, -10, -10, -10, -10)
        self.points += points

    def move(self, canv):
        if self.live:
            self.y += self.v
            canv.coords(self.id,
                        self.x - self.r,
                        self.y - self.r,
                        self.x + self.r,
                        self.y + self.r)
            if self.y + self.r >= 600 or self.y - self.r <= 0:
                self.v = -self.v
        else:
            canv.coords(self.id, 0, 0, 0, 0)