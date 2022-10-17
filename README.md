# IA TP 2 - FPUNA 2022
## Tema
- ### Damas
## Integrantes
- ### Camila Alderete
- ### Luis Canhete
- ### Oscar Pedrozo
## Enunciado
En todos los casos implementar 3 algoritmos: Minimax, Minimax con Poda Alfa Beta, y un agente basado en Reinforcement Learning (que pueda aprender de un jugador aleatorio o los jugadores minimax). Deberá ser posible parametrizar el Límite de Nivel para la búsqueda al algoritmo de Minimax con y sin poda. Al comparar los resultados deberán comparar por ejemplo: Minimax(3) vs AlfaBeta(3), Minimax(4) vs AlfaBeta(2), Minimax(2) vs AlfaBeta(4), Minimax(2) vs RL, AlfaBeta(2) vs RL, etc., donde entre paréntesis colocamos el nivel límite del algoritmo. Uds. deberán sugerir comparaciones interesantes y especificar niveles realistas atendiendo el juego en particular a ser resuelto. Para la demostración se
debe permitir además jugar a un Humano contra alguna Estrategia que se reciba como parámetro.

## Problema
Escoger el juego de Damas cuyas reglas de juego sean lo más parecido posible al juego de
Damas clásico que se juega en nuestro país (con fichas normales y fichas coronadas como damas por
ejemplo). Función de evaluación posible: Suma ponderada de fichas propias – suma ponderada de fichas
del oponente.

## Jugar
    python iniciar_juego.py 

## Ver tabla de aprendizaje
    python training_results.py 

## Dependencias
    pip install pygame
    pip install pyautogui

## Referencias
[Introduction to Machine Learning and Design of a Learning System](https://medium.datadriveninvestor.com/3-steps-introduction-to-machine-learning-and-design-of-a-learning-system-bd12b65aa50c)

[Reinforcement Learning aplicado al Tic Tac Toe](https://github.com/jpaciello/ia)
