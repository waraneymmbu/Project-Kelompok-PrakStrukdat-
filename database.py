import streamlit as st
import pandas as pd
import time
import hashlib
import random
import sqlite3
from datetime import datetime, timedelta

DB_NAME = 'database_baru_v3.db'


def make_hashes(password: str) -> str:
    return hashlib.sha256(str.encode(password)).hexdigest()


@st.cache_resource
def get_db_connection():
    # check_same_thread=False supaya bisa dipakai Streamlit
    return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
    """
    Membuat tabel userdata dengan kolom:
    username, password, email, role, full_name, age, about_me, work_history,
    join_date, photo, cv_file, linkedin_url, portfolio_file
    """
    conn = get_db_connection()
    c = conn.cursor()

    c.execute(
        '''
        CREATE TABLE IF NOT EXISTS userdata (
            username TEXT PRIMARY KEY,
            password TEXT,
            email TEXT,
            role TEXT,
            full_name TEXT,
            age INTEGER,
            about_me TEXT,
            work_history TEXT,
            join_date TEXT,
            photo BLOB,
            cv_file BLOB,
            linkedin_url TEXT,
            portfolio_file BLOB
        )
        '''
    )
    conn.commit()


def register_user(username, email, password_hash, role='seeker'):
    """
    Register user baru dengan nilai default:
    full_name="", age=0, about_me="", work_history="",
    photo NULL, cv_file NULL, linkedin_url "", portfolio_file NULL.
    """
    conn = get_db_connection()
    c = conn.cursor()
    join_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        c.execute(
            '''
            INSERT INTO userdata
            (username, password, email, role,
             full_name, age, about_me, work_history,
             join_date, photo, cv_file, linkedin_url, portfolio_file)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''',
            (
                username,
                password_hash,
                email,
                role,
                "",            # full_name
                0,             # age
                "",            # about_me
                "",            # work_history
                join_date,
                None,          # photo
                None,          # cv_file
                "",            # linkedin_url
                None           # portfolio_file
            )
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # username sudah ada
        return False
    except Exception:
        return False


def login_user_db(username, password_hash):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        'SELECT * FROM userdata WHERE username = ? AND password = ?',
        (username, password_hash)
    )
    data = c.fetchall()
    return data


def get_user_profile(username):
    """
    Dipakai di profile_page():
    return:
      email, full_name, age, about_me, work_history,
      photo, cv_file, linkedin_url, portfolio_file
    """
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        '''
        SELECT email,
               full_name,
               age,
               about_me,
               work_history,
               photo,
               cv_file,
               linkedin_url,
               portfolio_file
        FROM userdata
        WHERE username = ?
        ''',
        (username,)
    )
    data = c.fetchone()
    return data


def update_user_profile(
    username,
    full_name,
    age,
    about_me,
    work_history,
    new_email,
    linkedin_url,
    photo_blob,
    cv_blob,
    portfolio_blob
):
    """
    Dipanggil dari profile_page() saat klik SIMPAN.
    Foto boleh tetap None (karena di UI nggak diubah).
    """
    conn = get_db_connection()
    c = conn.cursor()
    try:
        c.execute(
            '''
            UPDATE userdata
            SET full_name     = ?,
                age           = ?,
                about_me      = ?,
                work_history  = ?,
                email         = ?,
                linkedin_url  = ?,
                photo         = ?,
                cv_file       = ?,
                portfolio_file= ?
            WHERE username    = ?
            ''',
            (
                full_name,
                age,
                about_me,
                work_history,
                new_email,
                linkedin_url,
                photo_blob,
                cv_blob,
                portfolio_blob,
                username
            )
        )
        conn.commit()
        return True
    except Exception:
        return False


# Inisialisasi DB & buat user admin default
init_db()
if not login_user_db('admin', make_hashes('admin')):
    register_user('admin', 'admin@getcareer.com', make_hashes('admin'), 'admin')
