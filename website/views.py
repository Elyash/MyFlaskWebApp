import requests

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
        name = request.form.get('gift_name')
        link = request.form.get('gift_link')
        price = request.form.get('gift_price')
        notes = request.form.get('gift_notes')

        if len(name) < 2:
            flash(f'Invalid gift name. Should be longer then {len(name)} chars', category='error')
            return render_template("home.html", user=current_user)
        
        try:
            status = requests.get(link, timeout=2000).status_code
        except requests.exceptions.RequestException as e:
            flash(f'Invalid link. Details: {e.args}', category='error')
            return render_template("home.html", user=current_user)
        if status != 200:
            flash(f'Gift link is unreachable, status code: {status}', category='error')
            return render_template("home.html", user=current_user)
        
        if price is '':
            price = -1
        try:
            price = float(price)
        except ValueError as e:
            flash(f'Invalid price. Details: {e.args}', category='error')
            return render_template("home.html", user=current_user)

        new_gift = Gift(name=name, link=link, price=price, notes=notes, user_id=current_user.id)  #providing the schema for the gift 
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
