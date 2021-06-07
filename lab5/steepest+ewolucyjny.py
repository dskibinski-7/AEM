import tsplib95
import networkx as nx
import random
import matplotlib.pyplot as plt
import time


def best_solution_inside(solution, f_delta, distance_matrix):

    #better_solution = solution.copy()
    for i in range(len(solution)):
        edge1_node1 = solution[i]
        try:
            edge1_node2 = solution[i+1]
        except IndexError:
            break


        #bierzemy pod uwage tylko te krawedzie ktora sa za obecnie przerabiana oraz przed
        avalaible_edges = solution[i+1:-1] + solution[:i]

        #zapewnienie usuniecia duplikatow
        try:
            avalaible_edges.remove(edge1_node1)
        except: pass
        try:
            avalaible_edges.remove(edge1_node2)
        except: pass


        #iterowanie po poozostalych krawedziach
        for j in range(len(avalaible_edges)):
            edge2_node1 = avalaible_edges[j]
            try:
                edge2_node2 = avalaible_edges[j+1]
            except IndexError:
                break

            cost_edges_to_delete = distance_matrix[edge1_node1,edge1_node2] + distance_matrix[edge2_node1,edge2_node2]
            cost_edges_to_add = distance_matrix[edge1_node1, edge2_node1] + distance_matrix[edge1_node2,edge2_node2]

            #ocena ruchu
            current_delta = cost_edges_to_add - cost_edges_to_delete

            if current_delta < f_delta:
                buffer = solution.copy()

                better_solution = solution.copy()
                ix_to_swap = [better_solution.index(edge1_node2), better_solution.index(edge2_node1)]
                better_solution[ix_to_swap[0]] = edge2_node1
                better_solution[ix_to_swap[1]] = edge1_node2

                #jezeli poczatek i koniec ten sam (start point) to spoko, jak nie to wroc do poprzedniego rozwiazania
                if better_solution[0] == better_solution[-1]:
                    f_delta = current_delta
                else:
                    better_solution = buffer

    return better_solution, f_delta



def best_solution_outside(solution, f_delta, distance_matrix):

    available_vertices = list(range(len(distance_matrix)))
    available_vertices = [v for v in available_vertices if v not in solution]
    for sv_idx in range(1,len(solution)-1):
        for av_idx in range(len(available_vertices)):
            #w solution nie podmieniam pierwszego i ostatniego elementu (punkt start-stop)
            #porownaj tylko i wylacznie zmienione krawedzie
            #roznica kosztow dodawanych i usuwanych lukow
            edge1_node1 = solution[sv_idx-1]
            edge1_node2 = solution[sv_idx]

            edge2_node1 = solution[sv_idx]
            edge2_node2 = solution[sv_idx+1]
            cost_edges_to_delete = distance_matrix[edge1_node1,edge1_node2] + distance_matrix[edge2_node1,edge2_node2]

            edge1_node2 = available_vertices[av_idx]
            edge2_node1 = available_vertices[av_idx]
            cost_edges_to_add = distance_matrix[edge1_node1,edge1_node2] + distance_matrix[edge2_node1,edge2_node2]

            current_delta = cost_edges_to_add - cost_edges_to_delete
            if current_delta < f_delta:
                better_vertices = solution.copy()
                better_vertices[sv_idx] = available_vertices[av_idx]
                f_delta = current_delta

    return better_vertices, f_delta


def hybrid_algorithm(distance_matrix):
    population = []

    #wygeneruj populację o wielkosci 20
    for i in range(20):
        while True:
            print('\tlosowanie populacji nr ', i)
            to_add = steepest_change_edges(distance_matrix)
            if to_add not in population:
                population.append(to_add)
                break
            
            

    licznik = 0
    start = time.time()
    stop_condition = 402#496.66

    while True:
        licznik += 1
        end = time.time()
        measured_time = end-start
        print('\t', measured_time)


        if measured_time < stop_condition:
            #wylosuj rodzicow z populacji
            parent1 = []
            parent2 = []
            while parent1==parent2:
                parent1 = random.choice(population)
                parent2 = random.choice(population)



            child = recombination(parent1, parent2, distance_matrix)
            steeped_child = steepest_change_edges(distance_matrix, child)

            #znajdz najgorsze rozwiazanie w populacji
            worst_dist_in_pop = 0
            for pop in population:
                i_distance = sum_weights(pop, distance_matrix)
                if i_distance > worst_dist_in_pop:
                    worst_dist_in_pop = i_distance
                    worst_pop = pop

            #sprawdz czy jest rozne od rozwiazan w populacji
            different = 1
            for pop in population:
                if steeped_child == pop:
                    different = 0


            if sum_weights(steeped_child,distance_matrix) < worst_dist_in_pop and different: #jest lepsze od najgorszego w population
                #usun najgorszy cykl z population
                population.remove(worst_pop)
                #dodaj steeped_child to population
                population.append(steeped_child)
        else:
            break

    return population, licznik


def recombination(parent1, parent2, distance_matrix):
    '''
    Proponowany operator rekombinacji: Wyszukujemy wszystkie
    wspólne podścieżki w obu rodzicach. Podścieżka może być
    pojedynczym wierzchołkiem, pojedynczą krawędzią, lub zbiorem
    połączonych krawędzi.
    Jeżeli suma wierzchołków we wspólnych podścieżakch jest mniejsza
    niż zadana liczba wierzchołków,
    to dodajemy losowo wierzchołki, które należały do jednego z rodziców.
    Podścieżki łączymy w sposób losowy,
    tak aby powstał cykl hamiltona
    '''

    child = list(set(parent1).intersection(parent2))

    #jezeli liczba wspolnych wierzcholkow/krawedzi jest mniejsza niz dlugosc cyklu
    while len(child) < 50:
        #dodajemy losowo wierzcholki ktore nalezay do jednego z rodzicow
        #ale nie sa jeszcze w common

        while True:
            to_add = random.choice(parent1)
            if to_add not in child:
                child.append(to_add)
                break


    return child

