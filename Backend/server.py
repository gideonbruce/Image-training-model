import os
import cv2
import pymysql
import hashlib
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)

# Configure MySQL connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="@Gideon",
    database="weed_detection"
)
cursor = db.cursor()

UPLOAD_FOLDER = "static/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Hash password for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Register User
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name, email, password = data["name"], data["email"], hash_password(data["password"])

    try:
        sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, email, password))
        db.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except pymysql.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400

# Login User
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email, password = data["email"], hash_password(data["password"])

    cursor.execute("SELECT id FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()

    if user:
        return jsonify({"message": "Login successful", "user_id": user[0]}), 200
    return jsonify({"error": "Invalid credentials"}), 401

# Upload Image and Associate with User
@app.route("/upload", methods=["POST"])
def upload_image():
    if "image" not in request.files or "user_id" not in request.form:
        return jsonify({"error": "Image and user_id required"}), 400

    image = request.files["image"]
    user_id = request.form["user_id"]
    filename = secure_filename(image.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    
    # Save the image
    image.save(filepath)

    # Save file path and user_id to MySQL
    sql = "INSERT INTO detections (image_path, user_id) VALUES (%s, %s)"
    cursor.execute(sql, (filepath, user_id))
    db.commit()

    return jsonify({"message": "Image uploaded successfully", "file_path": filepath, "user_id": user_id})

# Get All Detections for a User
@app.route("/get_user_detections/<int:user_id>", methods=["GET"])
def get_user_detections(user_id):
    cursor.execute("SELECT * FROM detections WHERE user_id = %s", (user_id,))
    results = cursor.fetchall()
    
    images = [{"id": row[0], "image_path": row[1], "detection_time": row[2], "user_id": row[3]} for row in results]
    return jsonify(images)

if __name__ == "__main__":
    app.run(debug=True)
