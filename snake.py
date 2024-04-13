import turtle
import time
import random

#variables globales
window_width=600#tamaño pantalla x
window_height=600#tamaño pantalla y
delay = 0.15#tiempo espera moverse
segmentos_cuerpo=[]
score=0
high_score=0
color_fondo='#29dc4f'
lista_manzanas=[]

window = turtle.Screen()#ventana
# ajustes ventana
window.title("Juego Snake Python-By Mateo González")#titulo ventana
window.setup(width=window_width, height=window_height)#tamaño ventana
window.bgcolor(color_fondo)#color fondo

# snake objeto
headSnake = turtle.Turtle()#objeto snake
# ajustes iniciales snake
headSnake.speed(0)  # velocidad animacion(movimiento)
headSnake.shape("square")  # forma snake (cubo)
headSnake.color("#118057")  # color snake
headSnake.penup()  # elimina el rastro de la animacion
headSnake.goto(0, 0)  # posicion (centro ventana)
headSnake.direction = "stop"  # direccion (up, down, right, left)

# food configuracion
food = turtle.Turtle()#objeto comida
food.speed(0)#se mueve al instante(sin animacion)
food.shape("circle")
food.color("red")
food.penup()
food.goto(100, 0)

# food2 configuracion
food2 = turtle.Turtle()#objeto comida
food2.speed(0)#se mueve al instante(sin animacion)
food2.shape("circle")
food2.color(color_fondo)
food2.penup()
food2.goto(-100, 0)

#score objeto texto
textScore=turtle.Turtle()
textScore.color(color_fondo)
textScore.penup()
textScore.hideturtle()#sconder raton
textScore.goto(0,255)
textScore.write(f'Score {score} / High Score {high_score}',align='center',font=('Impact',24))#texto mostrar

#start objeto texto
textStart=turtle.Turtle()
textStart.color('white')
textStart.penup()
textStart.hideturtle()
textStart.goto(0,180)
textStart.write(f'Move to start',align='center',font=('Impact',22))

def MostrarHUD():
    #actualizar colores textos
    if textScore.pencolor()==(0.1607843137254902, 0.8627450980392157, 0.30980392156862746):
        textScore.color('white')
            #actualizar pantalla
        textScore.clear()#limpiar texto
        textScore.write(f'Score {score} / High Score {high_score}',align='center',font=('Impact',22))
    else:
        textScore.color(color_fondo)
        textScore.clear()#limpiar texto

def movimientoHeadSnake():
    oY = headSnake.ycor()  # guardar posicion y
    oX = headSnake.xcor()  # guardar posicion x
    if headSnake.direction != "stop":#borrar texto start
        textStart.clear()
    #mover head
    distanciaMover=20#cantidad de distancia a mover
    if headSnake.direction == "up":#direccion
        headSnake.sety(oY + distanciaMover)#actualizar posicion
    elif headSnake.direction == "down":
        headSnake.sety(oY - distanciaMover)
    elif headSnake.direction == "right":
        headSnake.setx(oX + distanciaMover)
    elif headSnake.direction == "left":
        headSnake.setx(oX - distanciaMover)

#cambio direccion snake por teclado
def dirUp():  # que hacer
    if headSnake.direction!='down':#que no se superponga con el cuerpo
        headSnake.direction = "up"#cambio de direccion

def dirDown():
    if headSnake.direction!='up':
        headSnake.direction = "down"

def dirRight():
    if headSnake.direction!='left':
        headSnake.direction = "right"

def dirLeft():
    if headSnake.direction!='right':
        headSnake.direction = "left"

#teclado entradas teclas
window.listen()  # escuchando teclado
window.onkeypress(dirUp, "Up")  # (que hacer,tecla a pulsar)
window.onkeypress(dirDown, "Down")
window.onkeypress(dirRight, "Right")
window.onkeypress(dirLeft, "Left")
window.onkeypress(MostrarHUD,"space")

def ColisionFoodSnake():
    #calcular distancia del headSnake objeto al objeto food 
    if headSnake.distance(food) < 30:#la comio
        ActualizarPuntuacion(10)#sumar 10 puntos
        NuevoSegmentoCuerpo()#añadir un segmento mas al cuerpo
        if score==100:
            ReaparecerFood(2)#añadir otra manzana
        ReaparecerFood(1)#meter otra igual
    if headSnake.distance(food2) < 30:#la comio
        ActualizarPuntuacion(10)
        NuevoSegmentoCuerpo()
        ReaparecerFood(2)#meter otra igual

def ActualizarPuntuacion(sumar=0,reiniciar=False):
    #convertir en global para solucionar problema de acceder al valor 
    global score
    global high_score
    #actualizar puntos y puntuacion maxima
    if not reiniciar:
        score=score+sumar
        if score>high_score:
            high_score=score
    else:#fin programa, reiniciar puntos
        if score>high_score:
            high_score=score
        score=0
    if textScore.pencolor()==(0.1607843137254902, 0.8627450980392157, 0.30980392156862746):
        textScore.color('white')
            #actualizar pantalla
        textScore.clear()#limpiar texto
        textScore.write(f'Score {score} / High Score {high_score}',align='center',font=('Impact',22))

