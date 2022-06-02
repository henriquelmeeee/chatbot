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
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123'
app.config['MYSQL_DATABASE_DB'] = 'chatbot'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
    
conn = mysql.connect(); cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS messages (message text, response text)")

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

@app.route('/api/v1/response/', methods=["POST", "GET"])
def getresponse():
    if request.method == "GET":
        return jsonify({"error": "GET method is not allowed"}), 405
    else:
        content = request.json
        try:
            value = content["message"]
        except:
            return jsonify({"error": "The 'message' parameter was not specified"}), 400
        else:
            if content["message"] == '':
                return jsonify({"error": "The 'message' parameter must contain at least 1 character"}), 400
            else:
                conn = mysql.connect(); cursor = conn.cursor()
                if not is_sqli(content["message"]):
                    cursor.execute(f"SELECT response FROM messages WHERE message='{content['message']}'")
                    response = cursor.fetchall(); n = -1
                    for s in response:
                        try:
                            response[n]
                        except:
                            break
                        else:
                            n += 1
                    try:
                        response = response[random.randint(0, n)]
                    except:
                        return jsonify({"error": "No response in the database found"})
                    else:
                        response = str(response).replace('(', '').replace(')', '').replace('\'', '').replace(',', '')
                        return jsonify({"response": f"{response}"})
                else:
                    return jsonify({"error": "The 'message' parameter contains invalid characters"})


@app.route('/api/v1/response/new', methods=["POST"])
def newresponse():
    return ''

app.run(host='0.0.0.0', port=80)
