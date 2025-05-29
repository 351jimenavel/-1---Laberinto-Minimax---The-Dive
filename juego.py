# Laberinto Gato vs Ratón

import os
import time
import random

###### Inicio del Juego
# Estado inicial del juego 
jugador_posicion = [0, 0]   ## Posicion inicial RATÓN
gato_posicion = [4, 4]  ## Posicion inicial GATO
queso_posicion = [3,3]
tablero = None
tamaño = 5
controles_raton = {'w':'arriba', 's':'abajo', 'a':'izquierda', 'd':'derecha'}

def inicializar_juego():
    '''Inicializa el estado del juego'''
    global tablero, jugador_posicion, gato_posicion, queso_posicion

    tablero = crear_tablero(tamaño)
    jugador_posicion = [0, 0]
    gato_posicion = [4, 4]
    queso_posicion = [3,3]

###### Funciones para mostrar y mover
# Crear la grilla (tamaño x tamaño)
def crear_tablero(tamaño):
    '''Se crea las dimensiones del tablero'''
    tablero = []
    for _ in range(tamaño):
        fila = []
        for _ in range(tamaño):
            fila.append(".")
        tablero.append(fila)
    return tablero
        
def recorrido_de_personajes():
    '''Dibujo de grilla/punto y los personajes según correspondan las posiciones'''
    
    global tablero, jugador_posicion, gato_posicion, queso_posicion

    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n Estado actual del tablero:")

    # Se recorre cada fila del tablero
    for x in range(len(tablero)):
        # Dentro de cada fila se recorre cada columna
        for y in range(len(tablero[x])):
            posicion = [x,y]
            if posicion == jugador_posicion and posicion == gato_posicion:
                print('💥', end=' ')
            elif posicion == jugador_posicion:
                print('🐭', end=' ')
            elif posicion == gato_posicion:
                print('🐱', end=' ')
            elif posicion == queso_posicion:
                print("🧀", end=' ')
            else:
                print("🔳", end=' ')
        print()

def mover_personaje(tecla, posicion, controles):
    '''Se establecen los valores de los controles (como se moverán los personajes)'''
    global tamaño
    
    direccion = controles.get(tecla)    #.get es un metodo de diccionarios que busca una clave. Si la clave existe te devuelve el valor, si no existe, te devuelve none
    if not direccion:
        print("Tecla invalida")
        time.sleep(1)
        return False

    #Creamos una copia para no modificar la original sin antes validar el movimiento
    nuevo_x = posicion[0]
    nuevo_y = posicion[1]

    #Se utilizan las claves del diccionario controles para asignar cuales serán sus movimientos.
    if direccion == 'arriba' and nuevo_x > 0:   # arriba
        nuevo_x -= 1
    elif direccion == 'abajo' and nuevo_x < tamaño - 1:     # abajo
        nuevo_x += 1
    elif direccion == 'izquierda' and nuevo_y > 0:   # izquierda
        nuevo_y -= 1
    elif direccion == 'derecha' and nuevo_y < tamaño - 1:     # derecha
        nuevo_y += 1
    else:
        print("Movimiento inválido.")
        time.sleep(1) # Hace que el mensaje aparezca por un tiempo definido. Delay entre acciones.
        return False 
    
    # Actualizamos la posicion solo si el movimiento es válido
    posicion[0] = nuevo_x
    posicion[1] = nuevo_y
    return True

###### Funciones de turno
def turno_raton():
    '''Maneja el turno del raton'''
    movimiento = input(f"\nMover ratón w/a/s/d, q para salir): ").lower()
    
    if verificar_salir(movimiento):
        return False
    
    # Validar entrada
    if movimiento not in ['w', 'a', 's', 'd']:
        print("Entrada inválida. Usa w/a/s/d")
        return True     # Se devuelve True para que se pueda ingresar nuevamente
        
    if mover_personaje(movimiento, jugador_posicion, controles_raton):
        recorrido_de_personajes()   # Mostrar nuevo estaod
    
    if agarrar_queso(jugador_posicion, queso_posicion):
        print("\nEl ratón atrapó el queso! Ganó la partida")
        return False
    
    return True

def movimientos_validos_para_turnos(posicion):
    '''Devuelve todas las posciiones a las que el gato puede moverse desde su posicion actual, sin salir del tablero'''
    movimientos = []
    direcciones = [(-1,0), (1,0), (0,-1), (0,1)]        # movimientoss válidos (Arriba, abajo, izquierda, derecha)
    # Por cada direccion
    for eje_x, eje_y in direcciones:
        # Calcula el nuevo x e y sumando la direccion a la posicoon actual
        nuevo_x = posicion[0] + eje_x
        nuevo_y = posicion[1] + eje_y

        # Validar que este dentro del tablero
        if 0 <= nuevo_x < tamaño and 0 <= nuevo_y < tamaño:
            movimientos.append((nuevo_x,nuevo_y))    #Si es valido, se guarda en la lista
    return movimientos

def evaluar_puntaje(gato_posicion, jugador_posicion):
    '''Asigna un puntaje al estado del juego. Más alto si el gato atrapa al ratón, más bajo si está lejos.'''
    # Si el gato está en la misma psocion que el ratón, son 100 puntos
    if gato_posicion == jugador_posicion:
        return 100
    # Si el ratón llegó al queso son -100 puntos (malo para el raton)
    if jugador_posicion == queso_posicion:
        return -100

    ## Se calcula la distancia entre el gato y el rató  usando la DISTANCIA MANHATTAN
    posicion_en_el_ejex = abs(gato_posicion[0] - jugador_posicion[0])
    posicion_en_el_ejey = abs(gato_posicion[1] - jugador_posicion[1])
    distancia = posicion_en_el_ejex + posicion_en_el_ejey
    return -distancia   # Se devuelve como negativo ya que cuanto más cerca esté el gato, mejor. Penaliza que el gato esté lejos

