import json
import os

def build_html():
    products = []
    if os.path.exists("catalog_data.json"):
        with open("catalog_data.json", "r", encoding="utf-8") as f:
            try:
                products = json.load(f)
            except:
                pass

    html = """<!DOCTYPE html>
<html lang="tr" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Haibbies Design | Ürün Değerlendirme Kataloğu</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: { sans: ['Inter', 'sans-serif'] },
                    colors: { brand: { 500: '#3b82f6', 600: '#2563eb' } }
                }
            }
        }
    </script>
    <style>
        body { background-color: #0f172a; color: #f8fafc; }
        .glass-card {
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
        }
        .img-carousel::-webkit-scrollbar { height: 6px; }
        .img-carousel::-webkit-scrollbar-thumb { background: #475569; border-radius: 10px; }
    </style>
</head>
<body class="min-h-screen p-6 md:p-12">
    <header class="mb-12 flex flex-col md:flex-row justify-between items-start md:items-center gap-6 border-b border-slate-800 pb-8">
        <div>
            <h1 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400 tracking-tight">Haibbies Design</h1>
            <p class="text-slate-400 mt-2 text-lg">Otonom Pazar Araştırması & Ürün Değerlendirme Merkezi</p>
        </div>
        <div class="flex gap-4">
            <div class="glass-card px-6 py-3 rounded-2xl text-center">
                <div class="text-xs text-slate-400 font-semibold uppercase tracking-wider">İncelenen Ürün</div>
                <div class="text-3xl font-black text-white">""" + str(len(products)) + """</div>
            </div>
        </div>
    </header>

    <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
"""

    for p in products:
        # Extract images safely
        images_html = ""
        for img in p.get("images", []):
            images_html += f'<img src="{img}" class="h-48 w-48 object-cover rounded-xl border border-slate-700 flex-shrink-0 snap-center">'
        
        pros_html = "".join([f'<li class="flex items-start gap-2"><i class="fa-solid fa-circle-check text-emerald-400 mt-1 text-sm"></i><span class="text-sm text-slate-300">{pro}</span></li>' for pro in p.get("pros", [])])
        cons_html = "".join([f'<li class="flex items-start gap-2"><i class="fa-solid fa-circle-xmark text-rose-400 mt-1 text-sm"></i><span class="text-sm text-slate-300">{con}</span></li>' for con in p.get("cons", [])])

        html += f"""
        <!-- Product Card -->
        <div class="glass-card rounded-3xl overflow-hidden flex flex-col transition-transform hover:-translate-y-1 hover:shadow-2xl hover:shadow-blue-900/20">
            <!-- Images Carousel -->
            <div class="p-4 bg-slate-900/50">
                <div class="flex overflow-x-auto gap-3 img-carousel snap-x snap-mandatory pb-2">
                    {images_html}
                </div>
            </div>
            
            <div class="p-6 flex-1 flex flex-col">
                <div class="flex justify-between items-start mb-4">
                    <div>
                        <span class="px-3 py-1 rounded-full text-xs font-bold bg-blue-500/20 text-blue-300 border border-blue-500/30 uppercase tracking-wider">{p.get("category", "Genel")}</span>
                        <h2 class="text-2xl font-bold mt-3 leading-tight">{p.get("title", "İsimsiz Ürün")}</h2>
                    </div>
                </div>

                <p class="text-slate-400 text-sm mb-6 leading-relaxed line-clamp-3">{p.get("description", "")}</p>

                <div class="grid grid-cols-2 gap-4 mb-6">
                    <div class="bg-slate-800/50 p-4 rounded-2xl border border-slate-700/50">
                        <div class="text-xs text-slate-400 font-semibold mb-1">Önerilen Satış</div>
                        <div class="text-xl font-bold text-emerald-400">{p.get("suggested_price", "0")} TL</div>
                    </div>
                    <div class="bg-slate-800/50 p-4 rounded-2xl border border-slate-700/50">
                        <div class="text-xs text-slate-400 font-semibold mb-1">Rekabet Seviyesi</div>
                        <div class="text-lg font-bold text-amber-400">{p.get("competition", "Bilinmiyor")}</div>
                    </div>
                </div>

                <!-- Pros & Cons -->
                <div class="space-y-4 mb-6 flex-1">
                    <div>
                        <h4 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Artı Yönleri (Avantajlar)</h4>
                        <ul class="space-y-1.5">{pros_html}</ul>
                    </div>
                    <div>
                        <h4 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Eksi Yönleri (Riskler)</h4>
                        <ul class="space-y-1.5">{cons_html}</ul>
                    </div>
                </div>

                <!-- Curator Verdict -->
                <div class="bg-blue-900/20 border border-blue-800/50 p-4 rounded-2xl mb-6">
                    <h4 class="text-xs font-bold text-blue-400 uppercase tracking-wider mb-1"><i class="fa-solid fa-gavel"></i> Üretim Müdürü Kararı</h4>
                    <p class="text-sm text-blue-100">{p.get("manager_verdict", "Henüz değerlendirilmedi.")}</p>
                </div>

                <!-- Footer Links -->
                <div class="flex items-center justify-between pt-4 border-t border-slate-800 mt-auto">
                    <a href="products/{p.get("slug", "")}/bambu_ayarlari.txt" target="_blank" class="text-xs font-medium text-slate-400 hover:text-white transition flex items-center gap-1"><i class="fa-solid fa-sliders"></i> Ayarlar</a>
                    <a href="products/{p.get("slug", "")}/aciklama.txt" target="_blank" class="text-xs font-medium text-slate-400 hover:text-white transition flex items-center gap-1"><i class="fa-solid fa-file-lines"></i> Metin</a>
                    <a href="{p.get("source_url", "#")}" target="_blank" class="text-xs font-bold text-white bg-blue-600 hover:bg-blue-500 transition flex items-center gap-1 px-3 py-1.5 rounded-lg shadow-lg"><i class="fa-solid fa-cube"></i> STL İNDİR (Kaynak)</a>
                    <button onclick="deleteProduct(this, '{p.get("slug", "")}')" class="text-xs font-bold text-rose-500 hover:text-rose-400 transition flex items-center gap-1 bg-rose-500/10 hover:bg-rose-500/20 px-2 py-1 rounded"><i class="fa-solid fa-trash"></i> Sil</button>
                </div>
            </div>
        </div>
        """

    html += """
    </div>
    
    <script>
        function deleteProduct(btn, slug) {
            // Visual delete
            const card = btn.closest('.glass-card');
            card.style.display = 'none';
            
            // Show alert with command
            const cmd = `python delete_product.py ${slug}`;
            navigator.clipboard.writeText(cmd);
            alert(`Kart gizlendi.\\n\\nKalıcı olarak silmek için terminalde şu komutu çalıştırın (Komut kopyalandı):\\n\\n${cmd}`);
        }
    </script>
</body>
</html>
"""
    with open("catalog.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("catalog.html başarıyla güncellendi.")

if __name__ == "__main__":
    build_html()
