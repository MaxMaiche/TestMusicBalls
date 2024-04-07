import model
from screeninfo import get_monitors
import pygame


pygame.init()
FPS = 144
pygame.display.set_caption("Music Balls")
monitor = get_monitors()[0]
HEIGHT = int(monitor.height*0.90)
WIN = pygame.display.set_mode((HEIGHT, HEIGHT))


def draw(w):
    WIN.fill((0,0,0))
    pygame.draw.circle(WIN, (255,255,255), (w.size//2,w.size//2), w.size//2, 2)


    for ball in w.balls:
        pygame.draw.circle(WIN, ball.color, (ball.x, ball.y), ball.r)

    pygame.display.update()


if __name__ == '__main__':
    monitor = get_monitors()[0]
    w = model.Window(HEIGHT)

    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        w.step()
        draw(w)


    pygame.quit()
