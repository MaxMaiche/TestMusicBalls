import numpy as np

G = 0.1

class Window:
    def __init__(self,s):
        self.size = s
        self.ballRadius = s//200
        self.balls = []
        self.addBall()


    def __str__(self):
        return f"Window size: {self.size}"

    def addBall(self):
        x = np.random.randint(self.size//2-self.size//4,self.size//2+self.size//4)
        y = np.random.randint(self.size//2-self.size//4,self.size//2+self.size//4)
        self.balls.append(Ball(self,x,y,self.ballRadius))


    def step(self):
        for b in self.balls:
            b.direction[1] += G
            if b.isCollidingWithWall(self):
                if np.random.rand() < 0.80:
                    self.addBall()
                normal = np.array([b.x - self.size // 2, b.y - self.size // 2])
                normal /= np.linalg.norm(normal)
                b.direction -= 2 * np.dot(b.direction, normal) * normal


        suppress = []
        for i in range(len(self.balls)):
            for j in range(i+1,len(self.balls)):
                if i in suppress or j in suppress:
                    continue
                b1 = self.balls[i]
                b2 = self.balls[j]
                dist = np.sqrt((b1.x-b2.x)**2 + (b1.y-b2.y)**2)
                if dist < b1.r + b2.r:
                    normal = np.array([b1.x - b2.x, b1.y - b2.y])
                    normal /= np.linalg.norm(normal)
                    resFight = b1.fightWith(b2)
                    if resFight == 0:
                        b1.direction -= 2 * np.dot(b1.direction, normal) * normal
                        b2.direction -= 2 * np.dot(b2.direction, normal) * normal
                    elif resFight == 1:
                        suppress.append(j)
                    else:
                        suppress.append(i)




        self.balls = [b for i, b in enumerate(self.balls) if i not in suppress]

        for b in self.balls:
            b.x += b.direction[0]
            b.y += b.direction[1]
            b.r += 0.01



class Ball:
    def __init__(self,w, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        self.wSize = w.size
        self.inertia = [1,1]
        self.direction = np.random.rand(2)*2-1
        self.color = tuple(map(int,np.random.rand(3)*255))

        # print(self)

    def __str__(self):
        return f"Ball at ({self.x},{self.y}) with radius {self.r} and color {self.color}\n Direction: {self.direction} Inertia: {self.inertia}"


    def isCollidingWithWall(self, w):
        return np.sqrt((self.x-self.wSize//2)**2 + (self.y-self.wSize//2)**2) > w.size // 2 - self.r

    def fightWith(self, b):
        tot = self.r + b.r
        winProb = self.r / tot

        drawProb = 0.3
        if np.random.rand() < drawProb:
            return 0

        if np.random.rand() < winProb:
            self.r += b.r // 5
            return 1
        else:
            b.r += self.r // 5
            return 2