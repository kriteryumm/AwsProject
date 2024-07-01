from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename
import cv2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = '*****'
app.config['SECRET_KEY'] = '****'
app.config['UPLOAD_FOLDER'] = '*****'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    feedback = db.Column(db.Text, nullable=False)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    feedback_id = db.Column(db.Integer, db.ForeignKey('feedback.id'), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    username = db.Column(db.String(50), nullable=False)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'user'
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = Users(username=username, password_hash=hashed_password, role=role)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        except:
            flash('Username already exists.', 'danger')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            flash('Login successful!', 'success')
            session['user_id'] = user.user_id
            session['username'] = user.username
            session['role'] = user.role
            if user.role == 'user':
                return redirect(url_for('upload_qr'))
            elif user.role == 'admin':
                return redirect(url_for('admin'))
            elif user.role == 'staff':
                return redirect(url_for('staff'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')


@app.route('/upload_qr', methods=['GET', 'POST'])
def upload_qr():
    if request.method == 'POST':
        if 'qrcode' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['qrcode']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # QR code comparison logic
            decoded_qr_uploaded = decode_qrcode(filepath)
            decoded_qr_reference = decode_qrcode('qr_code.png')
            if decoded_qr_uploaded == decoded_qr_reference:
                session['qr_verified'] = True
                flash('QR code verified successfully!', 'success')
                return redirect(url_for('feedback'))
            else:
                flash('QR code did not match.', 'danger')
    return render_template('upload_qr.html')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if not session.get('qr_verified'):
        return redirect(url_for('upload_qr'))

    if request.method == 'POST':
        feedback_text = request.form['feedback']
        user_id = session['user_id']
        username = session['username']
        new_feedback = Feedback(user_id=user_id, username=username, feedback=feedback_text)
        db.session.add(new_feedback)
        db.session.commit()
        flash('Thank you for your feedback!', 'success')
        session.pop('qr_verified', None)
        session.pop('user_id', None)
        session.pop('username', None)
        session.pop('role', None)
        return render_template('thank_you.html')
    return render_template('feedback.html')


@app.route('/staff')
def staff():
    if session.get('role') != 'staff':
        return redirect(url_for('login'))

    feedback_list = Feedback.query.all()
    feedback_list_with_comments = [feedback for feedback in feedback_list if not Comment.query.filter_by(feedback_id=feedback.id).first()]
    return render_template('staff.html', feedback_list=feedback_list_with_comments)


@app.route('/add_comment/<int:feedback_id>', methods=['POST'])
def add_comment(feedback_id):
    comment_text = request.form['comment']
    user_id = session['user_id']
    username = session['username']
    new_comment = Comment(feedback_id=feedback_id, comment_text=comment_text, user_id=user_id, username=username)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('staff'))

@app.route('/admin')
def admin():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    feedback_list = Feedback.query.all()
    feedback_with_comments = []
    for feedback in feedback_list:
        comment = Comment.query.filter_by(feedback_id=feedback.id).first()
        if comment:
            feedback_with_comments.append({'username': feedback.username, 'feedback': feedback.feedback, 'comment_text': comment.comment_text})
        else:
            feedback_with_comments.append({'username': feedback.username, 'feedback': feedback.feedback, 'comment_text': ''})

    return render_template('admin.html', feedback_list=feedback_with_comments)


def decode_qrcode(image_path):
    img = cv2.imread(image_path)
    detector = cv2.QRCodeDetector()
    data, vertices_array, _ = detector.detectAndDecode(img)
    return data if vertices_array is not None else None

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
