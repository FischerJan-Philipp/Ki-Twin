
chat_file = "Data/_chat.txt"

# Öffne die Datei im Lesemodus
with open(chat_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Definiere den Namen oder die Nummer der Person, deren Nachrichten du filtern möchtest
filter_name = "Jan"

# Initialisiere eine leere Liste, um die gefilterten Nachrichten zu speichern
filtered_messages = []

# Durchlaufe die Zeilen der Chat-Datei
for line in lines:
    # Prüfe, ob die Zeile eine Nachricht ist
    if filter_name in line:
        # Wenn ja, füge sie zu den gefilterten Nachrichten hinzu
        filtered_messages.append(line)

# Schreibe die gefilterten Nachrichten in eine separate Datei oder gib sie auf der Konsole aus
with open("gefilterte_nachrichten.txt", "w", encoding="utf-8") as output_file:
    for message in filtered_messages:
        output_file.write(message)

# Alternativ, gib die gefilterten Nachrichten auf der Konsole aus
for message in filtered_messages:
    print(message)
