import pygame
import math
import random

from pygame import mixer

# Primeira Parte: Setup lógico do game
# Segunda Parte: loop do game

# INICIAR TODOS OS MÓDULOS PYGAMES
pygame.init()
clock = pygame.time.Clock()
fps = 60

# Criar a janela
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("World War III")
icone_aviao = pygame.image.load("aviao guerra.png")
pygame.display.set_icon(icone_aviao)


# Menu principal
def show_menu():
    menu_background = pygame.image.load("background_menu (2).png")
    play_button = pygame.image.load("play_button.png")

    while True:
        screen.blit(menu_background, (0, 0))
        screen.blit(play_button, (300, 300))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # saber se o fechou a janela
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 300 <= mouse_pos[0] <= 500 and 300 <= mouse_pos[1] <= 400:
                    return

        pygame.display.update()


show_menu()

# tela de fundo
background = pygame.image.load("background (1).png")


# Jogador
soldado_img = pygame.image.load("soldado (5) (1).png")
soldadoX = 370
soldadoY = 520
soldadoX_change = 0

# avião inimigo
aviaoinimigo_img = []
aviaoinimigoX = []
aviaoinimigoY = []
aviaoinimigoX_change = []
aviaoinimigoY_change = []
numero_inimigos = 6

for i in range(numero_inimigos):
    aviaoinimigo_img.append(pygame.image.load("Aviao32.png"))
    aviaoinimigoX.append(random.randint(0, 735))
    aviaoinimigoY.append(random.randint(50, 150))
    aviaoinimigoX_change.append(3)
    aviaoinimigoY_change.append(40)

# Bala
bala_img = pygame.image.load("bullet (1).png")
balaX = 0
balaY = 520
balaX_change = 0
balaY_change = 10
bala_state = "ready"

# Pontuaçao
valor_pontuacao = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# Game over
over_font = pygame.font.Font('freesansbold.ttf', 64)

#funções
def mostrar_pontuacao(x, y):
    pontuacao = font.render("Pontuação :" + str(valor_pontuacao), True, (0, 0, 0))
    screen.blit(pontuacao, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))


def soldado(x, y):
    screen.blit(soldado_img, (x, y))


def aviaoinimigo(x, y, i):
    screen.blit(aviaoinimigo_img[i], (x, y))


def fire_bala(x, y):
    global bala_state
    bala_state = "fire"
    screen.blit(bala_img, (x + 28, y + 20))


def ehcolisao(aviaoinimigoX, aviaoinimigoY, balaX, balaY):  # formula para achar distancia entre dois pontos
    distancia = math.sqrt((math.pow(aviaoinimigoX - balaX, 2)) + (math.pow(aviaoinimigoY - balaY, 2)))
    if distancia < 27:
        return True
    return False


# Criar loop
running = True
while running:
    screen.fill((0, 0, 0))  # cores rgb
    clock.tick(fps)
    screen.blit(background, (0, 0))  # Tela de fundo

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # saber se o fechou a janela
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # movimentação do soldado
                soldadoX_change = -5
            if event.key == pygame.K_RIGHT:
                soldadoX_change = 5
            if event.key == pygame.K_SPACE:
                if bala_state is "ready":  # ver se a bala esta na tela
                    som_bala = mixer.Sound("Gunshot-Sound-Effect.wav")
                    som_bala.play()
                    balaX = soldadoX
                    fire_bala(balaX, balaY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                soldadoX_change = 0

    # checando movimentos e limites do soldado
    soldadoX += soldadoX_change

    if soldadoX <= 0:
        soldadoX = 0
    elif soldadoX >= 736:
        soldadoX = 736

    # checando movimentos e limites do aviao inimigo
    for i in range(numero_inimigos):

        # game over
        if aviaoinimigoY[i] > 440:
            for j in range(numero_inimigos):
                aviaoinimigoY[j] = 2000
            game_over_text()
            break
        aviaoinimigoX[i] += aviaoinimigoX_change[i]
        if aviaoinimigoX[i] <= 0:
            aviaoinimigoX_change[i] = 3
            aviaoinimigoY[i] += aviaoinimigoY_change[i]
            aviaoinimigo_img[i] = pygame.transform.flip(aviaoinimigo_img[i], True, False)


        elif aviaoinimigoX[i] >= 736:
            aviaoinimigoX_change[i] = -3
            aviaoinimigoY[i] += aviaoinimigoY_change[i]
            aviaoinimigo_img[i] = pygame.transform.flip(aviaoinimigo_img[i], True, False)

        # colisao
        colisao = ehcolisao(aviaoinimigoX[i], aviaoinimigoY[i], balaX, balaY)
        if colisao:
            som_explosao = mixer.Sound("-game-explosion.wav")
            som_explosao.play()
            balaY = 520
            bala_state = "ready"
            valor_pontuacao += 1
            aviaoinimigoX[i] = random.randint(0, 735)
            aviaoinimigoY[i] = random.randint(50, 150)

        aviaoinimigo(aviaoinimigoX[i], aviaoinimigoY[i], i)

    # mover a bala
    if balaY <= 0:
        balaY = 520
        bala_state = "ready"

    if bala_state is "fire":
        fire_bala(balaX, balaY)
        balaY -= balaY_change

    soldado(soldadoX, soldadoY)
    mostrar_pontuacao(textX, textY)
    pygame.display.update()
