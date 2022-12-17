import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ca = certifi.where()

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI, tlsCAFile=ca)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/mars", methods=["POST"])
def web_mars_post():
    name_recieve = request.form['name_give']
    adress_receive = request.form['address_give']
    size_receive = request.form['size_give']
    doc = {
        'name': name_recieve,
        'address': adress_receive,
        'size': size_receive
    }
    db.orders.insert_one(doc)
    return jsonify({'msg': 'TERSIMPAN!'})

@app.route("/mars", methods=["GET"])
def web_mars_get():
    orders_list = list(db.orders.find({},{'_id': False}))
    return jsonify({'orders': orders_list})

# @app.route("/mars", methods=["GET"])
# def web_mars_get():
#     orders_list = list(db.orders.find({}, {'_id': False}))
#     return jsonify({'orders': orders_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)