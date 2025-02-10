import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 🔹 Load Supabase database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Please check your environment variables.")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# 🔹 Define Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    message = db.Column(db.Text, nullable=True)

# 🔹 Ensure database tables exist before handling requests
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    name, email, message = data.get("name"), data.get("email"), data.get("message")

    # 🔹 Validate form data
    if not name or not email or not message:
        return jsonify({"error": "All fields are required!"}), 400

    # 🔹 Insert data into the database
    new_entry = Contact(name=name, email=email, message=message)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify({"message": "Data saved successfully!"}), 201

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) 
    app.run(host="0.0.0.0", port=8000, debug=True)