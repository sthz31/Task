from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)

# {
#         'reviewer':reviewer,
#         'rate':rate,
#         'review':review,
#         'date':date
#     }

class User(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    reviewer = db.Column(db.String(80), nullable=False)
    rate = db.Column(db.String(10), nullable=False)
    review = db.Column(db.String(1000))
    date = db.Column(db.String(120))