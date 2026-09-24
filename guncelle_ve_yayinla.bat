@echo off
echo ===================================================
echo HAIBBIES DESIGN - KATALOG GUNCELLEME VE YAYINLAMA
echo ===================================================
echo.
echo Dosyalar GitHub'a (Buluta) yukleniyor...
git add .
git commit -m "Katalog Guncellemesi"
git push -u origin main
echo.
echo ===================================================
echo ISLEM TAMAMLANDI VEYA GUVENLIK EKRANI ACILACAK! 
echo Eger hata varsa yukaridaki mesaji kopyalayip Baris'a gonder.
echo ===================================================
pause
