from model.model import Model
modello_prova = Model()

print(f"La lista che contiene tutti i nodi (non filtrati) è lunga: {len(modello_prova.lista_nodi_totale)}")
#creo il grafo:
modello_prova.crea_grafo()
print(f"Il grafo ha {modello_prova.num_nodi()} nodi, e {modello_prova.num_archi()} archi")

lista_nodi = list(modello_prova._grafo.nodes())
print(lista_nodi[1].lista_tracce)
nodo1 = lista_nodi[1]

print(f"IL NODO 1 è {nodo1}")

#print(modello_prova.lista_componente_maggiore())


#CONTROLLA CHE LA RICORSIONE DIA TUTTI I VINCOLI SIANO GIUSTI E RESTITUISCONO TRUE
soluzione, numero_brani = modello_prova.crea_ricorsione(nodo1, 2)

print("Parte dalla sorgente:", soluzione[0] == nodo1)

print("Nodi non ripetuti:", len(soluzione) == len(set(soluzione)))


print(soluzione)

