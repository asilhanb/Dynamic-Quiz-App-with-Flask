# Python Pro Quiz Uygulaması

Flask ve veritabanı kullanarak geliştirilmiş, gençlere yönelik dinamik bir sınav web sitesi.

## Özellikler

- **Sınav Sistemi**: Python'ın çeşitli kütüphaneleri hakkında en az 5 soru içeren sınav
- **Kullanıcı Yönetimi**: Kullanıcı adı ile giriş ve puan takibi
- **Puan Sistemi**: Son puan ve en yüksek puan gösterimi
- **Görsel Algılama**: ImageAI Tiny YOLO modeli ile nesne tespiti
- **Veritabanı**: SQLite veritabanı ile kullanıcı, sınav sonuçları ve görsel algılama kayıtları

## Kurulum

### Windows'ta Kurulum

Python'un tam yolunu kullanarak paketleri kurun:

```powershell
C:\Users\Asilhan\AppData\Local\Python\bin\python.exe -m pip install -r requirements.txt
```

veya hazır script'i kullanın:
```powershell
.\KUR.bat
```

### Alternatif: PATH'e Ekleme

Python'u PATH'e eklemek için:
1. Windows tuşuna basın ve "environment variables" yazın
2. "Path" değişkenine şunu ekleyin: `C:\Users\Asilhan\AppData\Local\Python\bin`
3. PowerShell'i yeniden başlatın

Sonra normal komutları kullanabilirsiniz:
```bash
python -m pip install -r requirements.txt
```

2. ImageAI model dosyasını indirin (opsiyonel):
   - Tiny YOLO modeli için `yolo-tiny.h5` dosyasını proje klasörüne ekleyin
   - Model dosyası yoksa, uygulama mock detection kullanacaktır

3. Uygulamayı çalıştırın:
```bash
python app.py
```

4. Tarayıcınızda `http://localhost:5000` adresine gidin

## PythonAnywhere Deployment

1. PythonAnywhere hesabınıza giriş yapın
2. Files sekmesinden proje dosyalarınızı yükleyin
3. Web sekmesinde yeni bir web app oluşturun
4. WSGI configuration dosyasını düzenleyin
5. Static files mapping ekleyin: `/static/` -> `/home/username/pro/static/`
6. Virtualenv'i ayarlayın ve requirements.txt'yi yükleyin

## Veritabanı

Uygulama ilk çalıştırıldığında otomatik olarak `quiz_app.db` SQLite veritabanı oluşturulur.

### Tablolar:
- **User**: Kullanıcı bilgileri ve en yüksek puanları
- **QuizResult**: Sınav sonuçları
- **ImageDetection**: Görsel algılama sonuçları

## Sınav Konuları

1. Python ile sohbet botu otomasyonu (Discord.py)
2. Python ile web geliştirme (Flask)
3. Python ile yapay zeka geliştirme
4. Bilgisayar görüşü (Computer Vision - TensorFlow, ImageAI)
5. Doğal Dil İşleme (Natural Language Processing - BeautifulSoup, NLTK)

## Notlar

- ImageAI modeli yüklenemezse, uygulama mock detection kullanır
- Tüm görseller `static/uploads/` klasörüne kaydedilir
- Kullanıcılar sınavı istediği kadar tekrar alabilir

