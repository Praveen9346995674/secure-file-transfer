from flask import Flask, render_template, request, redirect, session, send_file, flash
from models import db, User, File
import config
import bcrypt
from utils import encrypt_file, decrypt_file, upload_to_s3, download_from_s3
import io

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

with app.app_context():
    db.create_all()

# LOGIN
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("❌ Email not registered", "error")
            return redirect('/')

        if not bcrypt.checkpw(password.encode(), user.password):
            flash("❌ Incorrect password", "error")
            return redirect('/')

        session['user_id'] = user.id
        flash("✅ Login successful!", "success")
        return redirect('/dashboard')

    return render_template('login.html')


# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            flash("⚠️ Email already exists!", "error")
            return redirect('/register')

        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        user = User(username=username, email=email, password=hashed)
        db.session.add(user)
        db.session.commit()

        flash("✅ Registration successful! Please login.", "success")
        return redirect('/')

    return render_template('register.html')


# DASHBOARD
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    files = File.query.filter_by(user_id=session['user_id']).all()
    return render_template('dashboard.html', files=files)


# UPLOAD
@app.route('/upload', methods=['POST'])
def upload():
    if 'user_id' not in session:
        return redirect('/')

    file = request.files['file']
    data = file.read()

    encrypted = encrypt_file(data)
    upload_to_s3(encrypted, file.filename)

    new_file = File(user_id=session['user_id'], filename=file.filename)
    db.session.add(new_file)
    db.session.commit()

    flash("📂 File uploaded successfully!", "success")
    return redirect('/dashboard')


# DOWNLOAD
@app.route('/download/<int:file_id>')
def download(file_id):
    if 'user_id' not in session:
        return redirect('/')

    file = File.query.get(file_id)

    encrypted_data = download_from_s3(file.filename)
    decrypted_data = decrypt_file(encrypted_data)

    return send_file(
        io.BytesIO(decrypted_data),
        download_name=file.filename,
        as_attachment=True
    )


# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    flash("👋 Logged out successfully", "success")
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)