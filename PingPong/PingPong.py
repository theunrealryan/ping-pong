import pygame
import random

# Definir constantes
PONT_D = 0
pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('TimesNewRoman', 50)
PONT_E = 0
WIDTH = 800
HEIGHT = 600
BALL_RADIUS = 10
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH // 2
HALF_PAD_HEIGHT = PAD_HEIGHT // 2
LEFT = False
RIGHT = True

# Classe Paddle
class Paddle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0

    def draw(self, canvas):
        pygame.draw.rect(canvas, (255, 255, 255), (self.x - HALF_PAD_WIDTH, self.y - HALF_PAD_HEIGHT, PAD_WIDTH, PAD_HEIGHT))

    def update(self):
        self.y += self.vel
        if self.y < HALF_PAD_HEIGHT:
            self.y = HALF_PAD_HEIGHT
        elif self.y > HEIGHT - HALF_PAD_HEIGHT:
            self.y = HEIGHT - HALF_PAD_HEIGHT

# Classe Ball
class Ball:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.vel_x = 0.3 * random.choice([1, -1])
        self.vel_y = -0.3 * random.random()

    def draw(self, canvas):
        pygame.draw.circle(canvas, (255, 255, 255), (self.x, self.y), BALL_RADIUS)

    def update(self, p1, p2,pontosd, pontose):
        self.x += self.vel_x
        self.y += self.vel_y
        if self.y - BALL_RADIUS < 0 or self.y + BALL_RADIUS > HEIGHT:
            self.vel_y = -self.vel_y
        if self.x - BALL_RADIUS < PAD_WIDTH and abs(self.y - p1.y) < HALF_PAD_HEIGHT:
            self.vel_x = -self.vel_x
            self.vel_x *= 1.1
            self.vel_y *= 1.1
        elif self.x + BALL_RADIUS > WIDTH - PAD_WIDTH and abs(self.y - p2.y) < HALF_PAD_HEIGHT:
            self.vel_x = -self.vel_x
            self.vel_x *= 1.1
            self.vel_y *= 1.1
        elif self.x - BALL_RADIUS < 0:
            self.__init__()
            pontosd += 1
        elif self.x + BALL_RADIUS > WIDTH:
            pontose += 1
            self.__init__()
        return pontosd, pontose

# Inicialização do jogo
pygame.init()
canvas = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Criação dos objetos
paddle1 = Paddle(HALF_PAD_WIDTH, HEIGHT // 2)
paddle2 = Paddle(WIDTH - HALF_PAD_WIDTH, HEIGHT // 2)
ball = Ball()

# Loop principal do jogo
while True:
    canvas.fill((0, 0, 0))
    texto_e = FONTE_PONTOS.render(f"{PONT_E}", True, (255, 255, 255))
    texto_d = FONTE_PONTOS.render(f"{PONT_D}", True, (255, 255, 255))
    canvas.blit(texto_e, ((WIDTH - texto_e.get_width()) / 4, 20))
    canvas.blit(texto_d, ((WIDTH - texto_d.get_width()) / 4 * 3, 20))
    paddle1.draw(canvas)
    paddle2.draw(canvas)
    ball.draw(canvas)
    # Capturar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                paddle2.vel = -1
            elif event.key == pygame.K_DOWN:
                paddle2.vel = 1
            elif event.key == pygame.K_w:
                paddle1.vel = -1
            elif event.key == pygame.K_s:
                paddle1.vel = 1
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                paddle2.vel = 0
            elif event.key in (pygame.K_w, pygame.K_s):
                paddle1.vel = 0

    # Atualização dos objetos
    PONT_D, PONT_E = ball.update(paddle1, paddle2, PONT_D, PONT_E)
    paddle1.update()
    paddle2.update()
    pygame.display.update()