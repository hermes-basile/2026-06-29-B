import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self.bestSelection = []
        self.max_tracks = 0


    def getBestSelection(self, starting_album, N):

        if starting_album not in self._graph.nodes:
            return []

        connected_components = list(nx.connected_components(self._graph))

        # Find which component contains the starting album
        starting_component = self._getConnectedComponent(starting_album)

        parziale = [starting_album]
        
        comp_rimanenti = copy.deepcopy(connected_components)
        comp_rimanenti.remove(starting_component)

        self._ricorsione(parziale, N, comp_rimanenti)

        return self.bestSelection, self.max_tracks

    def _ricorsione(self, parziale, N, comp_rimanenti):
        print(len(parziale))
        # condizione di terminazione
        if len(parziale) == N:
            total_tracks = self._getTotalTracks(parziale)
            if total_tracks > self.max_tracks:
                self.max_tracks = total_tracks
                self.bestSelection = copy.deepcopy(parziale)
            return

        if not comp_rimanenti or N-len(parziale) > len(comp_rimanenti):
            return

        # provo ad aggiungere album da altre componenti che non ho ancora aggiunto

        # prendo il primo
        nextComp = comp_rimanenti[0]

        # Prima opzione: non prendo nessun album da questa componente, chiamo il metodo ricorsivo
        # passandogli tutte le rimanenti comp connesse tranne nextComp
        # versione verbosa
        # comp_rimanenti_aggiornate = copy.deepcopy(comp_rimanenti)
        # comp_rimanenti_aggiornate.remove(nextComp)
        # self._ricorsione(parziale, N, comp_rimanenti_aggiornate)
        self._ricorsione(parziale, N, comp_rimanenti[1:])

        # Seconda opzione: prendo l'album con più tracce da questa componente e vado avanti, chiamo il metodo ricorsivo
        # passandogli tutte le rimanenti comp connesse tranne nextComp
        best_album = self._getAlbumWithMostTracks(nextComp)

        if best_album is not None:
            parziale.append(best_album)
            # comp_rimanenti_aggiornate = copy.deepcopy(comp_rimanenti)
            # comp_rimanenti_aggiornate.remove(nextComp)
            # comp_rimanenti_aggiornate = copy.deepcopy(comp_rimanenti)
            # comp_rimanenti_aggiornate.remove(nextComp)

            # self._ricorsione(parziale, N, comp_rimanenti_aggiornate)
            self._ricorsione(parziale, N, comp_rimanenti[1:])
            parziale.pop()

    def _getConnectedComponent(self, album):
        #get the connected component that contains the album
        connected_components = list(nx.connected_components(self._graph))
        for component in connected_components:
            if album in component:
                return component
        return None

    def _getTotalTracks(self, albums):
        total = 0
        for album in albums:
            if album.Tracks is not None:
                total += len(album.Tracks)
        return total

    def _getAlbumWithMostTracks(self, albums):
        best_album = None
        max_tracks_in_component = 0
        for album in albums:
            num_tracks = len(album.Tracks) #if album.Tracks is not None else 0
            if num_tracks > max_tracks_in_component:
                max_tracks_in_component = num_tracks
                best_album = album
        return best_album

    def buildGraph(self):
        # read all albums from the database
        albums = DAO.getAllAlbums()

        # Populate each album with its tracks
        for album in albums:
            DAO.getTracksForAlbum(album)

        self._graph.add_nodes_from(albums)

        # double cycle on nodes to check if they have the same genre
        for i, album1 in enumerate(albums):
            for album2 in albums[i + 1:]:
                if self._shareGenre(album1, album2):
                    self._graph.add_edge(album1, album2)

    def _shareGenre(self, album1, album2):
        # check se due album hanno tracce con genere in comune. QUesto è il caso generale in cui considero che tracce
        # presenti nello stesso album hanno tracce diverse. Questo nel db non dovrebbe verificarsi per cui è ridondante.

        if album1.Tracks is None or album2.Tracks is None:
            return False

        # generi presenti in album1
        genres1 = set(track.GenreId for track in album1.Tracks if track.GenreId is not None)
        # generi presenti in album2
        genres2 = set(track.GenreId for track in album2.Tracks if track.GenreId is not None)

        # verifico l'intersezione
        return len(genres1.intersection(genres2)) > 0

    def getNumConnectedComponents(self):
        return nx.number_connected_components(self._graph)

    def getLargestConnectedComponent(self):
        if len(self._graph.nodes) == 0:
            return []

        connected_components = list(nx.connected_components(self._graph))
        largest_component = max(connected_components, key=len)

        return list(largest_component)

    def getAlbumInfoInLargestComponent(self):
        #res = list of (album_title, num_tracks) for each album in the largest connected component
        largest_component = self.getLargestConnectedComponent()

        result = []
        for album in largest_component:
            num_tracks = len(album.Tracks) #if album.Tracks is not None else 0
            result.append((album.Title, num_tracks))

        # Sort by album title
        result.sort(key=lambda x: x[0])

        return result
    
    def getNumNodi(self):
        return len(self._graph.nodes)

    def getNumEdges(self):
        return len(self._graph.edges)

    def getAllAlbums(self):
        return self._graph.nodes