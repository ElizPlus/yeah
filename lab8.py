from flask import Blueprint, render_template, request, session, current_app, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path


lab8 = Blueprint('lab8', __name__)