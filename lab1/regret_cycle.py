import tsplib95
import networkx as nx
import random

kroa = tsplib95.load('/home/dawid/INFORMATYKA/AEM/kroA100.tsp')
krob = tsplib95.load('/home/dawid/INFORMATYKA/AEM/kroB100.tsp')

graph = kroa.get_graph()
distance_matrix_A = nx.to_numpy_matrix(graph)
graphB = krob.get_graph()
distance_matrix_B = nx.to_numpy_matrix(graphB)

#regret
#obliczanie odleglosci:
def sum_weights(cycle):
    sum = 0
    for i in range(len(cycle)-1):
        sum = sum + distance_matrix_B[cycle[i],cycle[i+1]] 
    return sum

t=0
#klucz to punkt startowy, value to dlugosc drogi
scores = {}
'''
while t<50:
    t+=1

    #losowanie pierwszego wierzcholka
    start_node = random.randint(0,99)
    print(start_node)
    cycle = []
    cycle.append(start_node)
    
    #lista pozostalych wiercholkow
    other_nodes = list(range(0,100)) 
    other_nodes.remove(start_node)
    
    #wybierz najblizszy wiercholek i stworz z tych dwoch wierzcholkow niepelny cyk
    closest = other_nodes[0]
    for n in other_nodes: #sprawdzac trzeba tylko w pozostalych!
        #n to sprawdzany wierzcholek do poprowadzenia drogi; current to wiercholek z ktorego szukamy drogi
        if (distance_matrix_B[start_node, n]<distance_matrix_B[start_node, closest]) and (start_node != n):
            closest = n
    
    cycle.append(closest)
    cycle.append(start_node)
    other_nodes.remove(closest)
    
    #current_cost = sum_weights(cycle) #obecny koszt
    #do tego momentu mam niepelny cykl


    while len(cycle)<50:
        regret_for_ns = {}
        #uzyskaj tablice kosztow dla elementu n
        for n in other_nodes:
            #uzyskac tablice kosztow dla n wierzcholka
            #posortowac ja
            #wyznaczyc roznice miedzy pierwszym a drugim 
            #wybieramy ten wierzcholek, ktory bedzie miec najwiekskzy zal
            #wstawiamy go w najlepsze miejsce!
            cost_table_for_node = []
            for i in range(0, len(cycle)-1): #obliczanie kosztow na poszcz. pozycjach
                cycle_with_n = cycle.copy()
                cycle_with_n.insert(i,n)
                cost_table_for_node.append(sum_weights(cycle_with_n)-sum_weights(cycle)) #koszt wstawienia
                #TUTAJ MUSI BYC DO KAZDEGO WIERZCHOLKA ODDZIELNIE! koszt miedzy node a obecnymi w cycle
                #cost_table_for_node.append(distance_matrix_B[n,cycle[i]])
                
            cost_table_for_node.sort()
            regret_for_current_n = cost_table_for_node[0] - cost_table_for_node[1] #2-zal miedzy peirwszym i drugim
            regret_for_ns[n] = regret_for_current_n
        max_regret = max(regret_for_ns, key=regret_for_ns.get) #wierzcholek z najwiekszym zalem
        other_nodes.remove(max_regret)
        #wstawic w najlepsze miejsce
        shortest = cycle.copy()
        shortest.insert(1,max_regret)
        for i in range(1,len(cycle)): #na wszystkich pozycjach; od drugiej bo 1 zostala dodana przed petla, zerowa to start, oraz bez ostatniej bo to powrot na poczatek
            other_shortest = cycle.copy()
            other_shortest.insert(i,max_regret)
            if sum_weights(other_shortest) < sum_weights(shortest) and (other_shortest!=shortest): #tutaj zrobic porownanie drog
                shortest = other_shortest.copy()
        cycle = shortest.copy()
        
    
    scores[start_node] = sum_weights(cycle)
#print(cycle)
    

print(scores)
sc_list = list(scores.values())
print("Maksimum: ", max(sc_list))
print("Minimum: ", min(sc_list))
print("Srednia: ", sum(sc_list)/len(sc_list))


'''
#POD GRAF:
#losowanie pierwszego wierzcholka
start_node = 14#random.randint(0,99)
print(start_node)
cycle = []
cycle.append(start_node)

