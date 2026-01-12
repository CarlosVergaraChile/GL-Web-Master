import zipfile
import re
from pathlib import Path

FILES = [
    'assets/docs/CAM+.docx',
    'assets/docs/ecoparque_industrial_arica.docx',
    'assets/docs/presentacion_a_cliente_01.docx',
    'assets/docs/presentacion_a_cliente_02.docx',
    'assets/docs/permisologia.docx',
]

KEYS = ['eje', 'ejes', 'cuadrante', 'Excel', 'Adhoc', 'Reborn', 'RIP', 'matriz', 'CAF', 'SEM']

def extract(path: Path):
    with zipfile.ZipFile(path) as z:
        data = z.read('word/document.xml').decode('utf-8', 'ignore')
    text = re.sub(r'<[^>]+>', ' ', data)
    text = re.sub(r'\s+', ' ', text)
    return text

for rel in FILES:
    path = Path(rel)
    full = Path(__file__).parent / path
    text = extract(full)
    with open(Path(__file__).parent / 'extract_output.txt', 'a', encoding='utf-8') as out:
        out.write(f"\n==== {path.name} ====\n")
        out.write(f"len={len(text)}\n")
        for kw in KEYS:
            idx = text.lower().find(kw.lower())
            if idx != -1:
                snippet = text[max(0, idx - 220): idx + 220]
                out.write(f"-- {kw} --\n{snippet}\n")
