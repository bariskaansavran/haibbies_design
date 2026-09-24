import json

file_path = r'c:\Users\baris.savran\Desktop\STL\haibbies_v3\catalog_data.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    if item['slug'] == 'kiiye_zel_ifreli_cryptex_da_vinci_hediye_kutusu':
        item['manager_verdict'] = 'Muazzam bir kişiselleştirilebilir hediye ürünü. Siparişte harfleri tek tek dizme işini hızlandırmak için tüm harflerin STL dosyaları kategorize edilip hazır tutulmalı. İç mekanizmanın kırılmaması için PETG, dış kabuğun şık görünmesi için Silk PLA kullanılmasını öneririm. Kişiselleştirme algısı yüksek olduğundan satış fiyatı 249 TL yerine rahatlıkla 349-399 TL seviyesine çıkarılabilir.'
    elif item['slug'] == 'meshy_ai_kristal_maara_gece_lambas':
        item['manager_verdict'] = 'Mükemmel bir dekorasyon ürünü. Şeffaf (Translucent) PETG veya şeffaf PLA ile basılması görselliği doruğa çıkarır. Sadece boş baskıyı satmak yerine, içerisine maliyeti çok düşük olan pilli bir peri LED (fairy light) ekleyerek Tak-Çalıştır Gece Lambası konseptiyle satmalıyız. Böylece 300 TL olan fiyatı 400-450 TL aralığına çekerek daha fazla kâr edebiliriz.'

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