#lista pozostalych wiercholkow
other_nodes = list(range(0,100)) 
other_nodes.remove(start_node)

#wybierz najblizszy wiercholek i stworz z tych dwoch wierzcholkow niepelny cyk
closest = other_nodes[0]
for n in other_nodes: #sprawdzac trzeba tylko w pozostalych!
    #n to sprawdzany wierzcholek do poprowadzenia drogi; current to wiercholek z ktorego szukamy drogi
    if (distance_matrix_A[start_node, n]<distance_matrix_A[start_node, closest]) and (start_node != n):
        closest = n

cycle.append(closest)
cycle.append(start_node)
other_nodes.remove(closest)

#current_cost = sum_weights(cycle) #obecny koszt
#do tego momentu mam niepelny cykl


while len(cycle)<50:
    regret_for_ns = {}
    #best_i_for_ns = {}
    #uzyskaj tablice kosztow dla elementu n
    for n in other_nodes:
        #uzyskac tablice kosztow dla n wierzcholka
        #posortowac ja
        #wyznaczyc roznice miedzy pierwszym a drugim 
        #wybieramy ten wierzcholek, ktory bedzie miec najwiekskzy zal
        #wstawiamy go w najlepsze miejsce!
        cost_table_for_node = []
        #best_i_for_ns[n] = 1
        for i in range(0, len(cycle)-1): #obliczanie kosztow na poszcz. pozycjach
            cycle_with_n = cycle.copy()
            cycle_with_n.insert(i,n)
            cost_table_for_node.append(sum_weights(cycle_with_n)-sum_weights(cycle)) #koszt wstawienia
            #TUTAJ MUSI BYC DO KAZDEGO WIERZCHOLKA ODDZIELNIE! koszt miedzy node a obecnymi w cycle
            #cost_table_for_node.append(distance_matrix_B[n,cycle[i]])
            
        cost_table_for_node.sort()
        regret_for_current_n = cost_table_for_node[0] - cost_table_for_node[1] #2-zal miedzy peirwszym i drugim
        regret_for_ns[n] = regret_for_current_n
    max_regret = max(regret_for_ns, key=regret_for_ns.get) #wierzcholek z najwiekszym zalem
    other_nodes.remove(max_regret)
    #wstawic w najlepsze miejsce
    shortest = cycle.copy()
    shortest.insert(1,max_regret)
    for i in range(1,len(cycle)): #na wszystkich pozycjach; od drugiej bo 1 zostala dodana przed petla, zerowa to start, oraz bez ostatniej bo to powrot na poczatek
        other_shortest = cycle.copy()
        other_shortest.insert(i,max_regret)
        if sum_weights(other_shortest) < sum_weights(shortest) and (other_shortest!=shortest): #tutaj zrobic porownanie drog
            shortest = other_shortest.copy()
    cycle = shortest.copy()
    

scores[start_node] = sum_weights(cycle)



#DISPLAY GRAF
to_display_edges = cycle.copy()
list_of_tuples_with_edges = []
to_display_edges = [x+1 for x in to_display_edges]
for i in range(len(to_display_edges)-1):
    list_of_tuples_with_edges.append((to_display_edges[i], to_display_edges[i+1]))
    
pos = dict(krob.node_coords)
G=nx.Graph()
G.add_nodes_from(kroa.get_nodes())
G.add_edges_from(list_of_tuples_with_edges)
nx.draw_networkx(G, pos=pos, font_size=5, node_size=40)
print(sum_weights(cycle))

