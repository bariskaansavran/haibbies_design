import json

file_path = r'c:\Users\baris.savran\Desktop\STL\haibbies_v3\catalog_data.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    if 'ku_yemlii' in item['slug'] or 'vantuz' in item['title'].lower() or 'kedi televizyonu' in item['title'].lower():
        verdict = item.get('manager_verdict', '').replace("FOTOĞRAFLAR BOZUK, BU ÜRÜN SİLİNMELİ.", "").strip()
        if "Tahmini Filament" in verdict:
            verdict = verdict.split("Tahmini Filament")[0]
        item['manager_verdict'] = verdict.strip() + " Üretimi harika bir fikir. Tahmini Filament: ~150g. Ekstra Donanım: Vantuz (Cama yapıştırmak için)."
    
    elif 'matkap_bataryas' in item['slug'] or 'ak' in item['title'].lower() and 'aparat' in item['title'].lower():
        verdict = item.get('manager_verdict', '').replace("FOTOĞRAFLAR BOZUK, BU ÜRÜN SİLİNMELİ.", "").strip()
        if "Tahmini Filament" in verdict:
            verdict = verdict.split("Tahmini Filament")[0]
        item['manager_verdict'] = verdict.strip() + " Çok kârlı fonksiyonel bir ürün. Tahmini Filament: ~105g. Ekstra Donanım: Dübel ve Vida Seti."

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    
print("Updated verdicts with exact weights.")
