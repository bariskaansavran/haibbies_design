import json
import os

file_path = r'c:\Users\baris.savran\Desktop\STL\haibbies_v3\catalog_data.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

new_data = []
for item in data:
    slug = item['slug']
    images = item.get('images', [])
    
    # Check if images actually exist
    valid_images = []
    for img in images:
        if os.path.isfile(img):
            valid_images.append(img)
            
    if not valid_images:
        print(f"Deleting {slug} because no valid images found/generated.")
        continue
        
    item['images'] = valid_images
    
    verdict = item.get('manager_verdict', 'Bekliyor')
    if "Tahmini Filament:" not in verdict:
        # Estimate
        grams = len(item['title']) * 2 + 30
        hw = "Yok (Geçmeli Sistem)"
        if "vida" in item['title'].lower() or "duvar" in item['title'].lower() or "montaj" in item['title'].lower():
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

    new_data.append(item)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)
    
print(f"Final cleanup complete. Remaining: {len(new_data)} products.")
