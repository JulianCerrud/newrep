import pygame 
import random
import math
from pygame import mixer

#iniciar Pygame --
pygame.init()

#para crear pantalla --
pantalla = pygame.display.set_mode((800,600))

#titulo de icono --
pygame.display.set_caption("-->> BATALLA ESPACIAL <<-- made By Julian2891")
icono = pygame.image.load("E:class 10/icono.png") #cargar imagen del logo --
pygame.display.set_icon(icono)
fondo = pygame.image.load("E:class 10/fondo.jpg") #imagen de fondo

#Agregar musica
mixer.music.load('E:class 10/fondosond1.wav') #cargas la musica de fondo
mixer.music.set_volume(1)#ajustas el volumen
mixer.music.play(-1)#-1 para que se repita infinitamente

#Variables de jugador -- 
img_jugador = pygame.image.load("E:class 10/img_jugador.png") #imagen jugador
jugador_x = 368 # la mitad mas la division del tamaño de la nave--
jugador_y = 500
jugador_x_cambio = 0 #almacena el movimiento en el eje de la X

#Variables de enemigo -- 
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos): #funcion cantidad de enemigos
    img_enemigo.append(pygame.image.load("E:class 10/enemigo.png")) #imagen de enemigo
    enemigo_x.append(random.randint(0, 763)) #se puede modificar de izquierda a derecha
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(1) #velocidad de el enemigo
    enemigo_y_cambio.append(40) #queremos que baje 60 pixclearel

#Variables de la Bala -- 
img_bala = pygame.image.load("E:class 10/bala.png")
bala_x = 0 #donde sale la bala --
bala_y = 500 #pixel que tiene la nave --
bala_x_cambio = 0 #no se utiliza esta variable --
bala_y_cambio = 2 #velocidad de la bala --
bala_visible = False

#puntaje --
puntaje = 0 
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

#texto final de juego --
fuente_final = pygame.font.SysFont('Pixelmania', 40) #GAME OVER
def texto_final():
    mi_fuente_final = fuente_final.render("GAME OVER", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (150, 230)) #arroja el Game over en pantalla

#funcion mostrar puntaje --
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True,(255, 255, 255))
    pantalla.blit(texto,(x, y))
 
#funcion de jugador --
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y)) #arroja jugador--

#funcion de enemigo --
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y)) #arroja enemigo--

#funcion disparar bala y que aparesca --
def disparar_bala(x, y): #coordenadas x, y --
    global bala_visible #variable global --
    bala_visible = True #la bala se puede ver --
    pantalla.blit(img_bala, (x + 16, y + 10)) #coloca bala en pantalla en la nave  y se colocan tuplas x, y -- 
    
#Funcion Colicion 
def hay_colicion(x_1, y_1, x_2, y_2): #se saca la raiz para poder que realice colicion
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2)) #calculo matematico
    if distancia < 27: #se coloca una distancia
        return True #hay colicion
    else:
        return False #no hay colicion


se_ejecuta = True #loop del juego --
while se_ejecuta:
    #si quieres utilizar fondo-> pantalla.fill((46, 109, 114))#relleno color RGB --

    #imagen de fondo
    pantalla.blit(fondo, (0,0))#coloca la imagen en la cordenada
    
    #iterar eventos
    for evento in pygame.event.get():
        
        if evento.type == pygame.QUIT: #evento QUIT para poder cerrar la ventana --
            se_ejecuta = False

        if evento.type == pygame.KEYDOWN:# tecla presionada se fija en eso --
            if evento.key == pygame.K_LEFT: #Se fija si la presionada es la tecla izquierda --
                jugador_x_cambio = -0.5 #velocidad de la derecha --
            if evento.key == pygame.K_RIGHT:#Se fija si la presionada es la tecla derecha --
                jugador_x_cambio = 0.5 #velocidad de la izquierda --
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound("E:class 10/disparo2.wav") #sonido de la bala
                sonido_bala.play()#para poder ejecurar el sonido
                if not bala_visible: #se coloca por que si precionas space se mueve la bala --
                    bala_x = jugador_x #tranforma jugador x a bala x
                    disparar_bala(bala_x, bala_y)  
                



        if evento.type == pygame.KEYUP: #usuario suelta la tecla --
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT: #se fija que tecla fue <-->
                jugador_x_cambio = 0 #Establece el cambio a cero --


    #modificar ubicacion del jugador
    jugador_x += jugador_x_cambio #modifique --

    #mantener entre los bordes la nave del jugador
    if jugador_x <= 0: #verificamos si es < = 0 por que el limite izquierdo
        jugador_x = 0 
    elif jugador_x >= 736: #no pase del borde derecho (eje 800 -64 por la nave = 736) limite
        jugador_x = 736

    #modificar ubicacion del enemigo
    for e in range(cantidad_enemigos):

        #FIN DEL JUEGO
        if enemigo_y[e] > 400:# si llega a la altura ya pierdes el juego
            for K in range(cantidad_enemigos):
                enemigo_y[K] = 1000
            texto_final() 
            break

        enemigo_x[e] += enemigo_x_cambio[e] #modifique pocison --

        #mantener entre los bordes la nave del enemigo
        if enemigo_x[e] <= 0: #verificamos si es < = 0 por que el limite izquierdo
            enemigo_x_cambio[e] = 0.3 #enemigo toca borde retorna al medio
            enemigo_y[e] += enemigo_y_cambio[e] #baja 50 pixeles por la x      
        elif enemigo_x[e] >= 736: #no pase del borde derecho (eje 800 -64 por la nave = 736) limite
            enemigo_x_cambio[e] = -0.3 #enemigo retorna al medio
            enemigo_y[e] += enemigo_y_cambio[e] #baja 50 pixeles por la y
        #colision
        colision = hay_colicion(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision: #verificacion de la colision
            sonido_colision = mixer.Sound("E:class 10/muerteenemigo1.wav") #sonido cuando matas una nave
            sonido_colision.play()#accionas el sonido
            bala_y = 500 #restablece bala a la altura de la nave
            bala_visible = False #deja de ser visible, para disparar bala nueva
            puntaje += 1 #suma el puntaje
            print(puntaje)
            enemigo_x[e] = random.randint(0, 736) #Reaparece el anemigo despues de matarlo
            enemigo_y[e] = random.randint(50, 200)
        
        enemigo(enemigo_x[e], enemigo_y[e], e) #se llama enemigo en pantalla

    #movimiento Bala
    if bala_y <= -24: #24 pixels
        bala_y = 500 #la altura de la nave
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio #balacambio vale 1 y se resta



    jugador(jugador_x, jugador_y) #se llama al jugador

    mostrar_puntaje(texto_x, texto_y)
    
    #actualizar
    pygame.display.update()



