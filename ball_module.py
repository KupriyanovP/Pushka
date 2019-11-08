from random import randrange as choice
class ball():
    def __init__(self, canv,  x=40, y=450):
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = 'blue'
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 100

    def set_coords(self,canv):
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self, canv):
        self.vy -= 2.5
        self.x += self.vx
        self.y -= self.vy
        if self.x + self.r >= 800:
            self.vx = - 0.7 * self.vx
            self.x = 800 - self.r
        if self.y + self.r >= 600:
            self.vy = - 0.7 * self.vy
            self.vx *= 0.7
            self.y = 600 - self.r
        self.set_coords(canv)
        self.live -= 1
        if self.live == 0:
            canv.coords(self.id, 0, 0, 0, 0)

    def hittest(self, obj):
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        return False
