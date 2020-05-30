import risar
import random
import math

class Oseba:
    def __init__(self):
        self.x = random.randint(0, risar.maxX)
        self.y = random.randint(0, risar.maxY)
        self.krog = risar.krog(1, 1, 5, barva= risar.zelena, sirina = 2)
        self.hitrost = random.randint(0,5)
        self.phi = random.random() * 2 * math.pi

        self.vx = self.hitrost * math.cos(self.phi)
        self.vy = self.hitrost * math.sin(self.phi)

    def premik(self):
        self.x += self.vx
        self.y += self.vy

        if 0 >= self.x:
            self.x = 1
            self.vx *= -1
        if self.x >= risar.maxX:
            self.x = risar.maxX - 1
            self.vx *= -1
        if 0 >= self.y:
            self.y = 1
            self.vy *= -1
        if self.y >= risar.maxY:
            self.y = risar.maxY - 1
            self.vy *= -1

        self.x = round(self.x)
        self.y = round(self.y)

        self.phi = math.atan2(self.vy,self.vx)
        self.phi += math.radians(random.random() * 40 - 20)
        self.vx = math.cos(self.phi)
        self.vy = math.sin(self.phi)

        self.krog.setPos(self.x, self.y)


sez_osebe = []
for i in range(100):
    o = Oseba()
    sez_osebe.append(o)

while True:
    for oseba in sez_osebe:
        oseba.premik()
    risar.cakaj(0.02)

