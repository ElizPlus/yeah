from flask import Blueprint, render_template, request, session, current_app, jsonify, redirect
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from db import db
from db.models import users, articles
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, current_user, logout_user


lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/')
def lab():
    return render_template('/lab9/index.html', login=session.get('login'))