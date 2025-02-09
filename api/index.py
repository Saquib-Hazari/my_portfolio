from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Use environment variable for database URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:2178@localhost:5432/contact")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Create database engine with connection pooling
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300)
db = SQLAlchemy(app)
Session = scoped_session(sessionmaker(bind=engine))
session = Session()

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    message = db.Column(db.Text, nullable=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        name, email, message = data.get('name'), data.get('email'), data.get('message')

        if not name or not email or not message:
            return jsonify({"error": "All fields are required!"}), 400

        new_entry = Contact(name=name, email=email, message=message)
        session.add(new_entry)
        session.commit()

        return jsonify({"message": "Data saved successfully!"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

# Vercel does not require app.run()