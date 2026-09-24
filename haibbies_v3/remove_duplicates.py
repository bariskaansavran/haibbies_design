import json

file_path = r'c:\Users\baris.savran\Desktop\STL\haibbies_v3\catalog_data.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

seen_slugs = set()
new_data = []
duplicate_found = False

for item in data:
    slug = item['slug']
    if slug in seen_slugs:
        print(f"Removing duplicate: {slug}")
        duplicate_found = True
    else:
        seen_slugs.add(slug)
        new_data.append(item)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)
    
if duplicate_found:
    print("Duplicates removed.")
else:
    print("No duplicates found.")
