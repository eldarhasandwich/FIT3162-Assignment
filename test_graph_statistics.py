
import classes.AdjacencyList as AL
import graph_statistics as GS

def init_adjlist(adjList = None):
    if not adjList:
        adjList = AL.AdjacencyList()
    
    # instansiate an adjlist from file
    f = open('plaintexts/adjlist_test.txt')
    data = f.readlines()
    f.close
    for line in data:
        a = line.split(' ')
        adjList.AddSenderRecipientPair(a[0], a[1], a[2], a[3][:-1])

    return adjList

def init_graphStats_from_adjlist(adjList):
    graphStats = GS.GraphStatistics()
    for key, value in adjList.senders.items():
        graphStats.add_data(value)

    return graphStats

def init_graphStats():
    al = init_adjlist()
    return init_graphStats_from_adjlist(al)

def test_number_of_nodes():
    gs = init_graphStats()

    assert gs.number_of_nodes() == 4

def test_number_of_edges():
    gs = init_graphStats()

    assert gs.number_of_edges() == 8

def test_max_edges():
    gs = init_graphStats()

    assert gs.max_edges() == 12

def test_get_density():
    gs = init_graphStats()

    assert gs.get_density() == 8/12

def test_degree_centalitry():
    gs = init_graphStats()

    assert gs.degree_centrality('1') == 2
    assert gs.degree_centrality('2') == 2
    assert gs.degree_centrality('3') == 3
    assert gs.degree_centrality('4') == 1

def test_shortest_path():
    gs = init_graphStats()

    assert gs.shortest_path_between_two_nodes('1', '2') == ['2', '1']
    assert gs.shortest_path_between_two_nodes('1', '3') == ['3', '1']
    assert gs.shortest_path_between_two_nodes('1', '4') == ['4', '1'] #
    assert gs.shortest_path_between_two_nodes('2', '3') == ['3', '2']
    assert gs.shortest_path_between_two_nodes('2', '4') == ['4', '1', '2']
    assert gs.shortest_path_between_two_nodes('3', '4') == ['4', '3']

def test_betweenness_centrality():
    gs = init_graphStats()

    assert gs.betweenness_centrality('1') == 7
    assert gs.betweenness_centrality('2') == 6
    assert gs.betweenness_centrality('3') == 6
    assert gs.betweenness_centrality('4') == 6

def test_closeness_centrality():
    gs = init_graphStats()

    assert gs.closeness_centrality('1') == 0.16666666666666666
    assert gs.closeness_centrality('2') == 0.14285714285714285
    assert gs.closeness_centrality('3') == 0.16666666666666666
    assert gs.closeness_centrality('4') == 0.16666666666666666

def test_harmonic_centrality():
    gs = init_graphStats()

    assert gs.harmonic_centrality('1') == 1.5
    assert gs.harmonic_centrality('2') == 1.3333333333333333
    assert gs.harmonic_centrality('3') == 1.5
    assert gs.harmonic_centrality('4') == 1.5

def test_eigenvector_centralityy():
    gs = init_graphStats()

    eCentrality = gs.eigenvector_centrality(100)

    assert eCentrality == {'1': 0.25, '2': 0.25, '3': 0.25, '4': 0.25}
    