from random import randrange as rnd, choice, triangular
import tkinter as tk
import math
import time

# print (dir(math))

root = tk.Tk()
fr = tk.Frame(root)
root.geometry('800x600')
canv = tk.Canvas(root, bg='white')
canv.pack(fill=tk.BOTH, expand=1)


class ball():
    def __init__(self, x=40, y=450):
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(['blue', 'green', 'red', 'brown'])
        self.id = canv.create_oval(
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r,
                fill=self.color
        )
        self.live = 100

    def set_coords(self):
        canv.coords(
                self.id,
                self.x - self.r,
                self.y - self.r,
                self.x + self.r,
                self.y + self.r
        )

    def move(self):
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
        self.set_coords()
        self.live -= 1
        if self.live == 0:
            canv.coords(self.id, 0, 0, 0, 0)

    def hittest(self, obj):
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        return False


class gun():
    def __init__(self):
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.id = canv.create_line(20, 450, 50, 420, width=7)

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        global balls, bullet
        bullet += 1
        new_ball = ball()
        new_ball.r += 5
        self.an = math.atan((event.y-new_ball.y) / (event.x-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls += [new_ball]
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event=0):
        if event:
            self.an = math.atan((event.y-450) / (event.x-20))
        if self.f2_on:
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')
        canv.coords(self.id, 20, 450,
                    20 + max(self.f2_power, 20) * math.cos(self.an),
                    450 + max(self.f2_power, 20) * math.sin(self.an)
                    )

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            canv.itemconfig(self.id, fill='orange')
        else:
            canv.itemconfig(self.id, fill='black')


class target():
    def __init__(self):
        self.points = 0
        self.live = 1
        self.id = canv.create_oval(0, 0, 0, 0)
        self.new_target()
        self.v = triangular(0, 5)

    def new_target(self):
        x = self.x = rnd(600, 780)
        y = self.y = rnd(300, 550)
        r = self.r = rnd(2, 50)
        color = self.color = 'red'
        canv.coords(self.id, x-r, y-r, x+r, y+r)
        canv.itemconfig(self.id, fill=color)

    def hit(self, points=1):
        canv.coords(self.id, -10, -10, -10, -10)
        self.points += points

    def move(self):
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


t1 = target()
t1.new_target()
targets = [(t1, 1)]
screen1 = canv.create_text(400, 300, text='', font='28')
points = canv.create_text(30, 30, text='0', font='28')
g1 = gun()
bullet = 0
balls = []
respawn = time.time()
target_num = 1

def new_game(event=''):
    global gun, t1, screen1, balls, bullet, target_num, respawn
    bullet = 0
    count = 0
    balls = []
    canv.bind('<Button-1>', g1.fire2_start)
    canv.bind('<ButtonRelease-1>', g1.fire2_end)
    canv.bind('<Motion>', g1.targetting)
    z = 0.03
    while targets or balls:
        del_balls = []
        for t, n in targets:
            t.move()
        for b_num in range(len(balls)):
            b = balls[b_num]
            b.move()
            for t, n in targets:
                if b.hittest(t) and t.live:
                    t.live = 0
                    t.hit()
                    count += 1
                    canv.itemconfig(screen1, text='Вы уничтожили цель ' + str(n) + ' за ' + str(bullet) + ' выстрелов')
                    canv.itemconfig(points, text=str(count))
            if b.live == 0:
                del_balls.append(b_num)
        for b_num in del_balls:
            balls.pop(b_num)
        if time.time() - respawn >= 3:
            target_num += 1
            targets.append((target(), target_num))
            targets[-1][0].new_target()
            respawn = time.time()
        canv.update()
        time.sleep(0.03)
        g1.targetting()
        g1.power_up()
    canv.itemconfig(screen1, text='')
    canv.delete(gun)
    #root.after(750, new_game)


def mainloop():
    global gun, t1, screen1, balls, bullet
    new_game()
    mainloop()


mainloop()
