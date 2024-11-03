from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# MongoDB bağlantısını oluştur
mongo_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongo_uri)
db = client["veri_tabanı"]
collection = db["veri_koleksiyonu"]

# Ana Sayfa - Listeleme
@app.route('/')
def index():
    data = collection.find()
    return render_template('index.html', data=data)

# Veri Ekleme
@app.route('/add', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        collection.insert_one({"name": name, "description": description})
        return redirect(url_for('index'))
    return render_template('add_data.html')

# Veri Güncelleme
@app.route('/update/<id>', methods=['GET', 'POST'])
def update_data(id):
    item = collection.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        collection.update_one({"_id": ObjectId(id)}, {"$set": {"name": name, "description": description}})
        return redirect(url_for('index'))
    return render_template('update_data.html', data=item)

# Veri Silme
@app.route('/delete/<id>', methods=['POST'])
def delete_data(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)