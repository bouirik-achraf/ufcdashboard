from flask import Flask,request
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel
import requests
connect('mongodb://localhost:27017/ufcdatabase')

app = Flask(__name__)


@app.route("/savetodatabase",methods=['GET'])
def home():
    print(request.args)
    return ""


if __name__ == "__main__":
    app.run(debug=True,port=5001)