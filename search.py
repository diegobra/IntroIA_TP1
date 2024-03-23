from collections import deque
import tree_hanoi
import hanoi_states
import tracemalloc

def breadth_first_tree_search(problem: hanoi_states.ProblemHanoi):
    """
    Realiza una búsqueda en anchura para encontrar una solución a un problema de Hanoi.
    Esta función no chequea si un estado se visito, por lo que puede entrar en Loop infinitos muy fácilmente. No
    usarla con más de 3 discos.

    Parameters:
        problem (hanoi_states.ProblemHanoi): El problema de la Torre de Hanoi a resolver.

    Returns:
        tree_hanoi.NodeHanoi: El nodo que contiene la solución encontrada.
    """
    frontier = deque([tree_hanoi.NodeHanoi(problem.initial)])  # Creamos una cola FIFO con el nodo inicial
    while frontier:
        node = frontier.popleft()  # Extraemos el primer nodo de la cola
        if problem.goal_test(node.state):  # Comprobamos si hemos alcanzado el estado objetivo
            return node
        frontier.extend(node.expand(problem))  # Agregamos a la cola todos los nodos sucesores del nodo actual

    return None


def breadth_first_graph_search(problem: hanoi_states.ProblemHanoi, display: bool = False):
    """
    Realiza una búsqueda en anchura para encontrar una solución a un problema de Hanoi. Pero ahora si recuerda si ya
    paso por un estado e ignora seguir buscando en ese nodo para evitar recursividad.

    Parameters:
        problem (hanoi_states.ProblemHanoi): El problema de la Torre de Hanoi a resolver.
        display (bool, optional): Muestra un mensaje de cuantos caminos se expandieron y cuantos quedaron sin expandir.
                                  Por defecto es False.

    Returns:
        tree_hanoi.NodeHanoi: El nodo que contiene la solución encontrada.
    """

    frontier = deque([tree_hanoi.NodeHanoi(problem.initial)])  # Creamos una cola FIFO con el nodo inicial

    explored = set()  # Este set nos permite ver si ya exploramos un estado para evitar repetir indefinidamente
    while frontier:
        node = frontier.popleft()  # Extraemos el primer nodo de la cola

        # Agregamos nodo al set. Esto evita guardar duplicados, porque set nunca tiene elementos repetidos, esto sirve
        # porque heredamos el método __eq__ en tree_hanoi.NodeHanoi de aima.Node
        explored.add(node.state)

        if problem.goal_test(node.state):  # Comprobamos si hemos alcanzado el estado objetivo
            if display:
                print(len(explored), "caminos se expandieron y", len(frontier), "caminos quedaron en la frontera")
            return node
        # Agregamos a la cola todos los nodos sucesores del nodo actual que no haya visitados
        frontier.extend(child for child in node.expand(problem)
                        if child.state not in explored and child not in frontier)

    return None

def depth_first_graph_search(problem: hanoi_states.ProblemHanoi, display: bool = False):
    """
    Diego Braga: Resolución a la pregunta 4 del TP1.
    Se implemente una búsqueda en profundidad tomando como base el algoritmo ya implementado
    en la función breadth_first_graph_search.

    En este caso se utiliza una cola LIFO para almacenar los nodos en la frontera, lo que hace que siempre
    se recorran primero los hijos en lugar de dejarlos para el final.

    Parameters:
        problem (hanoi_states.ProblemHanoi): El problema de la Torre de Hanoi a resolver.
        display (bool, optional): Muestra un mensaje de cuantos caminos se expandieron y cuantos quedaron sin expandir.
                                  Por defecto es False.

    Returns:
        tree_hanoi.NodeHanoi: El nodo que contiene la solución encontrada.
    """

    frontier = deque([tree_hanoi.NodeHanoi(problem.initial)])  # Se crea cola LIFO con el estado inciial

    explored = set()  # Este set nos permite ver si ya exploramos un estado para evitar repetir indefinidamente
    while frontier:
        node = frontier.popleft()  # Extraemos el primer nodo de la cola

        # Agregamos nodo al set. Esto evita guardar duplicados, porque set nunca tiene elementos repetidos, esto sirve
        # porque heredamos el método __eq__ en tree_hanoi.NodeHanoi de aima.Node
        explored.add(node.state)

        if problem.goal_test(node.state):  # Comprobamos si hemos alcanzado el estado objetivo
            if display:
                print(len(explored), "caminos se expandieron y", len(frontier), "caminos quedaron en la frontera")
            return node
        # Agregamos a la cola todos los nodos sucesores del nodo actual que no haya visitados
        # A diferencia de la búsqueda en anchura, en este caso los hijos se almacenan a la izquierda
        # para que en la próxima iteración sean los primeros en ser obtenidos de la cola.
        frontier.extendleft(child for child in node.expand(problem)
                            if child.state not in explored and child not in frontier)

    return None


def depth_limited_search(problem: hanoi_states.ProblemHanoi, depth: int):

    reached = deque([])

    def recursive_dls(node: tree_hanoi.NodeHanoi, problem2, depth2):

        _, memory_peak = tracemalloc.get_traced_memory()
        memory_peak /= 1024 * 1024
        print(f"Maxima memoria ocupada: {round(memory_peak, 2)} [MB]", )

        nonlocal reached

        if depth2 == 0:
            # Se chequea si en el final de esta rama alcanzó el objetivo
            if problem.goal_test(node.state):
                return node
            else:
                return 'cutoff'
        else:
            cutoff_occurred = False

            for child in node.expand(problem2):
                if child.state not in reached:

                    # Se agrega el hijo actual al stack y se analiza recursivamente
                    reached.append(child.state)
                    result = recursive_dls(child, problem, depth2 - 1)

                    # Se quita el hijo actual del stack para que pueda ser evaluado en otras ramas
                    # y así buscar la solución óptima
                    reached.pop()

                    if result == 'cutoff':
                        cutoff_occurred = True
                    elif result is not None:
                        return result

            if cutoff_occurred:
                return 'cutoff'

        return None

    # Se agrega el nodo principal porque es parte del camino hacia el final de la rama
    reached.append(tree_hanoi.NodeHanoi(problem.initial))
    return recursive_dls(tree_hanoi.NodeHanoi(problem.initial), problem, depth)


def iterative_deepening_search(problem: hanoi_states.ProblemHanoi, display: bool = False, max_depth: int = 99999):

    for depth in range(max_depth):
        result = depth_limited_search(problem, depth)
        if result != 'cutoff':
            return result
