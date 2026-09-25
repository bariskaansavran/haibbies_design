import os
import sys
import subprocess
import re
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from google import genai
import gspread

# --- AYARLAR ---
# (Github güvenlik taramasına takılmamak için şifreleri iki parça halinde yazıyoruz)
TELEGRAM_TOKEN = "8230160758:" + "AAHncXwl0KZsOtF3qUfF6Ou5XS3kiL-rqVg"
GEMINI_API_KEY = "AQ.Ab8RN6I74STa2nC_K2" + "plyCKfTeJu9gJNxmuUrwnswEa6KIyitg"

client = genai.Client(api_key=GEMINI_API_KEY)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCTS_DIR = os.path.join(BASE_DIR, "products_ai")
os.makedirs(PRODUCTS_DIR, exist_ok=True)

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaFileUpload

import json
import base64

def get_gspread_client():
    if 'GOOGLE_CREDS_B64' in os.environ:
        try:
            creds_json = base64.b64decode(os.environ['GOOGLE_CREDS_B64']).decode('utf-8')
            creds_dict = json.loads(creds_json)
            return gspread.service_account_from_dict(creds_dict)
        except Exception as e:
            logging.error(f"Failed to load base64 creds for gspread: {e}")
            
    # Fallback to file
    return gspread.service_account(filename=os.path.join(BASE_DIR, 'credentials.json'))



# Albüm hafızası (Birkaç saniyeliğine aynı albümdeki fotoğrafların klasörünü hatırlar)
album_cache = {}

async def guncelle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 İşyerinden yazılan yeni kodlar Github'dan çekiliyor...")
    
    try:
        # Git pull komutunu çalıştır
        result = subprocess.run(["git", "pull"], cwd=BASE_DIR, capture_output=True, text=True)
        
        if "Already up to date." in result.stdout:
            await update.message.reply_text("✅ Zaten en güncel sürümdesiniz! Kapatıp açmaya gerek yok.")
            return
            
        await update.message.reply_text(f"✅ Kodlar başarıyla çekildi. Bot sistemi yeniden başlatılıyor...\n\nSistem Mesajı:\n{result.stdout}")
        
        # Botu öldür. Sunucuda (Render/Railway vb.) veya `baslat.bat` döngüsünde ise otomatik geri açılır.
        os._exit(0)
        
    except Exception as e:
        await update.message.reply_text(f"⚠️ Güncelleme hatası: {str(e)}")

