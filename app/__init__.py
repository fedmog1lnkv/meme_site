from flask import Flask
from . import sql

app = Flask(__name__)

from app import views