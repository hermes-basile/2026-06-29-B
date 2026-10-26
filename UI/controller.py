import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self.result1 = None


    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()
        self._view._btnStampaInfo.disabled = True


        # messaggio di attesa se ci vuole tempo per creare il grafo
        self._view._txt_result.controls.append(
            ft.Text("Stiamo creando il grafo, aspetta qualche secondo.."))
        self._view.update_page()

        # Creare il grafo da model e pulire la view
        self._model.crea_grafo()
        self._view._txt_result.controls.clear()

        # scrivere all'utente che è tutto ok, nodi e archi
        self._view._txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato. ", color="green"))

        self._view._txt_result.controls.append(ft.Text(
            f"Il grafo ha {self._model.num_nodi()} nodi e {self._model.num_archi()} archi."))

        self._view._btnStampaInfo.disabled = False
        self.fill_DD()

        self._view.update_page()

    def handleStampaInfo(self,e):
        # pulizia view
        self._view._txt_result.controls.clear()
        # scrivere
        self._view._txt_result.controls.append(ft.Text(f"Numero componenti connesse:{self._model.numero_di_componenti_connesse()}\n"))
        self._view._txt_result.controls.append(
            ft.Text(f"Dimensione della componente connessa più grande: {len(self._model.lista_componente_maggiore())} album \n"))

        lista_album_ordinata = self._model.lista_componente_maggiore_ordinata()

        for album_nodo in lista_album_ordinata:
            self._view._txt_result.controls.append(ft.Text(f"- {album_nodo.Title} con {len(album_nodo.lista_tracce)} brani"))
        # aggiornare la pagina
        self._view.update_page()

    def fill_DD(self):



        self._view._ddAlbum.options.clear()
        self._view._ddAlbum.value = None
        self.result1 = None

        lista_da_caricare = self._model.lista_nodi_album_ordinata_alfabeticamente()

        # se l'elemento è formato da oggetti classe
        for elemento in lista_da_caricare:
            self._view._ddAlbum.options.append(
                ft.dropdown.Option(
                    text=str(elemento),
                    data=elemento,
                    on_click=self.readResult1
                )
            )

    def readResult1(self, e):
        self.result1 = e.control.data

    def handleSelezione(self,e):
        scelta_utente = self.result1
        if scelta_utente is None:
            self._view._txt_result.controls.append(ft.Text(
                "Attenzione prima di proseguire è necessario scegliere un opzione del dropdown", color="red"))
            self._view.update_page()

            return

        self._view._txt_result.controls.clear()

        txt_in = self._view._txtInN.value

        # controllo se ha scritto qualcosa
        if txt_in is None or txt_in.strip() == "":
            self._view._txt_result.controls.append(ft.Text(
                "Devi inserire un valore valido", color="red"))
            self._view.update_page()
            return

        try:
            number = int(txt_in)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text(
                "Attenzione, gli unici caratteri ammessi sono da 0 a 9: puoi inserire solo numeri", color="red"))
            self._view.NOMEVIEW.value = ""
            self._view.update_page()
            return

        self._view._txt_result.controls.append(ft.Text(f"Tutti i dati inseriti sono coerenti", color="green"))


        lista_soluzione, numero_brani_totali = self._model.crea_ricorsione( scelta_utente, number)

        lista_soluzione_ordinata = self._model.ordina_lista_ricorsione(lista_soluzione)

        # pulizia view
        self._view._txt_result.controls.clear()
        # scrivere
        self._view._txt_result.controls.append(ft.Text(f"Il numero totale di album della ricorsione è: {number} \n"))
        self._view._txt_result.controls.append(ft.Text(f"Il numero totale di brani è {numero_brani_totali}"))
        self._view._txt_result.controls.append(ft.Text(f"Di seguito gli album, in ordine alfabetico, con alcune info: \n"))
        for album in lista_soluzione_ordinata:

            self._view._txt_result.controls.append(ft.Text(f"{album.Title}, genere id:{album.AlbumId}, con {len(album.lista_tracce)} brani"))

        # aggiornare la pagina
        self._view.update_page()



