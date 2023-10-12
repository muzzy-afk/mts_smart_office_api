from app import app, db, jwt, model
from app.models import User

from flask import jsonify
from flask import request

from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required

import face_recognition
from PIL import Image
import os
import pickle
from PIL import Image
import numpy as np
from typing import List
import onnxruntime as ort
from insightface.app import FaceAnalysis
import shutil


#TODO: сделать апи для регистрации

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username).one_or_none()
    if not user or not user.check_password(password):
        return jsonify("Wrong username or password"), 401

    # Notice that we are passing in the actual sqlalchemy user object here
    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)


@app.route("/who_am_i", methods=["GET"])
@jwt_required()
def protected():
    # We can now access our sqlalchemy User object via `current_user`.
    return jsonify(
        id=current_user.id,
        name=current_user.name,
        surname=current_user.surname,
    )

@app.route("/recognition", methods=["POST"])
def recognition():
    img = request.files['file']
    img.save(os.path.join('app/save', img.filename))
    predict = model.predict_face(os.path.join('app/save', img.filename))
    return jsonify(predict = predict)