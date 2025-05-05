@echo off
echo CyberSentry Kurulum Asistanı
echo ==========================
echo.

REM Python kurulumunu kontrol et
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python kurulu değil! Lütfen Python 3.6 veya üstünü yükleyin.
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b
)

echo Python kurulumu bulundu. Bağımlılıklar yükleniyor...
echo.

REM Gerekli paketleri yükle
pip install -r config/requirements.txt

if %errorlevel% neq 0 (
    echo Bağımlılıklar yüklenirken hata oluştu!
    pause
    exit /b
)

echo Bağımlılıklar başarıyla yüklendi.
echo.
echo CyberSentry kullanıma hazır! Başlatmak için start.bat dosyasını çalıştırabilirsiniz.
echo.
pause 