def minimax(profundidad, es_maximizador, gato_posicion, jugador_posicion):
    '''Se usa el algortimo Minimax para calcular el mejor movimeinto pensnado a varios turnos adelante.
    - Maximiza las opciones del gato (busca atraparte)
    - Minimiza las opciones del ratón (intenta huir)'''
    # Si ya llegó al límite de profundidad (turnos que mira adelante) o alguien ganó (gato o ratón), evalua el puntaje actual
    if profundidad == 0 or gato_posicion == jugador_posicion or jugador_posicion == queso_posicion:
        return evaluar_puntaje(gato_posicion, jugador_posicion)
    
    # Si es el turno del gato (Maximizador), entonces busca el movimiento que de el mejor puntaje
    if es_maximizador:
        mayor_puntaje = float('-inf')
        for movimiento in movimientos_validos_para_turnos(gato_posicion):
            puntaje = minimax(profundidad - 1, False,movimiento,jugador_posicion)
            mayor_puntaje = max(mayor_puntaje, puntaje)
        return mayor_puntaje
    # Si no es el turno del ratón (minimizador), entonces busca el movimiento que de el menor puntaje
    else:
        menor_puntaje = float('inf')
        for movimiento in movimientos_validos_para_turnos(jugador_posicion):
            puntaje = minimax(profundidad - 1, True,gato_posicion,movimiento)
            menor_puntaje = min(menor_puntaje, puntaje)
        return menor_puntaje
    
def obtener_mejor_movimiento_gato(gato_posicion, jugador_posicion):
    '''Se recorre todos los movimientos posibles del gato y elige el que tenga el mejor resultado usando Minimax'''
    # Revisar si en los movimientos posibles alguno ya agarró al ratón
    for movimiento in movimientos_validos_para_turnos(gato_posicion):
        if list(movimiento) == jugador_posicion:
            return movimiento

    mejor_puntaje = float('-inf')
    mejor_movimiento = gato_posicion
    # Por cada movimiento posible...
    for movimiento in movimientos_validos_para_turnos(gato_posicion):
        # Se llama al minimax recursivamente
        puntaje = minimax(3,True,movimiento, jugador_posicion)
        # Se compara el puntaje recibido
        if puntaje > mejor_puntaje:
            # Se guarda el movimiento con puntaje más alto
            mejor_puntaje = puntaje
            mejor_movimiento = movimiento

    return mejor_movimiento     # Retorna dicho movimiento

# Verificar choque de personajes
def verificar_choque_gato_y_raton(jugador_posicion, gato_posicion):
    '''Se establece que se debe cumplir para que los personajes estén en estado de "choque" (que sus posiciones sean las mismas)'''
    return jugador_posicion == gato_posicion

def agarrar_queso(jugador_posicion, queso_posicion):
    '''Se establece que se debe cumplir para considerar que el ratón agarró el queso (que sus posiciones sean las mismas)'''
    return jugador_posicion == queso_posicion

# Funcion que verifica si el usuario quiere volver a iniciar el juego
def verificar_salir(movimiento):
    '''Funcion que facilita al usuario terminar el juego'''
    if movimiento == "q":
        print("Juego terminado.")
        return True

def primeros_turnos_raton(turnos):
    #Se establece el recorrido del ratón en ese tiempo donde el "No es inteligente" - 
    global jugador_posicion
    direcciones = [(-1,0), (1,0), (0,-1), (0,1)]        # Arriba, Abajo, izquierda, Derecha (2 espacios)
    # Bucle para mover al ratón
    for _ in range(turnos):
        movimientos_validos = []
        ## Movimiento aleatorio RATÓN
        # Actualizar posiciones
        for eje_x in direcciones:
            nuevo_x = jugador_posicion[0] + eje_x[0]
            for eje_y in direcciones:
                nuevo_y = jugador_posicion[1] + eje_y[1]

                if 0 <= nuevo_x < tamaño and 0 <= nuevo_y < tamaño:
                    movimientos_validos.append([nuevo_x, nuevo_y])
            
        if movimientos_validos:
            jugador_posicion = random.choice(movimientos_validos)
        
        recorrido_de_personajes()
        time.sleep(0.5)

def jugar():
    '''Funcion que maneja el flujo del juego'''
    inicializar_juego()
    primeros_turnos_raton(4)   
    turnos = 0
    cantidad_de_turnos_maximo = 10

    while (
        jugador_posicion != gato_posicion and
        jugador_posicion != queso_posicion and
        turnos < cantidad_de_turnos_maximo
    ):
        
        turnos += 1
        if turnos >= cantidad_de_turnos_maximo and jugador_posicion != queso_posicion:
            print("Se llegó al límite de turnos y el ratón no agarró el queso! Perdiste")
            break 

        recorrido_de_personajes()
        for turno in range(1, turnos+1):
            print(f"\rTienes {turno}/{cantidad_de_turnos_maximo} turnos", end=' ')

        if not turno_raton():
            break

        if verificar_choque_gato_y_raton(jugador_posicion,gato_posicion):
            print("\nAtrapado! El juego se acabó")
            recorrido_de_personajes()
            break

        # Turno del gato (controlado por minimax)
        nueva_posicion_gato = obtener_mejor_movimiento_gato(gato_posicion, jugador_posicion)
        gato_posicion[0] = nueva_posicion_gato[0]
        gato_posicion[1] = nueva_posicion_gato[1]
        if verificar_choque_gato_y_raton(jugador_posicion,gato_posicion):
            print("\nAtrapado! El juego se acabó")
            recorrido_de_personajes()
            break
    
jugar()