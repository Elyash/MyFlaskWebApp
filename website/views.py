from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Gift
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        gift = request.form.get('gift')#Gets the gift from the HTML 

        if len(gift) < 1:
            flash('Gift is too short!', category='error') 
        else:
            new_gift = Gift(data=gift, user_id=current_user.id)  #providing the schema for the gift 
            db.session.add(new_gift) #adding the gift to the database 
            db.session.commit()
            flash('Gift added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-gift', methods=['POST'])
def delete_gift():  
    gift = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    giftId = gift['giftId']
    gift = Gift.query.get(giftId)
    if gift:
        if gift.user_id == current_user.id:
            db.session.delete(gift)
            db.session.commit()

    return jsonify({})
