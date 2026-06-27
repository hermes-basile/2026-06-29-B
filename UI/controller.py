import flet as ft

from model.album import Album


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model


    def handleCreaGrafo(self, e):
        self._model.buildGraph()
        self._view._txt_result.controls.clear()
        self._view._txt_result.controls.append(
            ft.Text("Grafo correttamente creato.")
        )
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di nodi: {self._model.getNumNodi()}")
        )
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumEdges()}")
        )

        self.fillDDAlbums()
        self._view.update_page()

    def handleStampaInfo(self,e):
        self._view._txt_result.controls.clear()

        num_components = self._model.getNumConnectedComponents()
        self._view._txt_result.controls.append(
            ft.Text(f"Numero di componenti connesse: {num_components}")
        )

        self._view._txt_result.controls.append(
            ft.Text(f"")
        )

        largest_component = self._model.getLargestConnectedComponent()
        self._view._txt_result.controls.append(
            ft.Text(f"Dimensione della componente connessa più grande: {len(largest_component)} album")
        )

        self._view._txt_result.controls.append(
            ft.Text(f"")
        )

        self._view._txt_result.controls.append(
            ft.Text("Dettagli degli album appartenenti alla componente connessa più grande:")
        )

        self._view._txt_result.controls.append(
            ft.Text(f"")
        )

        album_info = self._model.getAlbumInfoInLargestComponent()
        for album_title, num_tracks in album_info:
            self._view._txt_result.controls.append(
                ft.Text(f"  - {album_title}: {num_tracks} brani")
            )

        self._view.update_page()

    def handleSelezione(self, e):
        self._view._txt_result.controls.clear()

        if self._AlbumValue is None:
            self._view._txt_result.controls.append(
                ft.Text("Seleziona un album dal menu a tendina.")
            )
            self._view.update_page()
            return

        try:
            N = int(self._view._txtInN.value)
        except ValueError:
            self._view._txt_result.controls.append(
                ft.Text("Inserisci un valore numerico valido per N.")
            )
            self._view.update_page()
            return

        best_selection, total_tracks = self._model.getBestSelection(self._AlbumValue, N)

        if not best_selection:
            self._view._txt_result.controls.append(
                ft.Text("Nessuna selezione trovata.")
            )
            self._view.update_page()
            return

        # Sort albums by title
        sorted_selection = sorted(best_selection, key=lambda album: album.Title)

        self._view._txt_result.controls.append(
            ft.Text("Lista ordinata degli album selezionati:")
        )
        self._view._txt_result.controls.append(ft.Text(""))

        for album in sorted_selection:
            num_tracks = len(album.Tracks)
            #assumo che tutte le tracce abbiano lo stesso genere, per cui prendo il genere del primo brano

            self._view._txt_result.controls.append(
                ft.Text(f"  - {album.Title}: genere {album.Tracks[0].GenreId}, {num_tracks} brani")
            )

        self._view._txt_result.controls.append(ft.Text(""))
        self._view._txt_result.controls.append(
            ft.Text(f"Numero totale di album selezionati: {len(best_selection)}")
        )
        self._view._txt_result.controls.append(
            ft.Text(f"Numero complessivo di brani: {total_tracks}")
        )

        self._view.update_page()

    def fillDDAlbums(self):
        # Populate dropdown with clients
        self._view._ddAlbum.options.clear()
        all_albums = self._model.getAllAlbums()

        albumsDDOptions = list(map(lambda x:ft.dropdown.Option(data=x, key=str(x), on_click=self._choiceAlbum), all_albums ))

        self._view._ddAlbum.options = albumsDDOptions

        self._view.update_page()

    def _choiceAlbum(self, e):
        self._AlbumValue = e.control.data