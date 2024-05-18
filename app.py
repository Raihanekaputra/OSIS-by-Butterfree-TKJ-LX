import datetime
import hashlib
import jwt
import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request, Response, flash, redirect, url_for, send_from_directory, make_response
from werkzeug.utils import secure_filename
# from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient("mongodb://test:test@ac-oowgeoe-shard-00-00.twt800w.mongodb.net:27017,ac-oowgeoe-shard-00-01.twt800w.mongodb.net:27017,ac-oowgeoe-shard-00-02.twt800w.mongodb.net:27017/?ssl=true&replicaSet=atlas-5kccjl-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0")
db = client.dbosis

app = Flask(__name__)
UPLOAD_FOLDER = 'static/images/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    galery_list = list(db.galery.find())
    return render_template('Beranda.html', galery = galery_list)

@app.route('/beranda')
def beranda():
    galery_list = list(db.galery.find())
    return render_template('Beranda.html', galery = galery_list)

@app.route('/galery')
def galery():
    galery_list = list(db.galery.find())
    return render_template('Galery.html', galery = galery_list)

@app.route('/profile')
def profile():
    galery_list = list(db.galery.find())
    return render_template('Profile.html', galery = galery_list)

@app.route('/osis')
def osis():
    galery_list = list(db.galery.find())
    return render_template('Tentang-osis.html', galery = galery_list)

@app.route('/smk')
def smk():
    galery_list = list(db.galery.find())
    return render_template('Tentang-sekolah.html', galery = galery_list)


@app.route('/login')
def login():
    login_list = list(db.galery.find())
    return render_template('login.html', login = login_list)

@app.route('/admin')
def admin():
    galery_list = list(db.galery.find())
    return render_template('admin.html', galery = galery_list)


@app.route("/galery", methods=["POST"])
def galery_post():
    description = request.form.get('description')
    image_file = request.files.get('image')
    
    gambar = None
    if image_file:
        filename = secure_filename(image_file.filename)
        gambar = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(gambar)
    
    try:
        doc = {
            'image': gambar,
            'description': description,
        }
        db.galery.insert_one(doc)
        return jsonify({'msg': 'Data berhasil ditambahkan'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/galery", methods=["GET"])
def galery_get():
    galery_list = list(db.galery.find({}, {'_id': 0}))
    return jsonify({'galery': galery_list})


@app.route("/galery/delete/<string:id>", methods=["POST", "GET"])
def galery_delete(id):
    try:
        object_id = ObjectId(id)
        doc = db.galery.find_one({"_id": object_id})
        if not doc:
            return f"No document found with ID: {id}", 404
        db.galery.delete_one({"_id": object_id})
        return redirect(url_for('admin'))
    except Exception as e:
        return f"Error deleting document: {e}", 500
    

    
# ...
@app.route("/galery/update/<string:id>", methods=['POST', 'GET'])
def galery_update(id):
    try:
        object_id = ObjectId(id)
        doc = db.galery.find_one({"_id": object_id})
        if not doc:
            return jsonify({"error": "No document found with ID: {}".format(id)}), 404
        description = request.form.get("description")

        image_file = request.files.get('imagemodal')
        print("SALMAN", image_file)
        if image_file:
            filename = secure_filename(image_file.filename)
            gambar = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(gambar)
        else:
            gambar = doc["image"]

        db.galery.update_one({"_id": object_id}, {"$set": {"image": gambar, "description": description}})
        return redirect(url_for('admin'))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
