# Kurulum Rehberi

## Hızlı Kurulum (Önerilen)

Uygulama ImageAI olmadan da çalışır. Sadece temel paketleri kurun:

```bash
pip install -r requirements.txt
```

veya

```bash
pip install Flask Flask-SQLAlchemy Werkzeug Pillow numpy
```

## Tam Kurulum (ImageAI ile)

Eğer gerçek görsel algılama istiyorsanız:

```bash
pip install -r requirements-full.txt
```

**DİKKAT:** TensorFlow çok büyük bir pakettir (1GB+) ve kurulumu uzun sürebilir.

## Kurulum Hataları

### "pip komutu bulunamadı" hatası

Windows'ta Python'u PATH'e eklemeniz gerekebilir. Alternatif olarak:

```bash
python -m pip install -r requirements.txt
```

veya

```bash
py -m pip install -r requirements.txt
```

### TensorFlow kurulum hatası

TensorFlow kurmakta sorun yaşıyorsanız, sadece minimal kurulum yapın:

```bash
pip install -r requirements-minimal.txt
```

Uygulama yine de çalışacaktır (mock detection kullanır).

### Versiyon uyumsuzlukları

Eğer belirli paket versiyonları sorun çıkarıyorsa, versiyonları kaldırın:

```bash
pip install Flask Flask-SQLAlchemy Werkzeug Pillow numpy
```

## Test

Kurulumdan sonra uygulamayı test edin:

```bash
python app.py
```

Tarayıcıda `http://localhost:5000` adresine gidin.

## ImageAI Model Dosyası

Eğer gerçek görsel algılama kullanmak istiyorsanız:

1. `yolo-tiny.h5` dosyasını indirin: https://github.com/OlafenwaMoses/ImageAI/releases
2. Dosyayı proje klasörüne koyun
3. `requirements-full.txt` ile paketleri kurun

Model dosyası yoksa uygulama otomatik olarak mock detection kullanır.



