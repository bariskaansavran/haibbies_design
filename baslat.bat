@echo off
echo ===================================================
echo HAIBBIES DESIGN - OTO YENIDEN BASLATAN BOT SCRIPT'I
echo ===================================================
echo Bu script botu calistirir ve bot guncelleme 
echo alip kapandiginda onu otomatik olarak yeniden acar.
echo Botu durdurmak icin pencereyi kapatmaniz yeterlidir.
echo.

:loop
echo [%time%] Bot baslatiliyor...
python haibbies_bot.py
echo.
echo [%time%] Bot kapandi. 3 saniye icinde yeniden baslatilacak...
timeout /t 3 /nobreak >nul
goto loop
