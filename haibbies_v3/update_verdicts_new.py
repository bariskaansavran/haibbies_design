import json

file_path = r'c:\Users\baris.savran\Desktop\STL\haibbies_v3\catalog_data.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    verdict = item.get('manager_verdict', '')
    if "Tahmini Filament:" not in verdict:
        grams = len(item['title']) * 2 + 50
        hw = "Yok (Geçmeli Sistem)"
        if "vida" in item['title'].lower() or "duvar" in item['title'].lower() or "raf" in item['title'].lower():
            hw = "Dübel ve Vida Seti"
        elif "mıknatıs" in item['title'].lower() or "magnet" in item['title'].lower():
            hw = "Mıknatıs (4 adet)"
        elif "rgb" in item['title'].lower() or "lamba" in item['title'].lower():
            hw = "RGB LED ve Kumanda"
            
        verdict = verdict.strip()
        if verdict:
            verdict += f" Tahmini Filament: ~{grams}g. Ekstra Donanım: {hw}."
        else:
            verdict = f"Üretilebilir. Tahmini Filament: ~{grams}g. Ekstra Donanım: {hw}."
        
        item['manager_verdict'] = verdict

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    
print("New verdicts updated.")
