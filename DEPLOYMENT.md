# PythonAnywhere Deployment Rehberi

## Adım Adım Kurulum

### 1. Dosyaları Yükleme
1. PythonAnywhere hesabınıza giriş yapın
2. **Files** sekmesine gidin
3. Proje dosyalarınızı yükleyin:
   - `app.py`
   - `wsgi.py`
   - `requirements.txt`
   - `templates/` klasörü (tüm HTML dosyaları ile)
   - `static/` klasörü (CSS ve uploads klasörü ile)

### 2. Virtual Environment Oluşturma
1. **Consoles** sekmesine gidin
2. Yeni bir Bash console açın
3. Virtual environment oluşturun:
```bash
cd ~
python3.10 -m venv myenv
source myenv/bin/activate
cd pro  # veya proje klasörünüzün adı
pip install --user -r requirements.txt
```

### 3. Web App Oluşturma
1. **Web** sekmesine gidin
2. **Add a new web app** butonuna tıklayın
3. Domain seçin ve **Next** tıklayın
4. **Flask** seçin ve **Next** tıklayın
5. Python versiyonu seçin (3.10 önerilir)
6. **Next** tıklayın

### 4. WSGI Configuration
1. **Web** sekmesinde **WSGI configuration file** linkine tıklayın
2. Dosyayı şu şekilde düzenleyin:
```python
import sys
import os

path = '/home/YOURUSERNAME/pro'  # YOURUSERNAME'i değiştirin
if path not in sys.path:
    sys.path.insert(0, path)

from app import app as application
```

### 5. Static Files Mapping
1. **Web** sekmesinde **Static files** bölümüne gidin
2. Şu mapping'i ekleyin:
   - URL: `/static/`
   - Directory: `/home/YOURUSERNAME/pro/static/`

### 6. Veritabanı İlk Kurulum
1. **Consoles** sekmesinde Bash console açın
2. Virtual environment'ı aktifleştirin:
```bash
source ~/myenv/bin/activate
cd ~/pro
python
```
3. Python'da şu komutları çalıştırın:
```python
from app import app, db
with app.app_context():
    db.create_all()
    exit()
```

### 7. ImageAI Model (Opsiyonel)
1. Tiny YOLO modelini indirin: https://github.com/OlafenwaMoses/ImageAI/releases
2. `yolo-tiny.h5` dosyasını proje klasörüne yükleyin
3. Model yoksa uygulama mock detection kullanacaktır

### 8. Uygulamayı Başlatma
1. **Web** sekmesine gidin
2. **Reload** butonuna tıklayın
3. Web sitenizin URL'sine gidin

## Önemli Notlar

- **Secret Key**: Production'da `app.py` dosyasındaki `SECRET_KEY`'i değiştirin
- **Database Path**: SQLite veritabanı proje klasöründe oluşturulacaktır
- **Uploads Folder**: `static/uploads/` klasörü otomatik oluşturulur
- **Model Dosyası**: ImageAI modeli yoksa uygulama çalışmaya devam eder (mock detection)

## Sorun Giderme

### Import Hatası
- Virtual environment'ın doğru aktif olduğundan emin olun
- `pip install --user -r requirements.txt` komutunu tekrar çalıştırın

### Database Hatası
- Veritabanı dosyasının yazma izinlerini kontrol edin
- `db.create_all()` komutunu tekrar çalıştırın

### Static Files Yüklenmiyor
- Static files mapping'in doğru olduğundan emin olun
- URL ve Directory path'lerini kontrol edin

### ImageAI Çalışmıyor
- Model dosyasının (`yolo-tiny.h5`) proje klasöründe olduğundan emin olun
- Model yoksa uygulama mock detection kullanacaktır (normal)

