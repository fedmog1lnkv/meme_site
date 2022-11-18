from flask import Flask
from . import sql

app = Flask(__name__)

from .views import *
from .configs import *