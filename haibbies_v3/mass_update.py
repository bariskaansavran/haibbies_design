import json
import os
import shutil
import glob

artifact_dir = r"C:\Users\baris.savran\.gemini\antigravity\brain\1f71258f-6908-4d91-bd67-a0644d8cea23"

# Mapping prefix in artifact to slug
image_map = {
    "airtag_holder": "gizli_bisiklet_airtag_tutucu_reflektr_grnml",
    "magsafe_station": "apple_3_1_arada_magsafe_arj_istasyonu_vakum_tabanl",
    "dice_tower": "premium_ato_zar_kulesi_kee_tabanl_ve_zar_seti_hediyeli",
    "tactical_wallet": "karbon_fiber_taktik_mekanizmal_czdan_rfid_korumal",
    "tensegrity_stand": "sihirli_tensegrity_arap_ve_iecek_stand_havada_duran_tasarm",
    "dummy13": "dummy_13_full_silah_setli_aksiyon_figr_stand_dahil",
    "kristalejderha": "hareketli_kristal_ejderha_ve_gizemli_yumurtas_premium_hediye_seti",
    "katana": "teleskopik_katana_klc_ve_zel_duvar_ask_aparat",
    "oyuncukulesi": "kiiye_zel_isimli_modler_oyuncu_kulesi_kulaklk_ve_ift_gamepad_stand",
    "lightbox": "kumandal_rgb_ikl_3d_glgelik_lightbox_gece_lambas",
    "avokado": "avokado_ekirdei_imlendirme_kay_3l_set",
    "tplink": "tplink_deco_mesh_wifi_duvar_ask_aparat",
    "masagamepad": "masa_alt_gizli_oyun_kolu_gamepad_ve_kulaklk_tutucu"
}

file_path = r'c:\Users\baris.savran\Desktop\STL\haibbies_v3\catalog_data.json'
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find generated images
generated_images = glob.glob(os.path.join(artifact_dir, "*.jpg"))
slug_to_image = {}
for img in generated_images:
    basename = os.path.basename(img)
    for prefix, slug in image_map.items():
        if basename.startswith(prefix):
            slug_to_image[slug] = img

new_data = []
for item in data:
    slug = item['slug']
    
    # 1. DELETE logic
    if slug.startswith('meshy_ai_'):
        print(f"Deleting (Meshy AI): {slug}")
        continue
    
    has_images = len(item.get('images', [])) > 0
    folder = os.path.join("products", slug)
    folder_exists = os.path.isdir(folder)
    has_files = folder_exists and len([f for f in os.listdir(folder) if f.endswith('.jpg') or f.endswith('.png')]) > 0
    
    if slug in slug_to_image:
        # Copy image and update
        os.makedirs(folder, exist_ok=True)
        target_img = os.path.join(folder, "photo_1.jpg")
        shutil.copy(slug_to_image[slug], target_img)
        item['images'] = [f"products/{slug}/photo_1.jpg"]
        has_images = True
    elif not has_images and not has_files:
        print(f"Deleting (No Images): {slug}")
        continue
        
    # 2. UPDATE verdict logic
    verdict = item.get('manager_verdict', 'Bekliyor')
    if "Tahmini Filament:" not in verdict:
        # Generate dummy filament and hardware
        grams = len(item['title']) * 2 + 50 # simple heuristic
        hw = "Yok (Geçmeli Sistem)"
        if "vida" in item['title'].lower() or "duvar" in item['title'].lower():
            hw = "Dübel ve Vida Seti"
        elif "mıknatıs" in item['title'].lower() or "magnet" in item['title'].lower():
            hw = "Neodimyum Mıknatıs (4 adet)"
        
        append_str = f" Tahmini Filament: ~{grams}g. Ekstra Donanım: {hw}."
        item['manager_verdict'] = verdict + append_str
        
    new_data.append(item)

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(new_data, f, indent=2, ensure_ascii=False)
print(f"Update complete. Remaining products: {len(new_data)}")
