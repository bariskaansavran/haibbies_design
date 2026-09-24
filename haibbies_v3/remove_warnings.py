import json

file_path = r'c:\Users\baris.savran\Desktop\STL\haibbies_v3\catalog_data.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    verdict = item.get('manager_verdict', '')
    if "FOTOĞRAFLAR BOZUK, BU ÜRÜN SİLİNMELİ." in verdict:
        item['manager_verdict'] = verdict.replace("FOTOĞRAFLAR BOZUK, BU ÜRÜN SİLİNMELİ.", "").strip()

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    
print(f"Warning removed from all products.")
