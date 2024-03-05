import turtle
import time
import random
# minute video 40min; enalce:https://youtu.be/lKzEvbGbbPo
#variables globales
window_width=600
window_height=600
delay = 0.1
segmentos_cuerpo=[]
score=0
high_score=0
color_fondo='light green'

window = turtle.Screen()#ventana
# ajustes ventana
window.title("Juego Snake Python-By Mateo González")#titulo ventana
window.setup(width=window_width, height=window_height)#tamaño ventana
window.bgcolor(color_fondo)#color fondo


# snake objeto
head = turtle.Turtle()#objeto snake
# ajustes iniciales snake
head.speed(0)  # velocidad animacion(movimiento)
head.shape("square")  # forma snake (cubo)
head.color("dark green")  # color snake
head.penup()  # elimina el rastro de la animacion
head.goto(0, 0)  # posicion (centro ventana)
head.direction = "stop"  # direccion (up, down, right, left)

# food configuracion
food = turtle.Turtle()#objeto comida
food.speed(0)#se mueve al instante(sin animacion)
food.shape("circle")
food.color("red")
food.penup()
food.goto(100, 0)

#score objeto
textScore=turtle.Turtle()
textScore.speed(0)
textScore.color(color_fondo)
textScore.penup()
textScore.hideturtle()
textScore.goto(0,255)
textScore.write(f'Score {score} / High Score {high_score}',align='center',font=('Impact',24))

#mostrar HUD
def MostrarHUD():
    #actualizar colores textos
    if textScore.pencolor()==color_fondo:
        textScore.color('white')
    else:
        textScore.color(color_fondo)
    #actualizar pantalla
    textScore.clear()
    textScore.write(f'Score {score} / High Score {high_score}',align='center',font=('Impact',22))
    
# movimientos del snake
def mov():
    oY = head.ycor()  # guardar posicion y
    oX = head.xcor()  # guardar posicion x
    if head.direction == "up":
        head.sety(oY + 10)
    elif head.direction == "down":
        head.sety(oY - 10)
    elif head.direction == "right":
        head.setx(oX + 10)
    elif head.direction == "left":
        head.setx(oX - 10)


# teclado movimiento snake
def dirUp():  # que hacer
    if head.direction!='down':#que no se superponga con el cuerpo
        head.direction = "up"#cambio de direccion


def dirDown():
    if head.direction!='up':
        head.direction = "down"


def dirRight():
    if head.direction!='left':
        head.direction = "right"


def dirLeft():
    if head.direction!='right':
        head.direction = "left"

def dirSpace():  # que hacer
    MostrarHUD()
    
window.listen()  # escuchando teclado
window.onkeypress(dirUp, "Up")  # (que hacer,tecla)
window.onkeypress(dirDown, "Down")
window.onkeypress(dirRight, "Right")
window.onkeypress(dirLeft, "Left")
window.onkeypress(MostrarHUD,"space")

# funciones food
def ColisionFoodSnake():
    if head.distance(food) < 30:
        Reaparecer()
        SegmentosCuerpo()
        ActualizarPuntuacion(10)

def ActualizarPuntuacion(sumar=0,reiniciar=False):
    global score
    global high_score
    
    if not reiniciar:
        score=score+sumar
        if score>high_score:
            high_score=score
    else:
        score=0
        
    textScore.clear()
    textScore.write(f'Score {score} / High Score {high_score}',align='center',font=('Impact',22))
    
def ColisionVentana():
    mitadAnchoPantalla=window_width/2
    mitadAltoPantalla=window_height/2
    ox=head.xcor()
    oy=head.ycor()
    for i in segmentos_cuerpo:
        ox=i.xcor()
        oy=i.ycor()
    tiempoDelay=0.5
    #cambios de posicion, segun el eje en el que salga moverlo para el borde contrario -20
    if ox>mitadAnchoPantalla:
        time.sleep(tiempoDelay)
        head.goto(-(mitadAnchoPantalla-20),oy)
        movBody()
    elif ox< -mitadAnchoPantalla:
        time.sleep(tiempoDelay)
        head.goto((mitadAnchoPantalla-20),oy)
        movBody()
    elif oy>mitadAltoPantalla:
        time.sleep(tiempoDelay)
        head.goto(ox,-(mitadAltoPantalla-20))
        movBody()
    elif oy< -mitadAltoPantalla:
        time.sleep(tiempoDelay)
        head.goto(ox,(mitadAltoPantalla-20))
        movBody()
        
def Reaparecer():
    minDistance = 30
    # valor
    px = random.randint(minDistance, int((window_width / 2) - minDistance))
    py = random.randint(minDistance, int((window_height / 2) - minDistance))
    # signo
    if random.randint(1, 2) == 1:
        px = -(px)
    if random.randint(1, 2) == 1:
        py = -(py)
    food.goto(px, py)

def SegmentosCuerpo():
    nuevo_segmento=turtle.Turtle()
    nuevo_segmento.speed(0)
    nuevo_segmento.shape("square")
    nuevo_segmento.color("green")
    nuevo_segmento.penup()
    segmentos_cuerpo.append(nuevo_segmento)
    
    movBody()

def movBody():
    total_segmentos=len(segmentos_cuerpo)
    for i in range(total_segmentos-1,0,-1):
        ox=segmentos_cuerpo[i-1].xcor()
        oy=segmentos_cuerpo[i-1].ycor()
        segmentos_cuerpo[i].goto(ox,oy)
    if total_segmentos>0:
        ox=head.xcor()
        oy=head.ycor()
        segmentos_cuerpo[0].goto(ox,oy)
        mov()
      
def colisionSnakeBody():
    for segmento in segmentos_cuerpo:
        if segmento.distance(head)<10:#fin partida
            time.sleep(1)
            head.goto(0,0)
            head.direction="stop"
            for segmento1 in segmentos_cuerpo:
                segmento1.goto(window_width+60,window_height+60)
            segmentos_cuerpo.clear()
            ActualizarPuntuacion(0,True)
            
#controlador/ejecutador
while True:
    window.update()
    ColisionVentana()
    ColisionFoodSnake()
    colisionSnakeBody()
    mov()
    movBody()
    time.sleep(delay)