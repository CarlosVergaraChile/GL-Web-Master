#!/usr/bin/env python3
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    'Gastón L\'Huillier</h4>': 'Gastón L\'Huillier Troncoso</h4>',
    'Edith Wilson</h4>': 'Edith Wilson Porter</h4>',
    'Carlos Vergara</h4>': 'Carlos Vergara Veloz</h4>',
    'Pablo Canobra</h4>': 'Pablo Canobra Osses</h4>',
    'José Inostroza</h4>': 'José Inostroza Avaria</h4>',
}

count = 0
for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        count += 1
        print(f"✓ {old} → {new}")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ {count} apellidos completados")
