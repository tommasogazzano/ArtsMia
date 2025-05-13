import copy

import networkx as nx
from networkx.classes import neighbors

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = DAO.getAllNodes()
        self._idMap = {}
        self._bestPath = []
        self._bestCost = 0
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


    def getOptimalPath(self, source, lun):
        self._bestPath = []
        self._bestCost = 0
        # ri-inizializzo tutto

        parziale = [source]  # inizializzo la sol parziale con source perché sicuramente ci deve essere
        for n in nx.neighbors(self._graph, source):
            if parziale[-1].classification == n.classification:
                parziale.append(n)
                self._ricorsione(parziale, lun)
                parziale.pop()


        return self._bestPath, self._bestCost

    def _ricorsione(self, parziale, lun):
        # controllo se parziale è una soluzione
        if len(parziale) == lun:  # parziale ha la lunghezza desiderata
        # verifico se è una soluzione migliore e in ogni caso esco
            if self.costo(parziale) > self._bestCost:
                self._bestCost = self.costo(parziale)
                self._bestPath = copy.deepcopy(parziale)

            return
        # se arrivo qui parziale può ancora ammettere altri nodi
        for n in self._graph.neighbors(parziale[-1]):
            if parziale[-1].classification == n.classification:
                parziale.append(n)
                self._ricorsione(parziale, lun)
                parziale.pop()



    def costo(self, listObject):
        # deve sommare gli archi della lista
        totCosto = 0
        for i in range(0, len(listObject)-1):   # -1 perché devo cercare gli archi
            totCosto += self._graph[listObject[i]][listObject[i+1]]["weight"]
        return totCosto








