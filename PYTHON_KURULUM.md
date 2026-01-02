# Python Kurulum Rehberi

## Python Kurulu Değilse

### Adım 1: Python'u İndirin
1. https://www.python.org/downloads/ adresine gidin
2. "Download Python" butonuna tıklayın (en son versiyon)
3. İndirilen `.exe` dosyasını çalıştırın

### Adım 2: Kurulum Sırasında ÖNEMLİ!
**"Add Python to PATH" seçeneğini MUTLAKA işaretleyin!**

Kurulum ekranında:
- ✅ "Add Python to PATH" kutusunu işaretleyin
- "Install Now" seçeneğini seçin

### Adım 3: Kurulumu Doğrulayın
Yeni bir PowerShell penceresi açın ve şunu çalıştırın:

```powershell
python --version
```

veya

```powershell
py --version
```

## Python Kurulu Ama PATH'te Değilse

Eğer Python kurulu ama komut çalışmıyorsa:

### Yöntem 1: Tam Yol ile Kullanın
Python'un kurulu olduğu yolu bulun ve tam yol ile kullanın:

```powershell
# Örnek (yol sizin sisteminizde farklı olabilir):
C:\Users\Asilhan\AppData\Local\Programs\Python\Python311\python.exe -m pip install Flask Flask-SQLAlchemy Werkzeug Pillow numpy
```

### Yöntem 2: PATH'e Ekleyin
1. Windows tuşuna basın ve "environment variables" yazın
2. "Edit the system environment variables" seçin
3. "Environment Variables" butonuna tıklayın
4. "System variables" altında "Path" seçin ve "Edit" tıklayın
5. "New" tıklayın ve Python'un kurulu olduğu klasörü ekleyin (örnek: `C:\Users\Asilhan\AppData\Local\Programs\Python\Python311`)
6. "OK" tıklayın ve PowerShell'i yeniden başlatın

## Hızlı Test

Python kurulumundan sonra şu komutu çalıştırın:

```powershell
python -m pip install Flask Flask-SQLAlchemy Werkzeug Pillow numpy
```

## Alternatif: Anaconda/Miniconda Kullanıyorsanız

Eğer Anaconda kuruluysa:

```powershell
conda install flask flask-sqlalchemy werkzeug pillow numpy
```

## Sorun Devam Ederse

1. Python'un kurulu olduğundan emin olun
2. PowerShell'i **yönetici olarak** çalıştırın
3. Yeni bir PowerShell penceresi açın (PATH değişiklikleri için)

