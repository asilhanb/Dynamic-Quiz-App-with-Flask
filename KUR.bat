@echo off
REM Paketleri Kurma Scripti
echo Paketler kuruluyor...
echo.

REM Python'un tam yolunu kullan
C:\Users\Asilhan\AppData\Local\Python\bin\python.exe -m pip install Flask Flask-SQLAlchemy Werkzeug Pillow numpy

echo.
echo Kurulum tamamlandi!
pause


