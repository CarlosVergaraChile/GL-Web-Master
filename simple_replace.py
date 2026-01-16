# Script simple para reemplazar texto
import codecs

# Leer archivo
with codecs.open('index.html', 'r', 'utf-8-sig') as f:
    text = f.read()

# Buscar y contar
count_before = text.count('Gast')
print(f'Lineas con Gast: {count_before}')

# Intentar varios tipos de apostrofes
apostrophes = ["'", "'", "`", "´", "'"]
replaced = False

for ap in apostrophes:
    search_text = f"Gastón L{ap}Huillier"
    if search_text in text and "Troncoso" not in text[text.find(search_text):text.find(search_text)+50]:
        print(f'Encontrado con apostrofe: {repr(ap)} (unicode {ord(ap)})')
        new_text = text.replace(search_text, f"Gastón L{ap}Huillier Troncoso")
        replaced = True
        break

if replaced:
    with codecs.open('index.html', 'w', 'utf-8-sig') as f:
        f.write(new_text)
    print('REEMPLAZADO EXITOSAMENTE')
else:
    print('NO SE PUDO ENCONTRAR EL TEXTO')
