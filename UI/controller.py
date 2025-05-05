import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaOggetti(self, e):
        self._model.buildGraph()
        self._view.txt_result.controls.append(ft.Text(f"Grafo Creato, Il grafo contiene {self._model.getNumNodes()} "
                                                      f"nodi e {self._model.getNumEdges()} archi"))

        self._view._txtIdOggetto.disabled = False
        self._view._btnCompConnessa.disabled = False

        self._view.update_page()


    def handleCompConnessa(self,e):
        txtInput = self._view._txtIdOggetto.value

        if txtInput == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"INSERIRE UN ID VALIDO", color="red"))
            self._view.update_page()
            return

        try:
            idInput = int(txtInput)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Il valore inserito non è un numero", color="red"))
            self._view.update_page()
            return

        if not self._model.hasNode(idInput):
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("l'ID inserito non corrisponde ad un oggetto del DB", color="red"))
            self._view.update_page()
            return


        sizeInfoConnessa = self._model.getInfoConnessa(idInput)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"La componente connessa che contiene il nodo {self._model.getObjectFromId(idInput)} ha dimensione"
                                                      f" pari a {sizeInfoConnessa}"))
        self._view.update_page()

        pass

