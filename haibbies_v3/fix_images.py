import urllib.request
import re
import urllib.parse
import os
import json

def fetch_image_for_product(slug, query):
    url = "https://images.search.yahoo.com/search/images?p=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        images = re.findall(r'imgurl=(http[^&]+)', html)
        if images:
            img_url = urllib.parse.unquote(images[0])
            folder = os.path.join("products", slug)
            os.makedirs(folder, exist_ok=True)
            img_path = os.path.join(folder, "photo_1.jpg")
            
            # Download image
            img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            with open(img_path, 'wb') as f:
                f.write(urllib.request.urlopen(img_req).read())
            
            # Update JSON
            with open("catalog_data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for item in data:
                if item["slug"] == slug:
                    item["images"] = [f"products/{slug}/photo_1.jpg"]
                    break
            
            with open("catalog_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
            print(f"Successfully updated image for {slug}")
            return True
    except Exception as e:
        print(f"Failed to fetch image for {slug}: {e}")
    return False

if __name__ == "__main__":
    fetch_image_for_product("gizli_bisiklet_airtag_tutucu_reflektr_grnml", "airtag bike reflector 3d printed")
    fetch_image_for_product("apple_3_1_arada_magsafe_arj_istasyonu_vakum_tabanl", "3d printed magsafe charging station")
