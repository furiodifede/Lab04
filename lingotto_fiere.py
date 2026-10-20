class Espositore:
    def __init__(self, codice, nome, cognome):
        self.codice = codice
        self.nome = nome
        self.cognome = cognome
        self.stand = None

    def __eq__(self, other):
        if isinstance(other, Espositore):
            return self.codice == other.codice
        return False

    def __str__(self):
        if self.stand:
            return f"{self.codice}: {self.nome} {self.cognome} - Stand assegnato: {self.stand.codice}"
        return f"{self.codice}: {self.nome} {self.cognome} - Nessuno stand assegnato"


class Stand:
    def __init__(self, codice, superficie, padiglione, prezzo_base):
        self.codice = codice
        self.superficie = superficie
        self.padiglione = padiglione
        self.prezzo_base = float(prezzo_base)
        self.disponibile = True
        self.espositore = None

    def calcola_prezzo(self):
        return self.prezzo_base

    def __eq__(self, other):
        if isinstance(other, Stand):
            return self.codice == other.codice
        return False

    def __lt__(self, other):
        return self.calcola_prezzo() < other.calcola_prezzo()

    def __str__(self):
        stato = "Disponibile" if self.disponibile else "Occupato"
        return f"{self.codice}: Standard | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - {stato}"


class StandPreseExtra(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, numero_prese):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.numero_prese = int(numero_prese)

    def calcola_prezzo(self):
        return self.prezzo_base * (1 + 0.07 * self.numero_prese)

    def __str__(self):
        stato = "Disponibile" if self.disponibile else "Occupato"
        return f"{self.codice}: Prese Extra | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - Prese aggiuntive: {self.numero_prese} - {stato}"


class StandPremium(Stand):
    def __init__(self, codice, superficie, padiglione, prezzo_base, posizione):
        super().__init__(codice, superficie, padiglione, prezzo_base)
        self.posizione = posizione

    def calcola_prezzo(self):
        return self.prezzo_base * 1.30

    def __str__(self):
        stato = "Disponibile" if self.disponibile else "Occupato"
        return f"{self.codice}: Premium | {self.superficie} mq - Padiglione {self.padiglione} - Prezzo {self.calcola_prezzo():.2f}€ - Posizione: {self.posizione} - {stato}"


class LingottoFiere:
    def __init__(self, nome):
        self._nome = nome
        self.stand_list = []
        self.espositori_list = []

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nuovo_nome):
        self._nome = nuovo_nome

    def carica_file_dati(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            for riga in file:
                dati = [campo.strip() for campo in riga.strip().split(",") if campo.strip()]
                if not dati:
                    continue

                codice = dati[0]
                if codice.startswith("ES"):
                    espositore = Espositore(codice, dati[1], dati[2])
                    self.espositori_list.append(espositore)
                elif codice.startswith("ST"):
                    superficie = dati[1]
                    padiglione = dati[2]
                    prezzo_base = float(dati[3])

                    if len(dati) == 4:
                        stand = Stand(codice, superficie, padiglione, prezzo_base)
                    elif len(dati) == 5:
                        if dati[4].isdigit():
                            stand = StandPreseExtra(codice, superficie, padiglione, prezzo_base, int(dati[4]))
                        else:
                            stand = StandPremium(codice, superficie, padiglione, prezzo_base, dati[4])

                    self.stand_list.append(stand)

    def assegna_stand_a_espositore(self, codice_stand, codice_espositore):
        stand_trovato = None
        for s in self.stand_list:
            if s.codice == codice_stand:
                stand_trovato = s
                break

        if not stand_trovato:
            raise Exception("Stand non trovato.")

        espositore_trovato = None
        for e in self.espositori_list:
            if e.codice == codice_espositore:
                espositore_trovato = e
                break

        if not espositore_trovato:
            raise Exception("Espositore non trovato.")

        if not stand_trovato.disponibile:
            raise Exception("Stand già occupato.")

        if espositore_trovato.stand is not None:
            raise Exception("Espositore già associato a uno stand.")

        stand_trovato.disponibile = False
        stand_trovato.espositore = espositore_trovato
        espositore_trovato.stand = stand_trovato

    def elenca_espositori(self):
        for espositore in self.espositori_list:
            print(espositore)

    def stand_ordinati_per_prezzo(self):
        return sorted(self.stand_list)