def steepest_change_edges(distance_matrix, child=0):
    #poczatek pomiaru czasu
    if child:
        random_nodes = child
    else:
        random_nodes = random.sample(range(100), 50)

    random_nodes.append(random_nodes[0])

    solution = random_nodes.copy()



    while True:
        #licznik+=1
        #print(licznik)
        f_delta = float('inf')
        #ZNAJDZ NAJLEPSZA DELTE W TRASIE
        #ZNAJDZ NAJLEPSZA DELTE POZA TRASA (WYMIANA WIERZCHOLKOW)

        #ZAAPLIKUJ LEPSZA!

        #najlepsze rozwiazanie oraz obecna delta W TRASIE
        better_solution_in, f_delta_in = best_solution_inside(solution, f_delta, distance_matrix)
        better_solution_out, f_delta_out = best_solution_outside(solution, f_delta, distance_matrix)




        if f_delta_in < f_delta_out:
            better_solution = better_solution_in
            f_delta = f_delta_in
        elif f_delta_out <= f_delta_in:
            better_solution = better_solution_out
            f_delta = f_delta_out


        #jezeli ujemna delta - to najlepsza znaleziona podmiana ma sens, w innym wypadku nie
        if f_delta<0:
            solution = better_solution
        else:
            break


    return solution


def display_graph(edges, kro):
    to_display_edges = edges.copy()
    list_of_tuples_with_edges = []
    to_display_edges = [x+1 for x in to_display_edges]
    for i in range(len(to_display_edges)-1):
        list_of_tuples_with_edges.append((to_display_edges[i], to_display_edges[i+1]))

    pos = dict(kro.node_coords)
    G=nx.Graph()
    G.add_nodes_from(kro.get_nodes())
    G.add_edges_from(list_of_tuples_with_edges)
    nx.draw_networkx(G, pos=pos, font_size=13, node_size=300)


def sum_weights(cycle, distance_matrix):
    sum = 0
    for i in range(len(cycle)-1):
        sum = sum + distance_matrix[cycle[i],cycle[i+1]]
    return sum


def check_hybrid(distance_matrix):
    measured_runs = []
    distances = []
    for j in range(10):
        print('iteration: ', j)
        population, measured_run = hybrid_algorithm(distance_matrix)

        #znajdz najlepsze z populacji
        best_dist_in_pop = float('inf')
        for pop in population:
            i_distance = sum_weights(pop, distance_matrix)
            if i_distance < best_dist_in_pop:
                best_dist_in_pop = i_distance
                solution = pop

        distances.append(best_dist_in_pop)
        measured_runs.append(measured_run)

        print(solution)
        print(measured_run)

    print('Number of runs scores: \n')
    print('Max: ', max(measured_runs))
    print('Min: ', min(measured_runs))
    print('Avg: ', sum(measured_runs) / len(measured_runs))
    print('\n', '-' * 20)
    print('\nDistance scores: \n')
    print('Max: ', max(distances))
    print('Min: ', min(distances))
    print('Avg: ', sum(distances) / len(distances))


def show_results(distance_matrix):
    measured_times = []
    distances = []
    for i in range(100):
        print('iteration: ', i)
        solution, measured_time = steepest_change_edges(distance_matrix)
        distances.append(sum_weights(solution,distance_matrix))
        measured_times.append(measured_time)


    print('Time scores: \n')
    print('Max: ', max(measured_times))
    print('Min: ', min(measured_times))
    print('Avg: ', sum(measured_times)/len(measured_times))
    print('\n','-'*20)
    print('\nDistance scores: \n')
    print('Max: ', max(distances))
    print('Min: ', min(distances))
    print('Avg: ', sum(distances)/len(distances))



def main():
    kroa = tsplib95.load(r"C:\Users\skibi\OneDrive\Dokumenty\Informatyka\Aem\tsplib95\archives\problems\tsp\kroA200.tsp")
    krob = tsplib95.load(r"C:\Users\skibi\OneDrive\Dokumenty\Informatyka\Aem\tsplib95\archives\problems\tsp\kroB200.tsp")


    graphA = kroa.get_graph()
    distance_matrix_A = nx.to_numpy_matrix(graphA)

    graphB = krob.get_graph()
    distance_matrix_B = nx.to_numpy_matrix(graphB)




    #population = hybrid_algorithm(distance_matrix_A)

    #check_hybrid(distance_matrix_B)

    population, licznik = check_hybrid(distance_matrix_A) 

    #wybrany  = [5, 108, 106, 156, 46, 30, 176, 12, 14, 122, 197, 190, 39, 11, 17, 109, 28, 183, 36, 117, 15, 62, 50, 193, 121, 115, 187, 43, 152, 65, 118, 91, 9, 174, 32, 155, 99, 35, 56, 73, 141, 68, 40, 29, 67, 34, 1, 180, 124, 186, 5]
    #print(sum_weights(wybrany, distance_matrix_A))
    #display_graph(wybrany, kroa)
    

    
#    solution, times = steepest_change_edges(distance_matrix_A)
#    plt.figure(1)
#    plt.title('steepest')
#    display_graph(solution, kroa)
##
#    plt.figure(2)
#    plt.title('random')
#    display_graph(random_nodes,kroa)

    plt.show()

main()
