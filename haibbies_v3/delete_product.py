import json
import os
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python delete_product.py <slug>")
        return
    
    slug_to_delete = sys.argv[1]
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "catalog_data.json")
    
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        return

    new_data = [p for p in data if p.get("slug") != slug_to_delete]
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
        
    print(f"Product '{slug_to_delete}' deleted.")
    
    import build_catalog
    build_catalog.build_html()

if __name__ == "__main__":
    main()
