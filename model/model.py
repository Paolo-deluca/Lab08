from database import distributore_DAO, prezzo_DAO
from database.distributore_DAO import DistributoreDAO
from model import prezzo_DTO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789)
        """
        # TODO
        prezzi_a = prezzo_DAO.PrezzoDAO.get_prezzi(1)
        prezzi_b = prezzo_DAO.PrezzoDAO.get_prezzi(2)

        somma_a = 0
        giorni_a = 0
        for prezzo in prezzi_a:
            parti_data = str(prezzo.data).split("-")
            mese_corrente = int(parti_data[1])
            if mese_corrente == mese:
                somma_a += prezzo.prezzo_litro
                giorni_a += 1

        somma_b = 0
        giorni_b = 0
        for prezzo in prezzi_b:
            parti_data = str(prezzo.data).split("-")
            mese_corrente = int(parti_data[1])
            if mese_corrente == mese:
                somma_b += prezzo.prezzo_litro
                giorni_b += 1

        media_a = somma_a / giorni_a if giorni_a > 0 else 0
        media_b = somma_b / giorni_b if giorni_b > 0 else 0

        return [("Distributore A", media_a), ("Distributore B", media_b)]

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, prezzi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana):
        """ Implementa la ricorsione """
        # TODO
        if giorno > 7:
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = list(sequenza_parziale)
            return

        for id_dist in [1, 2]:
            prezzo_litro = prezzi_settimana[id_dist][giorno - 1]
            costo_giornaliero = prezzo_litro * 100

            spostamento = 5 if ultimo_distributore is not None and ultimo_distributore != id_dist else 0
            nuovo_costo = costo_corrente + costo_giornaliero + spostamento

            sequenza_parziale.append(id_dist)
            self.__ricorsione(sequenza_parziale, giorno + 1, id_dist, nuovo_costo, prezzi_settimana)
            sequenza_parziale.pop()

    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        # TODO
        dizionario_prezzi = {}

        for id_dist in [1, 2]:
            lista_prezzi = prezzo_DAO.PrezzoDAO.get_prezzi(id_dist)
            giorni_7 = {}
            for p in lista_prezzi:
                parti_data = str(p.data).split("-")
                mese_corrente = int(parti_data[1])
                giorno_corrente = int(parti_data[2])

                if mese_corrente == mese and 1 <= giorno_corrente <= 7:
                    giorni_7[giorno_corrente] = p.prezzo_litro
            lista_ordinata = [giorni_7[g] for g in range(1, 8)]
            dizionario_prezzi[id_dist] = lista_ordinata


        return dizionario_prezzi