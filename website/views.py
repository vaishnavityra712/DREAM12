from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("index.html", user=current_user)

@views.route('/selection', methods=['GET'])
@login_required
def selection():
    user = User.query.filter_by(email=current_user.id).first()
    return render_template("selection.html", user=current_user)    

@views.route('/contact', methods=['GET'])
@login_required
def contact():
    user = User.query.filter_by(email=current_user.id).first()
    return render_template("contact.html", user=current_user)    

@views.route('/matches', methods=['GET'])
@login_required
def matches():
    user = User.query.filter_by(email=current_user.id).first()
    return render_template("matches.html", user=current_user)    


# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})