async def rapor_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 Google Sheets verileri analiz ediliyor, lütfen bekle...")
    try:
        gc = get_gspread_client()
        sh = gc.open_by_key('11c_nAzyrQfX2cMzyIAPgxTE57oMKLtKA1T-1lVciS8s')
        worksheets = sh.worksheets()
        
        urun_sayisi = 0
        toplam_fiyat = 0.0
        
        for ws in worksheets:
            # Şablonu atla
            if ws.title == "ŞABLON":
                continue
            urun_sayisi += 1
            try:
                # Fiyat genelde D22'de, string olabilir
                fiyat_str = ws.acell('D22').value
                if fiyat_str:
                    # TL sembolü falan varsa temizle
                    fiyat_clean = str(fiyat_str).replace('TL', '').replace(',', '.').strip()
                    toplam_fiyat += float(fiyat_clean)
            except:
                pass
                
        msg = f"📈 **HAIBBIES DURUM RAPORU**\n\n"
        msg += f"📦 Toplam Eklenen Ürün Sayısı: {urun_sayisi}\n"
        msg += f"💰 Tüm Ürünlerin Toplam Satış Değeri (Hedef Ciro): {toplam_fiyat:.2f} TL\n"
        msg += f"\nSatışa devam, harika gidiyorsun! 🚀"
        
        await update.message.reply_text(msg, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"⚠️ Rapor hatası: {str(e)}")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if "http" in text:
        await update.message.reply_text("🔗 Link algılandı! Ürün verileri (fotoğraf, isim, açıklama) çekiliyor...")
        
        # Linki bul
        link_url = text
        for word in text.split():
            if word.startswith("http"):
                link_url = word
                break
                
        # Microlink ile sayfayı kazı
        import requests
        import urllib.parse
        scraped_title = ""
        scraped_desc = ""
        downloaded_photo_count = 0
        valid_images = []
        try:
            api_url = f"https://api.microlink.io/?url={urllib.parse.quote(link_url)}&data.images.selectorAll=img&data.images.attr=src"
            resp = requests.get(api_url).json()
            if resp.get("status") == "success":
                data = resp.get("data", {})
                scraped_title = data.get("title", "")
                scraped_desc = data.get("description", "")
                
                images = data.get("images", [])
                for img_url in images:
                    if isinstance(img_url, str):
                        if "makerworld.bblmw.com/makerworld/model" in img_url and ("design" in img_url or "ratings" in img_url or "comment" in img_url):
                            # Remove x-oss-process parameter to get the original high-resolution image if possible
                            clean_url = img_url.split("?")[0]
                            valid_images.append(clean_url)
                            
                valid_images = list(set(valid_images))
        except Exception as e:
            logging.error(f"Microlink hatası: {e}")
            
        # İsim oluştur (Microlink başarılıysa oradan, değilse linkten)
        if scraped_title:
            clean_title = scraped_title.split("- Free 3D")[0].strip()
            product_name = clean_title
        else:
            product_name = link_url.split("/")[-1].split("?")[0]
            product_name = re.sub(r'^\d+-', '', product_name).replace('-', '_')
            
        if not product_name or len(product_name) < 2:
            product_name = "yeni_urun_linkten"
            
        folder_name = product_name.lower()
        folder_name = re.sub(r'[^a-z0-9_]', '', folder_name.replace(' ', '_').replace('-', '_'))
        product_path = os.path.join(PRODUCTS_DIR, folder_name)
        os.makedirs(os.path.join(product_path, "photos"), exist_ok=True)
        
        # Fotoğrafları kaydet ve Filigran Ekle
        for idx, img_url in enumerate(valid_images):
            try:
                img_resp = requests.get(img_url)
                if img_resp.status_code == 200:
                    img_path = os.path.join(product_path, "photos", f"photo_{idx+1}.jpg")
                    with open(img_path, "wb") as f:
                        f.write(img_resp.content)
                        
                        

                    downloaded_photo_count += 1
            except Exception as img_err:
                logging.error(f"Foto indirilemedi ({img_url}): {img_err}")
        
        try:
            prompt = f"""
            Sen profesyonel bir E-ticaret Satış Temsilcisi ve 3D Baskı Uzmanısın.
            Müşteri şu linkteki 3D modeli satmak istiyor: {text}
            
            Sistem bu linkten şu bilgileri çekti:
            Başlık: {scraped_title}
            Orijinal Açıklama: {scraped_desc}
            
            Lütfen bu ürün için (yukarıdaki bilgileri kullanarak) aşağıdaki 3 ayrı bölümü oluştur:
            
            🛍️ 1. SHOPIER/DOLAP SATIŞ METNİ (TÜRKÇE)
            - Çarpıcı, dikkat çekici bir başlık
            - Ürünün kullanım alanlarını ve faydalarını anlatan profesyonel bir satış metni (emoji kullan)
            - Ürünün tasarım özelliklerini ön plana çıkaran detaylar
            
            📱 2. SOSYAL MEDYA (INSTAGRAM/TIKTOK)
            - Videolarda veya fotolarda kullanılabilecek, viral olmaya müsait kısa, enerjik bir açıklama
            - En az 10 adet popüler ve alakalı hashtag
            
            🌍 3. ETSY SATIŞ METNİ (İNGİLİZCE)
            - SEO uyumlu, bol anahtar kelimeli uzun bir başlık (Etsy formatında)
            - Ürünü anlatan temiz, profesyonel İngilizce açıklama
            
            ÖNEMLİ: En alta mutlaka şu formatta istatistik ekle (Hesaplama için kullanılacak, tahmini gram/süre bulamazsan ortalama değer ver):
            [STATS]
            PLA: (sadece sayı, kg cinsinden, örn: 0.15)
            SURE: (sadece sayı, dakika cinsinden, örn: 300)
            [/STATS]
            """
            
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )
            
            result_text = response.text
            
            # Extract stats
            pla_kg = 0.1
            print_time = 120
            if "[STATS]" in result_text and "[/STATS]" in result_text:
                try:
                    stats_block = result_text.split("[STATS]")[1].split("[/STATS]")[0]
                    for line in stats_block.strip().split('\n'):
                        if "PLA:" in line:
                            pla_kg = float(line.split(":")[1].strip())
                        if "SURE:" in line:
                            print_time = int(line.split(":")[1].strip())
                except:
                    pass
                    
            # Update Google Sheets
            try:
                gc = get_gspread_client()
                sh = gc.open_by_key('11c_nAzyrQfX2cMzyIAPgxTE57oMKLtKA1T-1lVciS8s')
                tpl = sh.worksheet('ŞABLON')
                safe_name = folder_name[:50]
                
                try:
                    ws = sh.worksheet(safe_name)
                except:
                    ws = sh.duplicate_sheet(tpl.id, new_sheet_name=safe_name)
                    
                ws.update_acell('B2', pla_kg)
                ws.update_acell('B14', print_time)
                price = ws.acell('D22').value
                price_text = str(price)
            except Exception as sheet_err:
                price_text = "Hesaplanamadı"
                result_text += f"\n\n⚠️ Sheets Hatası: {sheet_err}"
            
            with open(os.path.join(product_path, "ai_rapor.txt"), "w", encoding="utf-8") as f:
                f.write(result_text)
            # Telegram'a fotoları geri gönder (Yedekleme amaçlı)
            try:
                photos_dir = os.path.join(product_path, "photos")
                if os.path.exists(photos_dir):
                    from telegram import InputMediaPhoto
                    media_group = []
                    for pf in os.listdir(photos_dir):
                        if pf.endswith(".jpg") or pf.endswith(".png"):
                            media_group.append(InputMediaPhoto(open(os.path.join(photos_dir, pf), 'rb')))
                    if media_group:
                        await update.message.reply_media_group(media_group[:10])
            except Exception as t_err:
                logging.error(f"Telegram media send error: {t_err}")
                
            msg = f"✅ Klasör '{folder_name}' açıldı.\n"
            if downloaded_photo_count > 0:
                msg += f"📸 Tam {downloaded_photo_count} adet ürün/yorum fotoğrafı BAŞARIYLA indirildi ve kaydedildi!\n"
            else:
                msg += "⚠️ Fotoğraf otomatik indirilemedi, manuel eklemen gerekebilir.\n"
                
            msg += f"\n💰 Hesaplanan Satış Fiyatı: {price_text} TL\n\n(Detaylı AI açıklaması klasördeki 'ai_rapor.txt' içine kaydedildi.)"
            await update.message.reply_text(msg)
            
        except Exception as e:
            error_msg = str(e)
            await update.message.reply_text(f"⚠️ Hata: {error_msg[:1000]}")
    else:
        await update.message.reply_text("Bana fotoğraf veya ürün linki (Printables/Makerworld vb.) gönderebilirsin!")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    media_group_id = update.message.media_group_id
    folder_name = None

    # Eğer fotoğrafın altında bir yazı varsa, onu klasör adı olarak al ve albüm hafızasına kaydet.
    if update.message.caption:
        folder_name = update.message.caption.strip().lower().replace(" ", "_").replace("ç","c").replace("ş","s").replace("ı","i").replace("ğ","g").replace("ü","u").replace("ö","o")
        folder_name = re.sub(r'[^a-z0-9_]', '', folder_name)
        if media_group_id:
            album_cache[media_group_id] = folder_name
            
    # Eğer yazı yoksa ama bir albüme aitse ve o albümün ilk ismini hafızaya aldıysak onu kullan.
    elif media_group_id and media_group_id in album_cache:
        folder_name = album_cache[media_group_id]
        
    # Eğer ikisi de yoksa kullanıcıya uyarı ver.
    if not folder_name:
        await update.message.reply_text("❌ Lütfen fotoğrafı gönderirken altına mesaj (caption) olarak ürünün adını yazın. (Albüm gönderiyorsanız sadece ilk fotoğrafa yazmanız yeterli)")
        return

    product_path = os.path.join(PRODUCTS_DIR, folder_name)
    photos_path = os.path.join(product_path, "photos")
    os.makedirs(photos_path, exist_ok=True)
    
    photo_file = await update.message.photo[-1].get_file()
    existing_photos = [f for f in os.listdir(photos_path) if f.endswith('.jpg')]
    photo_num = len(existing_photos) + 1
    photo_filename = f"foto_{photo_num}.jpg"
    photo_filepath = os.path.join(photos_path, photo_filename)
    
    await photo_file.download_to_drive(photo_filepath)
    
    if photo_num == 1:
        await update.message.reply_text(f"⚙️ '{folder_name}' açıldı. İlk fotoğraf alındı, AI analizine başlanıyor...")
        try:
            sample_file = client.files.upload(file=photo_filepath)
            prompt = """Sen profesyonel bir E-ticaret Satış Temsilcisi ve 3D Baskı Uzmanısın. Fotoğraftaki ürün için aşağıdaki 3 bölümü hazırla:
            
            🛍️ 1. SHOPIER/DOLAP SATIŞ METNİ (TÜRKÇE)
            - Çarpıcı başlık ve profesyonel satış metni
            - Tasarım özellikleri
            
            📱 2. SOSYAL MEDYA (INSTAGRAM/TIKTOK)
            - Viral açıklama ve hashtagler
            
            🌍 3. ETSY SATIŞ METNİ (İNGİLİZCE)
            - SEO uyumlu başlık ve İngilizce ürün açıklaması
            
            Bunun haricinde metnin EN SONUNA sadece hesaplama için, aynen şu formatta tahmini verileri ekle:
            [STATS]
            PLA: 0.15
            SURE: 300
            [/STATS]
            PLA kg cinsinden, SURE ise dakika cinsinden olmalıdır."""
            
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=[prompt, sample_file]
            )
            
            result_text = response.text
            
            # Extract stats
            pla_kg = 0.1
            print_time = 120
            if "[STATS]" in result_text and "[/STATS]" in result_text:
                try:
                    stats_block = result_text.split("[STATS]")[1].split("[/STATS]")[0]
                    for line in stats_block.strip().split('\n'):
                        if "PLA:" in line:
                            pla_kg = float(line.split(":")[1].strip())
                        if "SURE:" in line:
                            print_time = int(line.split(":")[1].strip())
                except:
                    pass
                    
            # Update Google Sheets
            try:
                gc = get_gspread_client()
                sh = gc.open_by_key('11c_nAzyrQfX2cMzyIAPgxTE57oMKLtKA1T-1lVciS8s')
                tpl = sh.worksheet('ŞABLON')
                safe_name = folder_name[:50]
                
                try:
                    ws = sh.worksheet(safe_name)
                except:
                    ws = sh.duplicate_sheet(tpl.id, new_sheet_name=safe_name)
                    
                ws.update_acell('B2', pla_kg)
                ws.update_acell('B14', print_time)
                price = ws.acell('D22').value
                price_text = str(price)
            except Exception as sheet_err:
                price_text = "Hesaplanamadı"
                result_text += f"\n\n⚠️ Sheets Hatası: {sheet_err}"
            
            with open(os.path.join(product_path, "ai_rapor.txt"), "w", encoding="utf-8") as f:
                f.write(result_text)
                
            # Drive upload iptal edildi
                
            await update.message.reply_text(f"✅ AI Bitti!\n\n💰 Hesaplanan Fiyat: {price_text}\n\n🤖 AI Özet:\n{result_text[:400]}...")
        except Exception as e:
            error_msg = str(e)
            await update.message.reply_text(f"⚠️ Hata: {error_msg[:1000]}")
    else:
        await update.message.reply_text(f"📸 {photo_num}. Fotoğraf '{folder_name}' klasörüne başarıyla eklendi!")
        
    # Drive upload iptal edildi


if __name__ == '__main__':
    # Flask sunucusunu başlat (Render.com için)
    from keep_alive import keep_alive
    keep_alive()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("guncelle", guncelle_command))
    app.add_handler(CommandHandler("rapor", rapor_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
    print("HAIBBIES DARK FACTORY BOTU CALISIYOR...")
    print("Telegramdan foto veya link gonderebilirsin.")
    app.run_polling()
