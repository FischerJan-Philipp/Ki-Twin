import re

# Öffnen und lesen Sie die .txt Datei
with open('gefilterte_nachrichten.txt', 'r', encoding='utf-8') as file:
    content = file.read()

# Entfernen Sie das Datum (z.B. [25.10.23, 12:02:13])
content_without_date = re.sub(r'\[\d+\.\d+\.\d+, \d+:\d+:\d+\]', '', content)

print(content_without_date)

# Filtern Sie Emojis und behalten Sie den Namen "Jan:"
filtered_content = re.sub(r'Jan:', '', content_without_date)



# Ausgabe des gefilterten Texts
print(filtered_content)



# Regulärer Ausdruck, um Emojis zu extrahieren
emoji_pattern = re.compile(
    r"[" 
    r"\U0001F600-\U0001F64F"  # Emoticons
    r"\U0001F300-\U0001F5FF"  # Symbols & Pictographs
    r"\U0001F680-\U0001F6FF"  # Transport & Map Symbols
    r"\U0001F1E0-\U0001F1FF"  # Flags (iOS)
    r"]+", flags=re.UNICODE
)

# Finden Sie alle Emojis im gefilterten Text
emojis = emoji_pattern.findall(filtered_content)

# Entfernen Sie die Emojis aus dem Text
text_without_emojis = emoji_pattern.sub('', filtered_content)

# Ausgabe der gefundenen Emojis
print("Gefundene Emojis:", emojis)
# Ausgabe des Texts ohne Emojis
print("Text ohne Emojis:", text_without_emojis)

with open("gefilterte_nachrichten_emoji.txt", "w", encoding="utf-8") as output_file:
    for message in text_without_emojis:
        output_file.write(message)


