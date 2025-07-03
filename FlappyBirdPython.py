# Pygame entende que todos os objetos se tornam um retângulo por padrão
import pygame
import os
import random

# -*-*-*-*-*-*-
# Base Game
largura_tela = 500
altura_tela = 800

img_cano = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
img_chao = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
img_background = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
imgs_passaro =[
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]
# tela de pontuação
pygame.font.init()
fonte_pontos = pygame.font.SysFont('arial', 30)

# -*-*-*-*-*-*-
# Class/ Definições - o que e como irá se mover.
# Ações são os Métodos!

class Passaro:
    IMGS = imgs_passaro
    #animações da rotação
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5 #?

    #atributos: -- começa como:
    def __init__(self, x ,y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y #?
        self.tempo = 0 
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # Calcular o movimento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        # Restringir o Deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2 #Começar o jogo melhor (ele pula um pouco +)

        self.y +=  deslocamento

        # Angulo do Passaro
        if deslocamento < 0 or self.y < (self.altura + 50): # animação
        #(Vira no momento ideal)
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA

        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        # Definir Qual img do passaro será:
        self.contagem_imagem += 1
        # bater a asa
        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO*4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # Se o passaro estiver caindo, não bater asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        # Desenhar a imagem
        imagem_rotaciado = pygame.transform.rotate(self.imagem, self.angulo)
        posicao_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotaciado.get_rect(center= posicao_centro_imagem)
        # "colou dentro da tela"
        tela.blit(imagem_rotaciado, retangulo.topleft) # img que deseja, posição

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)

class Cano: # Vou querer mudar um pouco
    #atributos:
    DISTANCIA = 200
    VELOCIDADE = 5 # quero mudar com o tempo

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(img_cano, False, True) # (img, x, y)
        self.CANO_BASE = img_cano
        self.passou = False
        self.definir_altura()

    def definir_altura(self): #tem algo errado...?
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y)) #x,y
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y)) 

        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Chao:
    #atributos:
    VELOCIDADE = 5
    LARGURA = img_chao.get_width()
    IMAGEM = img_chao

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0: # mudar de pos o chão
            self.x1 = self.x2 + self.LARGURA

        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

def desenha_tela(tela, passaros, canos, chao, pontos):
    tela.blit(img_background, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)#?DESENHAR (+passaros para IA)
    for cano in canos:
        cano.desenhar(tela)
                                                             #CORES RGB
    texto =fonte_pontos.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (largura_tela - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()


def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((largura_tela, altura_tela))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30) #30 padrão FPS

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular() #?
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i) # é a posição de cada pássaro
                if not cano.passou and passaro.x > cano.x: #?
                    cano.passou = True
                    adicionar_cano = True
            cano.mover() 
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano) #criou uma lista vazia
        
        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))

        for cano in remover_canos:
            canos.remove(cano)
        
        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

        desenha_tela(tela, passaros, canos, chao, pontos)

# Padrão
if __name__ == '__main__':
    main()