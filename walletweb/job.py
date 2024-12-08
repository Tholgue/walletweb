import sqlite3
from schedule import every, repeat, run_pending
import time

DATABASE = 'compteur.db'

@repeat(every().day.at("00:00", "Europe/Paris"))
def job():
    print('jobrun')
    with sqlite3.connect(DATABASE) as conn:
        print("Updated montant")
        c = conn.cursor()
        c.execute('SELECT montant FROM compteur WHERE id=1')
        montant = c.fetchone()[0]
        c.execute('UPDATE compteur SET montant = ? WHERE id=1', (montant+29,))
        conn.commit()

def run_job():
    while True:
        run_pending()
        time.sleep(10)