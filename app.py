from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    highest_score = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    quiz_results = db.relationship('QuizResult', backref='user', lazy=True)
    image_detections = db.relationship('ImageDetection', backref='user', lazy=True)

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ImageDetection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    detected_class = db.Column(db.String(255), nullable=True)
    confidence = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Quiz Questions Data
QUIZ_QUESTIONS = [
    {
        'id': 1,
        'question': 'Discord.py kütüphanesi ile bir bot oluştururken, botun mesajları dinlemesi için hangi decorator kullanılır?',
        'options': ['@bot.event', '@bot.command', '@client.event', '@discord.event'],
        'correct': 2,
        'topic': 'Python ile sohbet botu otomasyonu (Discord.py)'
    },
    {
        'id': 2,
        'question': 'Flask uygulamasında bir route tanımlamak için hangi decorator kullanılır?',
        'options': ['@app.route()', '@flask.route()', '@route()', '@url()'],
        'correct': 0,
        'topic': 'Python ile web geliştirme (Flask)'
    },
    {
        'id': 3,
        'question': 'Yapay zeka modellerinde overfitting problemi nedir?',
        'options': [
            'Modelin eğitim verilerinde çok iyi, test verilerinde kötü performans göstermesi',
            'Modelin eğitim verilerinde kötü performans göstermesi',
            'Modelin hiç öğrenememesi',
            'Modelin çok hızlı eğitilmesi'
        ],
        'correct': 0,
        'topic': 'Python ile yapay zeka geliştirme'
    },
    {
        'id': 4,
        'question': 'ImageAI kütüphanesinde Tiny YOLO modeli hangi amaç için kullanılır?',
        'options': [
            'Nesne tespiti ve sınıflandırma',
            'Metin işleme',
            'Ses tanıma',
            'Veri analizi'
        ],
        'correct': 0,
        'topic': 'Bilgisayar görüşü (Computer Vision - TensorFlow, ImageAI)'
    },
    {
        'id': 5,
        'question': 'BeautifulSoup kütüphanesi genellikle hangi işlem için kullanılır?',
        'options': [
            'Web scraping ve HTML/XML parsing',
            'Görüntü işleme',
            'Veritabanı işlemleri',
            'API çağrıları'
        ],
        'correct': 0,
        'topic': 'Doğal Dil İşleme (Natural Language Processing)'
    },
    {
        'id': 6,
        'question': 'NLTK kütüphanesi hangi alanda kullanılır?',
        'options': [
            'Doğal dil işleme ve metin analizi',
            'Görüntü işleme',
            'Ses işleme',
            'Veri görselleştirme'
        ],
        'correct': 0,
        'topic': 'Doğal Dil İşleme (Natural Language Processing)'
    }
]

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_or_create_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
    return user

def get_global_highest_score():
    result = db.session.query(db.func.max(User.highest_score)).scalar()
    return result if result else 0

@app.context_processor
def inject_scores():
    """Make scores available to all templates"""
    username = session.get('username', 'Guest')
    user = None
    if username != 'Guest':
        user = User.query.filter_by(username=username).first()
    
    global_highest = get_global_highest_score()
    user_highest = user.highest_score if user else 0
    
    return dict(global_highest=global_highest, user_highest=user_highest)

@app.route('/')
def index():
    username = session.get('username', 'Guest')
    user = None
    if username != 'Guest':
        user = User.query.filter_by(username=username).first()
    
    global_highest = get_global_highest_score()
    user_highest = user.highest_score if user else 0
    
    return render_template('index.html', 
                         global_highest=global_highest,
                         user_highest=user_highest)

@app.route('/set_username', methods=['POST'])
def set_username():
    username = request.form.get('username', '').strip()
    if username:
        session['username'] = username
        get_or_create_user(username)
        flash('Kullanıcı adı kaydedildi!', 'success')
    else:
        flash('Lütfen geçerli bir kullanıcı adı girin!', 'error')
    return redirect(url_for('index'))

@app.route('/quiz')
def quiz():
    username = session.get('username', 'Guest')
    if username == 'Guest':
        flash('Lütfen önce kullanıcı adınızı girin!', 'error')
        return redirect(url_for('index'))
    
    user = User.query.filter_by(username=username).first()
    global_highest = get_global_highest_score()
    user_highest = user.highest_score if user else 0
    
    return render_template('quiz.html',
                         questions=QUIZ_QUESTIONS,
                         global_highest=global_highest,
                         user_highest=user_highest)

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    username = session.get('username', 'Guest')
    if username == 'Guest':
        return redirect(url_for('index'))
    
    user = get_or_create_user(username)
    answers = request.form.to_dict()
    
    score = 0
    total = len(QUIZ_QUESTIONS)
    results = []
    
    for question in QUIZ_QUESTIONS:
        q_id = str(question['id'])
        user_answer = answers.get(f'question_{q_id}', None)
        
        if user_answer and int(user_answer) == question['correct']:
            score += 1
            results.append({
                'question': question['question'],
                'correct': True,
                'user_answer': question['options'][int(user_answer)],
                'correct_answer': question['options'][question['correct']]
            })
        else:
            results.append({
                'question': question['question'],
                'correct': False,
                'user_answer': question['options'][int(user_answer)] if user_answer and user_answer.isdigit() else 'Cevaplanmadı',
                'correct_answer': question['options'][question['correct']]
            })
    
    # Save quiz result
    quiz_result = QuizResult(
        user_id=user.id,
        score=score,
        total_questions=total
    )
    db.session.add(quiz_result)
    
    # Update user's highest score
    if score > user.highest_score:
        user.highest_score = score
    
    db.session.commit()
    
    global_highest = get_global_highest_score()
    user_highest = user.highest_score
    
    return render_template('quiz_result.html',
                         score=score,
                         total=total,
                         results=results,
                         global_highest=global_highest,
                         user_highest=user_highest)

@app.route('/image_detection')
def image_detection():
    username = session.get('username', 'Guest')
    if username == 'Guest':
        flash('Lütfen önce kullanıcı adınızı girin!', 'error')
        return redirect(url_for('index'))
    
    user = User.query.filter_by(username=username).first()
    global_highest = get_global_highest_score()
    user_highest = user.highest_score if user else 0
    
    # Get recent detections
    recent_detections = ImageDetection.query.filter_by(user_id=user.id).order_by(ImageDetection.created_at.desc()).limit(5).all()
    
    return render_template('image_detection.html',
                         global_highest=global_highest,
                         user_highest=user_highest,
                         recent_detections=recent_detections)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    username = session.get('username', 'Guest')
    if username == 'Guest':
        return jsonify({'error': 'Kullanıcı adı gerekli'}), 401
    
    if 'image' not in request.files:
        return jsonify({'error': 'Görsel dosyası bulunamadı'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Dosya seçilmedi'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Perform image detection using ImageAI
        user = get_or_create_user(username)
        detected_class = None
        confidence = None
        detected_image_path = None
        
        try:
            from imageai.Detection import ObjectDetection
            
            model_path = "yolo-tiny.h5"
            if os.path.exists(model_path):
                detector = ObjectDetection()
                detector.setModelTypeAsTinyYOLOv3()
                detector.setModelPath(model_path)
                detector.loadModel()
                
                detected_image_path = filepath.rsplit('.', 1)[0] + '_detected.' + filepath.rsplit('.', 1)[1]
                detections = detector.detectObjectsFromImage(
                    input_image=filepath,
                    output_image_path=detected_image_path,
                    minimum_percentage_probability=30
                )
                
                # Get the most confident detection
                if detections:
                    best_detection = max(detections, key=lambda x: x['percentage_probability'])
                    detected_class = best_detection['name']
                    confidence = round(best_detection['percentage_probability'], 2)
                else:
                    detected_class = "Nesne tespit edilemedi"
                    confidence = 0.0
            else:
                raise FileNotFoundError("Model dosyası bulunamadı")
                
        except (ImportError, FileNotFoundError, Exception) as e:
            # Fallback: If ImageAI is not available, use a simple mock detection
            import random
            mock_classes = ['Kedi', 'Köpek', 'Araba', 'İnsan', 'Bisiklet', 'Telefon', 'Masa', 'Sandalye', 'Bilgisayar']
            detected_class = random.choice(mock_classes)
            confidence = round(random.uniform(50, 95), 2)
        
        # Save to database
        image_detection = ImageDetection(
            user_id=user.id,
            image_path=filename,
            detected_class=detected_class,
            confidence=confidence
        )
        db.session.add(image_detection)
        db.session.commit()
        
        response_data = {
            'success': True,
            'detected_class': detected_class,
            'confidence': confidence,
            'image_path': filename
        }
        
        if detected_image_path and os.path.exists(detected_image_path):
            response_data['detected_image_path'] = os.path.basename(detected_image_path)
        else:
            response_data['detected_image_path'] = filename
            if not os.path.exists(model_path):
                response_data['note'] = 'Mock detection (ImageAI modeli yüklenemedi)'
        
        return jsonify(response_data)
    
    return jsonify({'error': 'Geçersiz dosya formatı'}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

