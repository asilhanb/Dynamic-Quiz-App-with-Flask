import os
from datetime import datetime
from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

# ------------------------------------------------------------------------------
# Uygulama ve veritabanı ayarları
# ------------------------------------------------------------------------------
class Config:
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR, 'exam.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'güçlü-bir-şifre'

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# ------------------------------------------------------------------------------
# Modeller
# ------------------------------------------------------------------------------
class User(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    name    = db.Column(db.String(64), nullable=False)
    results = db.relationship('Result', backref='user', lazy=True)

class Question(db.Model):
    id      = db.Column(db.Integer, primary_key=True)
    text    = db.Column(db.Text,    nullable=False)
    topic   = db.Column(db.String(32),  nullable=False)
    correct = db.Column(db.String(128), nullable=False)
    choices = db.Column(db.PickleType,  nullable=False)  # ['A','B','C','D'] :contentReference[oaicite:0]{index=0}&#8203;:contentReference[oaicite:1]{index=1}

class Result(db.Model):
    id        = db.Column(db.Integer,   primary_key=True)
    user_id   = db.Column(db.Integer,   db.ForeignKey('user.id'), nullable=False)
    score     = db.Column(db.Integer,   nullable=False)
    timestamp = db.Column(db.DateTime,  default=datetime.utcnow)

with app.app_context():
    db.create_all()

# ------------------------------------------------------------------------------
# Rotalar
# ------------------------------------------------------------------------------

# 1) Anasayfa: Soruları çek ve sınav formunu göster
@app.route('/', methods=['GET'])
def exam():
    questions = Question.query.all()
    return render_template('exam.html', questions=questions)

# 2) Cevapları işle: puanı hesapla, kaydet, sonuç sayfasına yönlendir
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    user = User.query.filter_by(name=username).first()
    if not user:
        user = User(name=username)
        db.session.add(user)
        db.session.commit()

    all_q = Question.query.all()
    total = len(all_q)
    correct_count = sum(
        1
        for q in all_q
        if request.form.get(f'question-{q.id}') == q.correct
    )
    score = int(correct_count * (100 / total))

    res = Result(user_id=user.id, score=score)
    db.session.add(res)
    db.session.commit()

    personal_best = db.session.query(func.max(Result.score))\
                       .filter(Result.user_id==user.id).scalar()
    global_best   = db.session.query(func.max(Result.score)).scalar()

    return render_template(
        'result.html',
        last_score=score,
        personal_best=personal_best,
        global_best=global_best
    )

# 3) Liderlik tablosu: her kullanıcının en yüksek skorunu sırala
@app.route('/leaderboard')
def leaderboard():
    records = db.session.query(
        User.name,
        func.max(Result.score).label('best_score')
    ).join(Result).group_by(User.id)\
     .order_by(func.max(Result.score).desc())\
     .all()
    return render_template('leaderboard.html', records=records)

# ------------------------------------------------------------------------------
# Sunucu başlatma
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
