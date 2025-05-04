# populate_questions.py

from app import create_app
from models import db, Question

# 1) Uygulamayı başlat
app = create_app()

with app.app_context():
    # 2) Eğer tablo boşsa, soruları ekle
    if Question.query.count() == 0:
        questions = [
            Question(
                text="Hangi Discord.py olayı, botun bir mesaj aldığında tetiklenir?",
                topic="Discord.py",
                correct="B",
                choices=["on_ready()", "on_message()", "on_member_join()", "on_reaction_add()"]
            ),
            Question(
                text="Flask’te @app.route('/hello') dekoratörü hangi isteklere varsayılan olarak izin verir?",
                topic="Flask",
                correct="C",
                choices=["Sadece POST", "Sadece GET", "GET ve POST", "Hiçbiri"]
            ),
            Question(
                text="Denetimli öğrenme ile denetimsiz öğrenme arasındaki temel fark nedir?",
                topic="AI",
                correct="A",
                choices=[
                    "Denetimli öğrenmede etiketli veri, denetimsizde etiketlenmemiş veri kullanılır.",
                    "Denetimsiz öğrenmede insan gözetimi vardır.",
                    "Denetimli öğrenme sadece görsel veriyle çalışır.",
                    "Denetimsiz öğrenme sadece metin verisiyle sınırlıdır."
                ]
            ),
            Question(
                text="TensorFlow genellikle ne amaçla kullanılır?",
                topic="Computer Vision",
                correct="B",
                choices=[
                    "Web sayfası oluşturma",
                    "Derin öğrenme modelleri eğitme ve çalıştırma",
                    "Veritabanı yönetimi",
                    "Dosya sistemi erişimi"
                ]
            ),
            Question(
                text="BeautifulSoup Python’da en çok ne için kullanılır?",
                topic="NLP",
                correct="B",
                choices=[
                    "Makine öğrenmesi modelleri eğitmek",
                    "HTML ve XML belgelerini ayrıştırmak",
                    "Metin sınıflandırması yapmak",
                    "Ses tanıma işlemleri"
                ]
            ),
        ]
        db.session.add_all(questions)
        db.session.commit()
        print("✅ Sorular veritabanına eklendi.")
    else:
        print("ℹ️ Sorular zaten mevcut; ekleme atlandı.")
