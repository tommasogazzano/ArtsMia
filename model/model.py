import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMap = {}
        for node in self._nodes:
            self._idMap[node.object_id] = node


    def buildGraph(self):
        self._graph.add_nodes_from(self._nodes)
        self.addAllEdges()

    def getNumNodes(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getIdMap(self):
        return self._idMap

    def getAllEdgesV1(self):
        for u in self._nodes:
            for v in self._nodes:
                peso = DAO.getPeso(u,v)
                if peso is not None:
                    self._graph.add_edge(u, v, weight=peso)

    def addAllEdges(self):
        allEdges = DAO.getAllEdges(self._idMap)
        for e in allEdges:
            self._graph.add_edge(e.o1, e.o2, weight=e.peso)

    def getInfoConnessa(self, idInput):
        '''
        identifica la componente connessa che contiene idInput e ne restituisce la dimensione
        '''

        if not self.hasNode(idInput):
            return None

        source = self._idMap[idInput]

        #modo 1: conto i successori --> non c'è SOURCE
        succ = nx.dfs_successors(self._graph, source)
        print("Size connessa con modo 1: ", len(succ.values()))


        #modo 2: conto i predecessori --> Non c'è SOURCE
        pred = nx.dfs_predecessors(self._graph, source)
        print("Size connessa con modo 2: ", len(pred.values()))

        # NB --> I VALORI SONO DIVERSI --> VERIFICHIAMO CONTANDO I NODI DELL'ALBERO DI VISITA


        #modo 3: conto i nodi dell'albero di visita
        dfsTree = nx.dfs_tree(self._graph, source)
        print("Size connessa con modo 3: ", len(dfsTree.nodes()))
        # sembra che i pred sia giusto e il succ sia sbagliato!

        # con il debug vediamo che il succ non conta i vari nodi, ma conta la lista delle connesse
        # si risolve facendo res = []
        # for s in succ: res.extend(s) --> così creiamo una lista con tutti i nodi --> siamo sicuri che
        # la componente connetta sia giusta

        # NB -> c'è un metodo di nx per fare tutto questo

        #modo 4: uso il metodo nodes_connected_component di networkx

        conn = nx.node_connected_component(self._graph, source)
        print("Size connessa con modo 4: ", len(conn))

        return len(conn)


    def hasNode(self, idInput):
        return idInput in self._idMap

    def getObjectFromId(self, idInput):
        return self._idMap[idInput]
