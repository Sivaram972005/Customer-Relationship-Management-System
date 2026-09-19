import mysql.connector
from config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

def fetch_all(sql, params=()):
    con=get_connection(); cur=con.cursor(dictionary=True)
    try:
        cur.execute(sql, params); return cur.fetchall()
    finally:
        cur.close(); con.close()

def fetch_one(sql, params=()):
    con=get_connection(); cur=con.cursor(dictionary=True)
    try:
        cur.execute(sql, params); return cur.fetchone()
    finally:
        cur.close(); con.close()

def execute(sql, params=()):
    con=get_connection(); cur=con.cursor()
    try:
        cur.execute(sql, params); con.commit(); return cur.lastrowid
    except Exception:
        con.rollback(); raise
    finally:
        cur.close(); con.close()
