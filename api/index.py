from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("postgresql://postgres:2178@localhost:5432/contact")
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

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
    data = request.json
    name, email, message = data.get('name'), data.get('email'), data.get('message')

    if not name or not email or not message:
        return jsonify({"error": "All fields are required!"}), 400

    new_entry = Contact(name=name, email=email, message=message)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({"message": "Data saved successfully!"}), 201

# Vercel requires this
from flask_lambda import FlaskLambda
app = FlaskLambda(app)