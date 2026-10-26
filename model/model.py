import copy

import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self.lista_nodi_totale = DAO.getAllNodes()

        self.idMapObject = {}
        for nodo in self.lista_nodi_totale:
            self.idMapObject[nodo.AlbumId] = nodo

        self._grafo = nx.Graph()

    def crea_grafo(self):
        self._grafo.clear()

        lista_id = DAO.getNodi()

        lista_nodi = []

        for id_nodo in lista_id:
            nodo = self.idMapObject[id_nodo]
            DAO.fillTracce(nodo)
            lista_nodi.append(nodo)

        self._grafo.add_nodes_from(lista_nodi)

        self.add_archi_model()

    def add_archi_model(self):
        lista_nodi = list(self._grafo.nodes())

        for i in range(len(lista_nodi)):
            for j in range(i + 1, len(lista_nodi)):

                u = lista_nodi[i]
                v = lista_nodi[j]
                lista_u = u.lista_tracce
                lista_v = v.lista_tracce
                for a in range(len(lista_u)):
                    for b in range( len(lista_v)):
                        genere_a = lista_u[a]["genreName"]
                        genere_b = lista_v[b]["genreName"]
                        if genere_a == genere_b:
                            if not self._grafo.has_edge(u, v):
                                self._grafo.add_edge(u, v)

    def numero_di_componenti_connesse(self):
        return nx.number_connected_components(self._grafo)

    def ordina_alfabeticamente_album(self):
        pass

    def lista_componente_maggiore(self):
        set_componente_maggiore = (max(nx.connected_components(self._grafo), key=len))
        lista = list(set_componente_maggiore)
        return lista

    def lista_componente_maggiore_ordinata(self):
        lista = self.lista_componente_maggiore()
        lista_ordinata = sorted(lista, key=lambda album:album.Title)
        return lista_ordinata

    def lista_nodi_album_ordinata_alfabeticamente(self):
        lista = self._grafo.nodes()
        lista_ordinata = sorted(lista, key=lambda album: album.Title)
        return lista_ordinata

    def ordina_lista_ricorsione(self, lista):
        lista_ordinata = sorted(lista, key=lambda album: album.Title)
        return lista_ordinata






    def crea_ricorsione(self, source, N):
        self.soluzione = []

        self.numero_brani_ottimo = None

        self.dizionario = {}
        for nodo in list(self._grafo.nodes()):
            self.dizionario[nodo] = nx.node_connected_component(self._grafo, nodo)

        self.ricorsione([source], N)

        return self.soluzione, self.numero_brani_ottimo

    def ricorsione(self, parziale, N):
        if len(parziale) == N:
            numero_brani = self.conta_brani_in_lista(parziale)
            if self.numero_brani_ottimo is None:
                self.soluzione = copy.deepcopy(parziale)
                self.numero_brani_ottimo = numero_brani


            if numero_brani > self.numero_brani_ottimo:
                self.soluzione = copy.deepcopy(parziale)
                self.numero_brani_ottimo = numero_brani

            return





        for candidato in list(self._grafo.nodes()):
            if self.is_ammissibile(candidato, parziale):
                parziale.append(candidato)
                self.ricorsione(parziale, N)
                parziale.pop()



    def is_ammissibile(self, candidato, parziale):
        ammissibile = True
        if candidato in parziale:
            return False
        for nodo_parziale in parziale:
            lista_componente = set(self.dizionario[nodo_parziale])
            if candidato in lista_componente:
                return False
        return ammissibile




    def conta_brani_in_lista(self,lista):
        count = 0
        for album in lista:
            numero_brani = len(album.lista_tracce)
            count += numero_brani
        return count







    def num_nodi(self):
        return len(self._grafo.nodes)

    def num_archi(self):
        return len(self._grafo.edges)