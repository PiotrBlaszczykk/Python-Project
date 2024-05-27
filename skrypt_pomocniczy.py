import json
import os

# Ścieżka do pliku JSON
file_path = "Swędzioł nic tutaj nie ruszaj"
przesuniecie = 540

def shift_positions(file_path):
    # Wczytanie danych JSON z pliku
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Klucze do aktualizacji
    keys_to_update = ['Spawn', 'Warps', 'StaticProps', 'VoidProps']

    # Przesunięcie wartości 'x' o 600 w prawo
    for key in keys_to_update:
        if key in data:
            for item in data[key]:
                if 'position' in item:
                    item['position']['x'] += przesuniecie

    # Zapisanie zmodyfikowanych danych do pliku
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

    # Opcjonalnie: wyświetlenie zmodyfikowanych danych
    print(json.dumps(data, indent=2))


# Wywołanie funkcji z podaną ścieżką
shift_positions(file_path)
