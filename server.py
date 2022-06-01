"""
---------------------------------------------
feito por Henrique (github.com/henriquelmeeee)
Projeto iniciado em 31 de maio de 2022
---------------------------------------------
"""

from flask import Flask, render_template, url_for, redirect, request, jsonify
from flaskext.mysql import MySQL
from datetime import datetime
import subprocess, os, random

template_dir = os.path.abspath('.')
static_dir = os.path.abspath('.')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

import mysql.connector
from mysql.connector import Error
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'pass'
app.config['MYSQL_DATABASE_DB'] = 'database'
app.config['MYSQL_DATABASE_HOST'] = 'host'
mysql.init_app(app)

# Checar SQL Injection em strings enviadas pelo usuário

def is_sqli(string):
    return False

# Gerar mensagem aleatória para o input da mensagem

def random_placeholder_generate():
    return str(random.choice(["Digite algo...", "Você pode digitar qualquer coisa.", "ChatBot está esperando por você.", "Como você está se sentindo?"]))

@app.route('/')
def home():
    return redirect(url_for('application'))

@app.route('/app/')
def application():
    return render_template('./static/index.html', placeholder=random_placeholder_generate())

## API

# response: resposta da API de uma determinada string.
# response/new: nova resposta da API de uma determinada string.

@app.route('/api/v1/response/', methods=["POST"])
def getresponse():
    content = request.json
    if content["message"] is None or content["message"] == '':
        return jsonify({"error": "The 'message' parameter must contain at least 1 character"})
    else:
        conn = mysql.connect(); cursor = conn.cursor()
        if not is_sqli(content["message"]):
            cursor.execute(f"SELECT response FROM messages WHERE message='{content['message']}'")
            response = str(cursor.fetchall())
            if response == '()':
                return jsonify({"error": "No response in the database found"})
            else:
                return jsonify({"response": f"{response}"})
        else:
            return jsonify({"error": "The 'message' parameter contains invalid characters"})


@app.route('/api/v1/response/new', methods=["POST"])
def newresponse():
    return ''

app.run(host='0.0.0.0', port=33, debug=True)
