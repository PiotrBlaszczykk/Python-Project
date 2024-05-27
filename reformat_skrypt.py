import json
import os

# Ścieżka do pliku JSON
file_path = "NIE UŻYWAĆĆĆĆ!!!"


def custom_format(data):
    """Formatuje określone klucze do jednoliniowego zapisu."""
    if isinstance(data, dict):
        for key, value in data.items():
            if key in ['position', 'scale'] and isinstance(value, dict):
                # Spłaszczenie obiektu do jednej linii
                data[key] = json.dumps(value, separators=(',', ':'))
            else:
                custom_format(value)
    elif isinstance(data, list):
        for item in data:
            custom_format(item)


def reformat_json(file_path):
    # Wczytanie danych JSON z pliku
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Niestandardowe formatowanie danych
    custom_format(data)

    # Zapisanie zmodyfikowanych danych do pliku
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2, separators=(',', ': '))


# Wywołanie funkcji z podaną ścieżką
reformat_json(file_path)
