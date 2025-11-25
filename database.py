import streamlit as st
import pandas as pd
import time 
import hashlib
import random
import sqlite3
from datetime import datetime, timedelta

DB_NAME = 'database_baru_v3.db' 

def make_hashes(password):
    """Menghasilkan hash SHA256 dari password."""
    return hashlib.sha256(str.encode(password)).hexdigest()

@st.cache_resource
def get_db_connection():
    """Mendapatkan koneksi database SQLite."""
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    """Menginisialisasi tabel database jika belum ada."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS userdata (
            username TEXT PRIMARY KEY, 
            password TEXT, 
            email TEXT,
            role TEXT, 
            full_name TEXT,
            age INTEGER,
            about_me TEXT,
            work_history TEXT,
            join_date TEXT
        )
    ''')
    conn.commit()

def register_user(username, email, password_hash, role='seeker'):
    """Mendaftarkan pengguna baru ke database."""
    conn = get_db_connection()
    c = conn.cursor()
    join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        c.execute('''INSERT INTO userdata
                     (username, password, email, role, full_name, age, about_me, work_history, join_date) 
                     VALUES (?,?,?,?,?,?,?,?,?)''', 
                  (username, password_hash, email, role, "", 0, "", "", join_date))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    except Exception:
        return False

def login_user_db(username, password_hash):
    """Memverifikasi kredensial login pengguna."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM userdata WHERE username = ? AND password = ?', (username, password_hash))
    data = c.fetchall()
    return data

def get_user_profile(username):
    """Mengambil data profil pengguna."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT email, full_name, age, about_me, work_history FROM userdata WHERE username = ?', (username,))
    data = c.fetchone()
    return data

def update_user_profile(username, full_name, age, about_me, work_history, new_email):
    """Memperbarui data profil pengguna."""
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute('''UPDATE userdata 
                     SET full_name = ?, age = ?, about_me = ?, work_history = ?, email = ? 
                     WHERE username = ?''', 
                  (full_name, age, about_me, work_history, new_email, username))
        conn.commit()
        return True
    except Exception:
        return False

init_db()
if not login_user_db('admin', make_hashes('admin')):
    register_user('admin', 'admin@getcareer.com', make_hashes('admin'), 'admin')
