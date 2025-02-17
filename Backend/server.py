from flask import Flask, request, jsonify
import jwt
import datetime

app = Flask(__name__)
SECRET_KEY = "3dyr478y8fuy4n8y4ue"

