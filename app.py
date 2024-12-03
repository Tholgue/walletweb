from flask import Flask, render_template, request, jsonify
import numbers
from datetime import datetime
import sqlite3

app = Flask(__name__)
DATABASE = 'compteur.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS compteur (id INTEGER PRIMARY KEY, montant REAL, last_update DATE)''')
        c.execute('''CREATE TABLE IF NOT EXISTS depenses (id INTEGER PRIMARY KEY, montant REAL, libelle TEXT, date DATE)''')
        c.execute('INSERT OR IGNORE INTO compteur (id, montant, last_update) VALUES (1, 0, ?)''', (datetime.now().date(),))
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/depenses', methods=['GET'])
def get_depenses():
    args = request.args
    limit = args.get('limit')
    
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        sql = 'SELECT * FROM depenses'
        if (limit is not None):
            sql += ' LIMIT ' + limit + ';'
        c.execute(sql)
        depenses = c.fetchall()
    return jsonify({"depenses": depenses})

@app.route('/api/compteur', methods=['GET'])
def get_compteur():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('SELECT montant FROM compteur WHERE id=1')
        montant = c.fetchone()[0]
    return jsonify({"compteur": montant})

@app.route('/api/ajouter_depense', methods=['POST'])
def ajouter_depense():
    data = request.json
    montant = data['montant']
    libelle = data.get('libelle', '')
    date = datetime.now().date()
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('INSERT INTO depenses (montant, libelle, date) VALUES (?, ?, ?)', (montant, libelle, date))
        c.execute('UPDATE compteur SET montant = montant - ? WHERE id=1', (montant,))
        conn.commit()
    return jsonify({"message": "Dépense ajoutée !"})

@app.route('/api/definir_montant', methods=['POST'])
def definir_montant():
    data = request.json
    montant = data['montant']
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('UPDATE compteur SET montant = ? WHERE id=1', (montant,))
        conn.commit()
    return jsonify({"message": "Montant défini"})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000) 