import tsplib95
import networkx as nx
import random
#nearest neighbour
#mam macierz odleglosci pomiedzy wiercholkami 0...99, [i,j] - odleglosc miedzy itym a jotym wierzcholkiem

kroa = tsplib95.load('/home/dawid/INFORMATYKA/AEM/kroA100.tsp')
krob = tsplib95.load('/home/dawid/INFORMATYKA/AEM/kroB100.tsp')

graph = kroa.get_graph()
distance_matrix_A = nx.to_numpy_matrix(graph)

graphB = krob.get_graph()
distance_matrix_B = nx.to_numpy_matrix(graphB)


def sum_weights(cycle):
    sum = 0
    for i in range(len(cycle)-1):
        sum = sum + distance_matrix_A[cycle[i],cycle[i+1]] 
    return sum

#klucz to punkt startowy, value to dlugosc drogi
scores = {}
t=0

while t<50:
    t+=1
    #losowanie pierwszego wierzcholka
    start_node = random.randint(0,99)
    #print(start_node)
    solved_nodes = []
    solved_nodes.append(start_node)
    
    #lista pozostalych wiercholkow
    other_nodes = list(range(0,100)) 
    other_nodes.remove(start_node)
    
    #powtarzaj poki nie znajdziesz 50 wiercholkow
    while len(solved_nodes)<50:
        current_node = solved_nodes[-1] #ostatnio dodany wiercholek
        #znajdz najblizszy
        closest = other_nodes[0] #pierwszy lepszy wiercholek z pozostalych
        for n in other_nodes: #sprawdzac trzeba tylko w pozostalych!
            #n to sprawdzany wierzcholek do poprowadzenia drogi; current to wiercholek z ktorego szukamy drogi
            if (distance_matrix_B[current_node, n]<distance_matrix_B[current_node, closest]) and (current_node != n):
                closest = n
        solved_nodes.append(closest)
        other_nodes.remove(closest)
    
            
    solved_nodes.append(start_node)
    scores[start_node] = sum_weights(solved_nodes)


print(scores)
sc_list = list(scores.values())
print("Maksimum: ", max(sc_list))
print("Minimum: ", min(sc_list))
print("Srednia: ", sum(sc_list)/len(sc_list))







# ##############pod graf:
# start_node = 80#random.randint(0,99)
# #print(start_node)
# solved_nodes = []
# solved_nodes.append(start_node)

# #lista pozostalych wiercholkow
# other_nodes = list(range(0,100)) 
# other_nodes.remove(start_node)

# #powtarzaj poki nie znajdziesz 50 wiercholkow
# while len(solved_nodes)<50:
#     current_node = solved_nodes[-1] #ostatnio dodany wiercholek
#     #znajdz najblizszy
#     closest = other_nodes[0] #pierwszy lepszy wiercholek z pozostalych
#     for n in other_nodes: #sprawdzac trzeba tylko w pozostalych!
#         #n to sprawdzany wierzcholek do poprowadzenia drogi; current to wiercholek z ktorego szukamy drogi
#         if (distance_matrix_A[current_node, n]<distance_matrix_A[current_node, closest]) and (current_node != n):
#             closest = n
#     solved_nodes.append(closest)
#     other_nodes.remove(closest)

        
# solved_nodes.append(start_node)
# scores[start_node] = sum_weights(solved_nodes)

# print(sum_weights(solved_nodes))

# ########przygotowanie grafu:
# to_display_edges = solved_nodes.copy()
# list_of_tuples_with_edges = []
# to_display_edges = [x+1 for x in to_display_edges]
# for i in range(len(to_display_edges)-1):
#     list_of_tuples_with_edges.append((to_display_edges[i], to_display_edges[i+1]))
    
# pos = dict(krob.node_coords)
# G=nx.Graph()
# G.add_nodes_from(kroa.get_nodes())
# G.add_edges_from(list_of_tuples_with_edges)
# nx.draw_networkx(G, pos=pos, font_size=5, node_size=40)
