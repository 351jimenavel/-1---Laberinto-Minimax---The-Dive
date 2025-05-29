# -1---Laberinto-Minimax---The-Dive
# Juego de Persecución Inteligente  
## Laberinto Ratón vs Gato

### ¿Qué creé?
Este proyecto es un juego de persecución inteligente en un laberinto, donde hay dos protagonistas: el **gato** y el **ratón**.  
En un tablero bidimensional, juegan una partida de 10 turnos (5 cada uno).  

- El **gato** (controlado por el algoritmo Minimax) busca moverse de forma óptima para atrapar al ratón.  
- El **ratón** (manejado por el usuario con las teclas W/A/S/D) tiene que agarrar el queso antes de que se acaben los turnos, porque si no, ¡pierde igual aunque escape del gato!

### ¿Qué funcionó?
La forma metódica en que encaré el desarrollo fue clave.  
Primero construí el tablero, luego posicioné a los personajes, moví uno con input, luego el otro, agregué condiciones de victoria y derrota… y finalmente incorporé el algoritmo Minimax para el gato.  
Ir paso a paso me ayudó a entender no solo el propósito del juego, sino también cómo conectar cada parte del código.  

### ¿Qué fue un desastre?
Agregar el queso al inicio fue una mezcla de acierto y problema.  
Como lo posicioné aleatoriamente (al igual que los primeros movimientos del ratón), a veces pasaba que el ratón caía encima del queso en los primeros turnos y el juego terminaba demasiado rápido, algo que no quería.  
Además, evitar que los personajes repitan casillas o hagan movimientos tontos aún es un desafío. El manejo de la aleatoriedad en los recorridos es un punto que definitivamente quiero mejorar.  

### Mi mejor ¡ajá!
Descubrir cómo estructurar el juego fue un momento clave.
Empecé escribiendo funciones sueltas para ir entendiendo las partes importantes del juego. Luego probé con clases, pero finalmente opté por volver al enfoque con funciones. Eso no solo me ayudó a entender mejor la lógica, sino que también optimizó cómo organizaba y llamaba cada parte del código, haciéndolo más limpio y menos repetitivo.
