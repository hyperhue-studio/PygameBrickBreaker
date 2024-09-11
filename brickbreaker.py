# ===================
# Importaciones
# ===================
import pygame
import random

# ===================
# Inicializar Pygame
# ===================
radio = 10
pygame.init()

# ===================
# Configuraciones generales
# ===================

# Definición de colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)
MORADO = (255, 0, 255)
GRIS = (128, 128, 128)
AMARILLO = (255, 255, 0)

# Configuración de la pantalla
ANCHO = 800
ALTO = 600
PANTALLA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Brick Breaker")

# Definición de variables globales
VIDAS = 3
PUNTUACION = 0
NIVEL = 1
POTENCIADORES = ["Duplicar Pelota", "Alargar Base", "4 Pelotas", "Bolas Rapidas"]

# ===================
# Clases
# ===================
class Bloque(pygame.sprite.Sprite):
    def __init__(self, color, x, y, tipo):
        super().__init__()
        self.image = pygame.Surface([80, 30])
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.tipo = tipo
        self.impactos = 1 if tipo != "duro" else 2

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def explotar(self):
        bloques_a_destruir = []
        for bloque in bloques:
            # Verificar bloques arriba
            if self.rect.top - bloque.rect.bottom <= radio and abs(bloque.rect.centerx - self.rect.centerx) <= self.rect.width / 2:
                if bloque.tipo != "metal":
                    bloques_a_destruir.append(bloque)
            # Verificar bloques abajo
            if bloque.rect.top - self.rect.bottom <= radio and abs(bloque.rect.centerx - self.rect.centerx) <= self.rect.width / 2:
                if bloque.tipo != "metal":
                    bloques_a_destruir.append(bloque)
            # Verificar bloques a la izquierda
            if self.rect.left - bloque.rect.right <= radio and abs(bloque.rect.centery - self.rect.centery) <= self.rect.height / 2:
                if bloque.tipo != "metal":
                    bloques_a_destruir.append(bloque)
            # Verificar bloques a la derecha
            if bloque.rect.left - self.rect.right <= radio and abs(bloque.rect.centery - self.rect.centery) <= self.rect.height / 2:
                if bloque.tipo != "metal":
                    bloques_a_destruir.append(bloque)
        for bloque in bloques_a_destruir:
            bloque.kill()
    
    def activar_potenciador(self):
        potenciador = random.choice(POTENCIADORES)
        if potenciador == "Duplicar Pelota":
            ball2 = Bola(BLANCO, 10)
            ball2.rect.topleft = bola.rect.topleft
            ball2.velocidad = [random.randint(2, 5), random.randint(-5, 5)]  # Velocidad aleatoria

            todos_los_sprites.add(ball2)
            bloques_poder.add(ball2)
            bolas.add(ball2)

        elif potenciador == "Alargar Base":
            # Se modifican las dimensiones de la paleta
            paleta.image = pygame.Surface([200, 20])
            paleta.image.fill(ROJO)
            paleta.rect = paleta.image.get_rect(midbottom=(ANCHO//2, ALTO))

        elif potenciador == "4 Pelotas":
            # Se crean 3 nuevas pelotas
            ball2 = Bola(BLANCO, 10)
            ball2.rect.topleft = bola.rect.topleft
            ball2.velocidad = [random.randint(2, 5), random.randint(-5, 5)]

            ball3 = Bola(BLANCO, 10)
            ball3.rect.topleft = bola.rect.topleft
            ball3.velocidad = [random.randint(2, 5), random.randint(-5, 5)]

            ball4 = Bola(BLANCO, 10)
            ball4.rect.topleft = bola.rect.topleft
            ball4.velocidad = [random.randint(2, 5), random.randint(-5, 5)]
            
            todos_los_sprites.add(ball2)
            todos_los_sprites.add(ball3)
            todos_los_sprites.add(ball4)
            bloques_poder.add(ball2)
            bloques_poder.add(ball3)
            bloques_poder.add(ball4)
            bolas.add(ball2)
            bolas.add(ball3)
            bolas.add(ball4)

        elif potenciador == "Bolas Rapidas":
            #Se aumenta la velocidad de todas las bolas
            for ball in bolas:
                ball.velocidad = [random.randint(5, 10), random.randint(-10, 10)]
            for ball in bloques_poder:
                ball.velocidad = [random.randint(5, 10), random.randint(-10, 10)]

        print(f"Potenciador activado: {potenciador}")

class Bola(pygame.sprite.Sprite):
    def __init__(self, color, radio):
        super().__init__()
        self.image = pygame.Surface([radio*2, radio*2])
        self.image.fill(NEGRO)
        self.image.set_colorkey(NEGRO)
        pygame.draw.circle(self.image, color, (radio, radio), radio)
        self.rect = self.image.get_rect()
        self.velocidad = [random.randint(2, 5), random.randint(-5, 5)]
        self.horizontal_bounce_count = 0

    def update(self):
        self.rect.move_ip(self.velocidad)

        if self.rect.left <= 0 or self.rect.right >= ANCHO:
            self.velocidad[0] = -self.velocidad[0]
            self.horizontal_bounce_count += 1
        else:
            self.horizontal_bounce_count = 0
        
        if self.horizontal_bounce_count >= 3:
            self.velocidad[1] = self.velocidad[1] + (1 if self.velocidad[1] >= 0 else -1)
            self.horizontal_bounce_count = 0

        if self.rect.top <= 0:
            self.velocidad[1] = -self.velocidad[1]

        if self.rect.bottom >= ALTO:
            self.kill()  # Elimina la bola del grupo
            if not bloques_poder:  # Si no hay bolas en juego
                quitar_vida()

class Paleta(pygame.sprite.Sprite):
    def __init__(self, color, ancho, alto):
        super().__init__()
        self.image = pygame.Surface([ancho, alto])
        self.image.fill(color)
        self.rect = self.image.get_rect(midbottom=(ANCHO//2, ALTO))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-10, 0)
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(10, 0)

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(ANCHO, self.rect.right)

    def sigue_bola(self, bola):
        """
        Hace que la paleta siga la bola en el eje X.
        """
        if bola.rect.centerx > self.rect.centerx:
            self.rect.move_ip(min(10, bola.rect.centerx - self.rect.centerx), 0)
        elif bola.rect.centerx < self.rect.centerx:
            self.rect.move_ip(-min(10, self.rect.centerx - bola.rect.centerx), 0)

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(ANCHO, self.rect.right)

# Se crean los grupos de sprites
bloques = pygame.sprite.Group()
bloques_poder = pygame.sprite.Group()  # Aquí almacenas las bolas adicionales
bola = Bola(BLANCO, 10)
paleta = Paleta(ROJO, 120, 20)
todos_los_sprites = pygame.sprite.Group(bola, paleta)
bolas = pygame.sprite.Group()
bola = Bola(BLANCO, 10)
bolas.add(bola)

# ===================
# Funciones
# ===================

def quitar_vida():
    global VIDAS
    VIDAS -= 1
    if VIDAS == 0:
        game_over()
        generar_bloques()
    else:
        reset_bola_paleta()

def reset_bola_paleta():
    global bola
    bola.rect.topleft = ((ANCHO - radio*2) // 2, ALTO - paleta.rect.height - radio*2 - 10)
    bola.velocidad = [random.randint(2, 5), random.randint(-5, 5)]
    paleta.rect.midbottom = (ANCHO//2, ALTO)
    todos_los_sprites.add(bola)   # Agregar la bola al grupo de sprites
    bolas.add(bola)               # Agregar la bola al grupo de bolas


def game_over():
    global VIDAS, PUNTUACION, NIVEL
    print(f"Juego terminado. Puntuación: {PUNTUACION}, Nivel: {NIVEL}")
    menu()
    VIDAS = 3
    PUNTUACION = 0
    NIVEL = 1

def reset():
    global VIDAS
    bola.rect.topleft = ((ANCHO - radio*2) // 2, ALTO - paleta.rect.height - radio*2 - 10)
    bola.velocidad = [random.randint(2, 5), random.randint(-5, 5)]
    paleta.rect.midbottom = (ANCHO//2, ALTO)
    generar_bloques()

def generar_bloques():
    global NIVEL
    NIVEL += 1
    bloques.empty()
    for i in range(5):
        for j in range(6):
            tipo = random.choice(["normal", "duro", "metal", "bomba", "potenciador"])
            colores = {"normal": VERDE, "duro": AZUL, "metal": GRIS, "bomba": ROJO, "potenciador": AMARILLO}
            color = colores[tipo]
            bloque = Bloque(color, 100 + j * 90, 50 + i * 40, tipo)
            bloques.add(bloque)

def menu():
    global player, player2
    fuente = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        PANTALLA.fill(NEGRO)
        menu_text = fuente.render("1 - Solo, 2 - Modo AI", True, BLANCO)
        PANTALLA.blit(menu_text, (ANCHO // 2 - menu_text.get_width() // 2, ALTO // 2 - menu_text.get_height() // 2))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            main()
        elif keys[pygame.K_2]:
            mainAI()

        pygame.display.update()

# Inicialización de grupos de sprites
bloques = pygame.sprite.Group()
bola = Bola(BLANCO, 10)
paleta = Paleta(ROJO, 120, 20)
todos_los_sprites = pygame.sprite.Group(bola, paleta)

reset()

reloj = pygame.time.Clock()

# Bucle principal del juego para solo
def main():
    global PUNTUACION, VIDAS, NIVEL

    reset_bola_paleta()  # Asegurarse de que la bola y la paleta estén en sus posiciones iniciales
    generar_bloques()
    while VIDAS > 0:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()

        todos_los_sprites.update()

        # Lógica de colisión
        # Primero, colisión con la bola principal
        if pygame.sprite.collide_rect(bola, paleta):
            bola.velocidad[1] = -bola.velocidad[1]

        # Luego, colisión con las bolas adicionales
        for ball in bloques_poder:
            if pygame.sprite.collide_rect(ball, paleta):
                ball.velocidad[1] = -ball.velocidad[1]

        bloques_colisionados = pygame.sprite.spritecollide(bola, bloques, False)
        for bloque in bloques_colisionados:
            # Cambiar dirección de la bola al colisionar con un bloque
            bola.velocidad[1] = -bola.velocidad[1]
            
            # Si es un bloque "bomba", explota y se destruye
            if bloque.tipo == "bomba":
                bloque.explotar()
                bloque.kill()
                continue

            # Si es un bloque "potenciador", se destruye y se activa el potenciador
            if bloque.tipo == "potenciador":
                bloque.activar_potenciador()
                bloque.kill()
                continue

            # Si es un bloque "metal", no hacer nada más
            if bloque.tipo == "metal":
                continue
            
            # Reducir impactos restantes del bloque y eliminar si es necesario
            bloque.impactos -= 1
            if bloque.impactos <= 0:
                bloque.kill()
                multiplicador = {"normal": 10, "duro": 30, "metal": 50, "bomba": 50, "potenciador": 100}
                PUNTUACION += multiplicador[bloque.tipo]

        # Agregar lógica de colisión para bolas adicionales
        for ball in bloques_poder:
            bloques_colisionados_adicionales = pygame.sprite.spritecollide(ball, bloques, False)
            for bloque in bloques_colisionados_adicionales:
                ball.velocidad[1] = -ball.velocidad[1]
                
                # Si es un bloque "bomba", explota y se destruye
                if bloque.tipo == "bomba":
                    bloque.explotar()
                    bloque.kill()
                    continue

                # Si es un bloque "potenciador", se destruye y se activa el potenciador
                if bloque.tipo == "potenciador":
                    bloque.activar_potenciador()
                    bloque.kill()
                    continue

                # Si es un bloque "metal", no hacer nada más
                if bloque.tipo == "metal":
                    continue

                # Reducir los impactos en el bloque y eliminarlo si es necesario
                bloque.impactos -= 1
                if bloque.impactos == 0:
                    bloque.kill()

        if not any([bloque.tipo != "metal" for bloque in bloques]):
            reset()

        PANTALLA.fill(NEGRO)

        # Dibujar y actualizar bloques
        bloques.draw(PANTALLA)
        todos_los_sprites.draw(PANTALLA)

        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(f"Vidas: {VIDAS} Puntuación: {PUNTUACION} Nivel: {NIVEL}", True, BLANCO)
        PANTALLA.blit(texto, [10, 10])

        pygame.display.flip()
        reloj.tick(60)

        if VIDAS == 1 and bola.rect.top >= ALTO:  # Si la vida es 1, termina el juego
            quitar_vida()
        elif VIDAS > 1 and bola.rect.top >= ALTO:  # Verifica si hay más de 1 vida antes de restar
            quitar_vida()

# Bucle principal del juego para solo
def mainAI():
    global PUNTUACION, VIDAS, NIVEL

    reset_bola_paleta()  # Asegurarse de que la bola y la paleta estén en sus posiciones iniciales
    generar_bloques()
    while VIDAS > 0:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()

        # Hacer que la paleta siga la bola
        paleta.sigue_bola(bola)

        todos_los_sprites.update()

        # Lógica de colisión
        # Primero, colisión con la bola principal
        if pygame.sprite.collide_rect(bola, paleta):
            bola.velocidad[1] = -bola.velocidad[1]

        # Luego, colisión con las bolas adicionales
        for ball in bloques_poder:
            if pygame.sprite.collide_rect(ball, paleta):
                ball.velocidad[1] = -ball.velocidad[1]

        bloques_colisionados = pygame.sprite.spritecollide(bola, bloques, False)
        for bloque in bloques_colisionados:
            # Cambiar dirección de la bola al colisionar con un bloque
            bola.velocidad[1] = -bola.velocidad[1]
            
            # Si es un bloque "bomba", explota y se destruye
            if bloque.tipo == "bomba":
                bloque.explotar()
                bloque.kill()
                continue

            # Si es un bloque "potenciador", se destruye y se activa el potenciador
            if bloque.tipo == "potenciador":
                bloque.activar_potenciador()
                bloque.kill()
                continue

            # Si es un bloque "metal", no hacer nada más
            if bloque.tipo == "metal":
                continue
            
            # Reducir impactos restantes del bloque y eliminar si es necesario
            bloque.impactos -= 1
            if bloque.impactos <= 0:
                bloque.kill()
                multiplicador = {"normal": 10, "duro": 30, "metal": 50, "bomba": 50, "potenciador": 100}
                PUNTUACION += multiplicador[bloque.tipo]

        # Agregar lógica de colisión para bolas adicionales
        for ball in bloques_poder:
            bloques_colisionados_adicionales = pygame.sprite.spritecollide(ball, bloques, False)
            for bloque in bloques_colisionados_adicionales:
                ball.velocidad[1] = -ball.velocidad[1]
                
                # Si es un bloque "bomba", explota y se destruye
                if bloque.tipo == "bomba":
                    bloque.explotar()
                    bloque.kill()
                    continue

                # Si es un bloque "potenciador", se destruye y se activa el potenciador
                if bloque.tipo == "potenciador":
                    bloque.activar_potenciador()
                    bloque.kill()
                    continue

                # Si es un bloque "metal", no hacer nada más
                if bloque.tipo == "metal":
                    continue

                # Reducir los impactos en el bloque y eliminarlo si es necesario
                bloque.impactos -= 1
                if bloque.impactos == 0:
                    bloque.kill()

        if not any([bloque.tipo != "metal" for bloque in bloques]):
            reset()

        PANTALLA.fill(NEGRO)

        # Dibujar y actualizar bloques
        bloques.draw(PANTALLA)
        todos_los_sprites.draw(PANTALLA)

        fuente = pygame.font.Font(None, 36)
        texto = fuente.render(f"Vidas: {VIDAS} Puntuación: {PUNTUACION} Nivel: {NIVEL}", True, BLANCO)
        PANTALLA.blit(texto, [10, 10])

        pygame.display.flip()
        reloj.tick(60)

        if VIDAS == 1 and bola.rect.top >= ALTO:  # Si la vida es 1, termina el juego
            quitar_vida()
        elif VIDAS > 1 and bola.rect.top >= ALTO:  # Verifica si hay más de 1 vida antes de restar
            quitar_vida()

    game_over()

# ===================
# Ejecución del Juego
# ===================
if __name__ == "__main__":
    menu()
