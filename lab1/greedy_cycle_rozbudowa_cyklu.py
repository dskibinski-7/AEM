import tsplib95
import networkx as nx
import random

kroa = tsplib95.load('/home/dawid/INFORMATYKA/AEM/kroA100.tsp')
krob = tsplib95.load('/home/dawid/INFORMATYKA/AEM/kroB100.tsp')

graph = kroa.get_graph()
distance_matrix_A = nx.to_numpy_matrix(graph)
graphB = krob.get_graph()
distance_matrix_B = nx.to_numpy_matrix(graphB)

#greedy cycle
#obliczanie odleglosci:
def sum_weights(cycle):
    sum = 0
    for i in range(len(cycle)-1):
        sum = sum + distance_matrix_A[cycle[i],cycle[i+1]] 
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
    
    #print('Cycle before while:', cycle)
    
    while len(cycle)<50:
        shortest = cycle.copy()
        shortest.insert(1,other_nodes[0])
        #print('shortest before for: ', shortest)
        for n in other_nodes: #wszystkie wiercholki
            for i in range(1,len(cycle)): #na wszystkich pozycjach; od drugiej bo 1 zostala dodana przed petla, zerowa to start, oraz bez ostatniej bo to powrot na poczatek
                other_shortest = cycle.copy()
                other_shortest.insert(i,n)
                #print('other shortest in n:', n, ' i:', i, ' and other_shortest: ', other_shortest)
                if sum_weights(other_shortest) < sum_weights(shortest) and (other_shortest!=shortest): #tutaj zrobic porownanie drog
                    shortest = other_shortest.copy()
                    to_del = n #wierzcholek do usuniecia
        other_nodes.remove(to_del) #gdzie powinny byc usuwane uzyte wierzcholki
        cycle = shortest.copy()
        
    #pamietaj ze to sa wierzcholki o jeden mniejsze w porownaniu z kroa
    scores[start_node] = sum_weights(cycle)
    #print(cycle)
    

print(scores)
sc_list = list(scores.values())
print("Maksimum: ", max(sc_list))
print("Minimum: ", min(sc_list))
print("Srednia: ", sum(sc_list)/len(sc_list))
'''

#pod graf:
#losowanie pierwszego wierzcholka
start_node = 61
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

#print('Cycle before while:', cycle)

while len(cycle)<50:
    shortest = cycle.copy()
    shortest.insert(1,other_nodes[0])
    #print('shortest before for: ', shortest)
    for n in other_nodes: #wszystkie wiercholki
        for i in range(1,len(cycle)): #na wszystkich pozycjach; od drugiej bo 1 zostala dodana przed petla, zerowa to start, oraz bez ostatniej bo to powrot na poczatek
            other_shortest = cycle.copy()
            other_shortest.insert(i,n)
            #print('other shortest in n:', n, ' i:', i, ' and other_shortest: ', other_shortest)
            if sum_weights(other_shortest) < sum_weights(shortest) and (other_shortest!=shortest): #tutaj zrobic porownanie drog
                shortest = other_shortest.copy()
                to_del = n #wierzcholek do usuniecia
    other_nodes.remove(to_del) #gdzie powinny byc usuwane uzyte wierzcholki
    cycle = shortest.copy()
    
#pamietaj ze to sa wierzcholki o jeden mniejsze w porownaniu z kroa
scores[start_node] = sum_weights(cycle)
#print(cycle)
    
########przygotowanie grafu:
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