def ColisionVentana():
    tiempoDelay=0.55
    distanciaMover=30
    mitadAnchoPantalla=window_width/2
    mitadAltoPantalla=window_height/2
    ox=0
    oy=0
    #coger posicion ultimo segmento
    if len(segmentos_cuerpo)>0:
        for i in segmentos_cuerpo:
            ox=i.xcor()
            oy=i.ycor()
    else:
        ox=headSnake.xcor()
        oy=headSnake.ycor()
    #cambios de posicion, invertir posicion del eje del que se escape - distanciaMover
    if ox>mitadAnchoPantalla:#se sale de pantalla
        time.sleep(tiempoDelay)#esperar para moverlo a la zona de la pantalla
        headSnake.goto(-(mitadAnchoPantalla-distanciaMover),oy)#moverlo
    elif ox< -mitadAnchoPantalla:
        time.sleep(tiempoDelay)
        headSnake.goto((mitadAnchoPantalla-distanciaMover),oy)
    elif oy>mitadAltoPantalla:
        time.sleep(tiempoDelay)
        headSnake.goto(ox,-(mitadAltoPantalla-distanciaMover))
    elif oy< -mitadAltoPantalla:
        time.sleep(tiempoDelay)
        headSnake.goto(ox,(mitadAltoPantalla-distanciaMover))

def ReaparecerFood(manzana=1):
    minDistance = 30

    if manzana==1:#solo una manzana
        # valor aleatorio dentro de la ventana
        px = random.randint(minDistance, int((window_width / 2) - minDistance))
        py = random.randint(minDistance, int((window_height / 2) - minDistance))
        # signo(cuadrante)
        if random.randint(1, 2) == 1:
            px *= -1
        if random.randint(1, 2) == 1:
            py *= -1
        food.goto(px, py)
    if manzana==2:#la segunda manzana
        # valor aleatorio dentro de la ventana
        px = random.randint(minDistance, int((window_width / 2) - minDistance))
        py = random.randint(minDistance, int((window_height / 2) - minDistance))
        # signo(cuadrante)
        if random.randint(1, 2) == 1:
            px *= -1
        if random.randint(1, 2) == 1:
            py *= -1
        food2.goto(px, py)
        if score==100:#mostrar manzana 2
            food2.color('#802411')


def NuevoSegmentoCuerpo():
    #objeto segmento nuevo
    nuevo_segmento=turtle.Turtle()
    nuevo_segmento.speed(0)
    nuevo_segmento.shape("square")
    nuevo_segmento.color("#138d46")
    nuevo_segmento.penup()
    segmentos_cuerpo.append(nuevo_segmento)#guardar segemento en una lista
    movimientoBody()#actualizar posicion de los segmentos

def movimientoBody():
    total_segmentos=len(segmentos_cuerpo)#cantidad de segmentos del cuerpo
    #actualizar el primer segmento a parte
    if total_segmentos>0:
        ox=headSnake.xcor()
        oy=headSnake.ycor()
        segmentos_cuerpo[0].goto(ox,oy)
    #actualizar posicion de los segmentos menos el primero
    for i in range(total_segmentos-1,0,-1):
        #coger posicion x,y del segmento anterior(ya actualizado)
        ox=segmentos_cuerpo[i-1].xcor()
        oy=segmentos_cuerpo[i-1].ycor()
        segmentos_cuerpo[i].goto(ox,oy)#actualizar posicion del segmento actual
    movimientoHeadSnake()#mover cabeza

def colisionSnakeBody():
    if len(segmentos_cuerpo)>0:
        for segmento in segmentos_cuerpo:#mirar todos los segementos
            if segmento.distance(headSnake)<10:#fin partida
                time.sleep(1)#esperar 1s
                headSnake.goto(0,0)
                headSnake.direction="stop"
                #sacar segementos de la zona de la pantalla
                for segmento1 in segmentos_cuerpo:
                    segmento1.goto(window_width+30,window_height+30)
                segmentos_cuerpo.clear()#limpiar lista
                ActualizarPuntuacion(0,True)#reiniciar puntuacion
                #mostrar texto start
                textStart.clear()
                textStart.write(f'Move to start',align='center',font=('Impact',22))

#controlador/ejecutador programa
while True:#bucle infinito
    window.update()#actualizar canvas pantalla 
    if headSnake.direction!="stop":
        ColisionVentana()
        ColisionFoodSnake()
        colisionSnakeBody()
        movimientoBody()#moviemeinto del snake
        time.sleep(delay)#esperar en segundos y repetir bucle 