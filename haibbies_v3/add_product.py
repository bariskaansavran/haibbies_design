import sys
import os
import json
import requests
import argparse
import urllib.parse
import re

def safe_slug(text):
    text = text.lower().replace(" ", "_")
    return re.sub(r'[^a-z0-9_]', '', text)

def download_image(url, save_path):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(r.content)
            return True
    except:
        pass
    return False

def main():
    parser = argparse.ArgumentParser(description="Add a new product to Haibbies V3 Catalog")
    parser.add_argument("--title", required=True, help="Product Title")
    parser.add_argument("--category", required=True, help="Category (e.g. Dekor, Oyuncak, Ev)")
    parser.add_argument("--desc", required=True, help="Description for Dolap")
    parser.add_argument("--price", required=True, help="Suggested Dolap Price in TL")
    parser.add_argument("--competition", required=True, help="Competition level (e.g. Düşük, Orta, Yüksek)")
    parser.add_argument("--pros", required=True, help="Pros (semicolon separated)")
    parser.add_argument("--cons", required=True, help="Cons (semicolon separated)")
    parser.add_argument("--verdict", required=True, help="Manager Verdict")
    parser.add_argument("--source", required=True, help="Original Source URL")
    parser.add_argument("--img1", required=True, help="Image URL 1")
    parser.add_argument("--img2", required=True, help="Image URL 2")
    parser.add_argument("--img3", required=True, help="Image URL 3")
    parser.add_argument("--print_settings", required=True, help="Bambu Lab Print Settings text")
    
    args = parser.parse_args()
    
    slug = safe_slug(args.title)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prod_dir = os.path.join(base_dir, "products", slug)
    os.makedirs(prod_dir, exist_ok=True)
    
    # Download images
    downloaded_images = []
    for idx, img_url in enumerate([args.img1, args.img2, args.img3], 1):
        img_path = os.path.join(prod_dir, f"photo_{idx}.jpg")
        if img_url and img_url.startswith("http"):
            if download_image(img_url, img_path):
                downloaded_images.append(f"products/{slug}/photo_{idx}.jpg")
    
    # Write description, settings, and STL link
    with open(os.path.join(prod_dir, "aciklama.txt"), "w", encoding="utf-8") as f:
        f.write(args.desc)
        
    with open(os.path.join(prod_dir, "bambu_ayarlari.txt"), "w", encoding="utf-8") as f:
        f.write(args.print_settings)
        
    with open(os.path.join(prod_dir, "stl_link.txt"), "w", encoding="utf-8") as f:
        f.write(args.source)
        
    # Append to JSON
    json_path = os.path.join(base_dir, "catalog_data.json")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = []
        
    new_product = {
        "slug": slug,
        "title": args.title,
        "category": args.category,
        "description": args.desc,
        "suggested_price": args.price,
        "competition": args.competition,
        "pros": [p.strip() for p in args.pros.split(";") if p.strip()],
        "cons": [c.strip() for c in args.cons.split(";") if c.strip()],
        "manager_verdict": args.verdict,
        "source_url": args.source,
        "images": downloaded_images
    }
    
    data.append(new_product)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    # Rebuild HTML
    import build_catalog
    build_catalog.build_html()
    print(f"Başarıyla eklendi: {args.title}")

if __name__ == "__main__":
    main()
