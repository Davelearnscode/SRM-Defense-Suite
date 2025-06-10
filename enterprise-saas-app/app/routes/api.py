from flask import Blueprint, jsonify, request, abort
from flask_login import login_required, current_user
from app.services import ai_service
from app.models import Item
from app import db

api = Blueprint('api', __name__)

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@api.route('/userinfo')
@login_required
def userinfo():
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "role": current_user.role
    })

@api.route('/ai/predict', methods=['POST'])
def ai_predict():
    data = request.json
    text = data.get('text', '')
    prediction = ai_service.predict(text)
    return jsonify({"prediction": prediction})

@api.route('/ai/learn', methods=['POST'])
def ai_learn():
    data = request.json
    text = data.get('text', '')
    label = data.get('label', '')
    ai_service.learn(text, label)
    return jsonify({"status": "learned"})

@api.route('/items', methods=['GET', 'POST'])
@login_required
def items():
    if request.method == 'POST':
        name = request.json.get('name')
        item = Item(name=name)
        db.session.add(item)
        db.session.commit()
        return jsonify({'id': item.id, 'name': item.name}), 201
    items = Item.query.all()
    return jsonify([{'id': i.id, 'name': i.name} for i in items])

@api.route('/admin-only')
@admin_required
def admin_only():
    return "Admin content"