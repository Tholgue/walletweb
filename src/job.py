import sqlite3

DATABASE = '/db/compteur.db'

print('jobrun')
with sqlite3.connect(DATABASE) as conn:
    print("Updated montant")
    c = conn.cursor()
    c.execute('SELECT montant FROM compteur WHERE id=1')
    montant = c.fetchone()[0]
    c.execute('UPDATE compteur SET montant = ? WHERE id=1', (montant+29,))
    conn.commit()