import json

file_path = r'c:\Users\baris.savran\Desktop\STL\haibbies_v3\catalog_data.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    if 'Bekliyor' in item.get('manager_verdict', '') or 'Hemen' in item.get('manager_verdict', ''):
        print(f"SLUG: {item['slug']}")
        print(f"TITLE: {item['title']}")
        print(f"PRICE: {item.get('suggested_price')}")
        print(f"PROS: {item.get('pros')}")
        print(f"CONS: {item.get('cons')}")
        print("---")
