from flask import Blueprint, render_template, request, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab6 = Blueprint('lab6', __name__)

def db_connect():
    print(current_app.config['DB_TYPE'])
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'elizaveta_plyusnina_knowledge_base',
            user = 'elizaveta_plyusnina_knowledge_base',
            password = '0113'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab6.route('/lab6/')
def lab():
    return render_template('/lab6/lab6.html', login=session.get('login'))

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']

    conn, cur = db_connect()

    if data['method'] == 'info':
        cur.execute("SELECT * FROM offices")
        offices = cur.fetchall()
        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }

    elif data['method'] == 'booking':
        login = session.get('login')
        if not login:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            }

        office_number = data['params']
        cur.execute("SELECT * FROM offices WHERE number = %s", (office_number,))
        office = cur.fetchone()

        if office and office['tenant'] != '':
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 2,
                    'message': 'Already booked'
                },
                'id': id
            }

        if office:
            cur.execute("UPDATE offices SET tenant = %s WHERE number = %s", (login, office_number))
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'result': 'Office booked',
                'id': id
            }

    elif data['method'] == 'cancellation':
        login = session.get('login')
        if not login:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': id
            }

        office_number = data['params']
        cur.execute("SELECT * FROM offices WHERE number = %s", (office_number,))
        office = cur.fetchone()

        if office and office['tenant'] == '':
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Office not booked'
                },
                'id': id
            }

        if office and office['tenant'] != login:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 4,
                    'message': 'Cannot cancel someone else\'s booking'
                },
                'id': id
            }

        if office:
            cur.execute("UPDATE offices SET tenant = '' WHERE number = %s", (office_number,))
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'result': 'Office released',
                'id': id
            }

    db_close(conn, cur)
    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }