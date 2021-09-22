from flask import Blueprint, render_template
from app import mysql

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')