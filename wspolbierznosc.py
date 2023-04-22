import threading
import queue
import random
import time
import hashlib

# Zdefiniuj rozmiar bufora
ROZMIAR_BUFORA = 5

# Stwórz wspólną kolejkę (bufor) do przechowywania elementów
bufor = queue.Queue(ROZMIAR_BUFORA)

# Definiuj element sentynela
SENTYNELA = "KONIEC"

class Producent(threading.Thread):
    def __init__(self, plik_wejsciowy):
        super().__init__()
        self.plik_wejsciowy = plik_wejsciowy

    def run(self):
        with open(self.plik_wejsciowy, "r") as plik:
            for linia in plik:
                # Wyprodukuj element (tutaj linia z pliku)
                element = linia.strip()

                # Zdobądź dostęp do bufora, aby umieścić element
                bufor.put(element)
                print(f"Producent {self.name} wyprodukował element {element}")

                # Czekaj losowy czas, aby symulować czas produkcji
                time.sleep(random.uniform(0.1, 1))

        # Dodaj element sentynela po zakończeniu wczytywania pliku
        bufor.put(SENTYNELA)

class Konsument(threading.Thread):
    def __init__(self, plik_wyjsciowy):
        super().__init__()
        self.plik_wyjsciowy = plik_wyjsciowy

    def run(self):
        with open(self.plik_wyjsciowy, "w") as plik:
            while True:
                # Zdobądź dostęp do bufora, aby pobrać element
                element = bufor.get()

                # Jeśli element to sentynela, zakończ wątek konsumenta
                if element == SENTYNELA:
                    break

                print(f"Konsument {self.name} skonsumował element {element}")

                # Haszuj element
                hashowany_element = hashlib.sha256(element.encode()).hexdigest()

                # Zapisz haszowany element do pliku wyjściowego
                plik.write(f"{hashowany_element}\n")

                # Czekaj losowy czas, aby symulować czas konsumpcji
                time.sleep(random.uniform(0.1, 1))

# Utwórz wątki producentów i konsumentów
producent1 = Producent("file1.txt")
producent2 = Producent("file2.txt")
konsument1 = Konsument("plik_wyjsciowy1.txt")
konsument2 = Konsument("plik_wyjsciowy2.txt")

# Uruchom wszystkie wątki
producent1.start()
producent2.start()
konsument1.start()
konsument2.start()

# Dołącz wszystkie wątki
producent1.join()
producent2.join()
