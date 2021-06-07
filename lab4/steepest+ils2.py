import tsplib95
import networkx as nx
import random
import matplotlib.pyplot as plt
import time
    

'''
Perturbacja2 (ILS2) powinna polegać na usunięciu większej liczby krawędzi 
i wierzchołków (np. 20%) (destroy) i naprawieniu rozwiązania nie losowo, 
ale za pomocą metody heurystycznej (jednej z tych zaimplementowanych na  pierwszych zajęciach). 
Metodą ILS2 implementujemy także w wersji bez wykorzystania lokalnego przeszukiwania (ILS2a).
'''




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


def steepest_change_edges(distance_matrix, random_nodes):
    #poczatek pomiaru czasu
    #start = time.time() 

    
    solution = random_nodes.copy()
    #dopóki da się poprawić (dopóki najlepsze rozwiązanie != obecne rozwiązanie)
    #licznik =0
    
       
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
        
        #koniec mierzenia czasu
    #end = time.time()
    
    #measured_time = end-start
        
    return solution




def isl_two(distance_matrix):
    #wygeneruj rozwiazanie x
    start = time.time()
    stop_condition = 402#496.66 #dla instancji A
    random_nodes = random.sample(range(200), 50)
    random_nodes.append(random_nodes[0])
    
    #zastosuj lokalne przesukiwanie
    x = steepest_change_edges(distance_matrix, random_nodes)
    licznik = 0
    #dopóki nie spełniono warunków stopu (sredni czas Msls)
    while True:
        licznik+=1
        #print('iteracja: ', licznik)
        end = time.time()
        measured_time = end-start
        #print('measured time: ', measured_time)
        
        
        if measured_time < stop_condition:
            #perturbacja x (wymiana kilku wierzcholkow na inne losowe)
            z = perturbation(x.copy(), distance_matrix)
            y = steepest_change_edges(distance_matrix, z)
            
            if sum_weights(y, distance_matrix) < sum_weights(x, distance_matrix):
                x = y           
        else:
            break
        
    return x, licznik


def check_ils(distance_matrix):
    measured_runs = []
    distances = []
    for j in range(10):
        print('iteration: ', j)
        solution, measured_run = isl_two(distance_matrix)
        distances.append(sum_weights(solution,distance_matrix))
        measured_runs.append(measured_run)
        
        print(solution)
        print(measured_run)
    
    
    print('Number of runs scores: \n')
    print('Max: ', max(measured_runs))
    print('Min: ', min(measured_runs))
    print('Avg: ', sum(measured_runs)/len(measured_runs))
    print('\n','-'*20)
    print('\nDistance scores: \n')
    print('Max: ', max(distances))
    print('Min: ', min(distances))
    print('Avg: ', sum(distances)/len(distances))



def perturbation(x, distance_matrix):
    #usun 20% losowych wierzcholkow
    for i in range(10):
        random_ix = random.choice(list(range(len(x))))
        #jezeli pierwszy/ostatni i wciaz sa te same, to usun tez pocz/koniec
        if random_ix == 0 and x[0]==x[-1]:
            del x[-1]
        elif random_ix == 50 and x[0]==x[-1]:
            del x[0]
        
        del x[random_ix]
    
    #jezeli cykl nie jest zamkniety
    if x[0] != x[-1]:
        #domknij
        x.append(x[0])
        
    #zastouj heurystyke; tutaj rozbudowa cyklu
    available_vertices = list(range(200))
    available_vertices = [v for v in available_vertices if v not in x]
    
    while len(x) < 50:
        shortest = x.copy()
        shortest.insert(1,available_vertices[0])
        #print('shortest before for: ', shortest)
        for n in available_vertices: #wszystkie wiercholki
            for i in range(1,len(x)): #na wszystkich pozycjach; od drugiej bo 1 zostala dodana przed petla, zerowa to start, oraz bez ostatniej bo to powrot na poczatek
                other_shortest = x.copy()
                other_shortest.insert(i,n)
                #print('other shortest in n:', n, ' i:', i, ' and other_shortest: ', other_shortest)
                if sum_weights(other_shortest, distance_matrix) < sum_weights(shortest, distance_matrix) and (other_shortest!=shortest): #tutaj zrobic porownanie drog
                    shortest = other_shortest.copy()
                    to_del = n #wierzcholek do usuniecia
        available_vertices.remove(to_del) #gdzie powinny byc usuwane uzyte wierzcholki
        x = shortest.copy()
        
       
    return x
        
    #napraw przy pomocy heurystyki
        


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
    
    #best_msls = msls(distance_matrix_A)
    #solution = isl_two(distance_matrix_A)
    
    check_ils(distance_matrix_B)
    
    #print(solution)
    #print(sum_weights(solution, distance_matrix_A))
    ##show_results(distance_matrix_A)
    
    
#    solution, times = steepest_change_edges(distance_matrix_A)
#    plt.figure(1)
#    plt.title('steepest')    
#    display_graph(solution, kroa)
##    
#    plt.figure(2)
#    plt.title('random') 
#    display_graph(random_nodes,kroa)
    
    #plt.show()

main()
