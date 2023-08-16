#!/usr/bin/env python3
"""End-to-end integration test"""

import requests

url = 'http://0.0.0.0:5000'


def register_user(email: str, password: str) -> None:
    """register user"""
    r = requests.post(
        f'{url}/users',
        data={
            'email': email,
            'password': password})
    if r.status_code == 200:
        assert r.json() == {'email': email, 'message': 'user created'}
    elif r.status_code == 400:
        assert r.json() == {'message': 'email already registered'}


def log_in_wrong_password(email: str, password: str) -> None:
    """log in with wrong password"""
    r = requests.post(
        f'{url}/sessions',
        data={
            'email': email,
            'password': password})
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """log in"""
    r = requests.post(
        f'{url}/sessions',
        data={
            'email': email,
            'password': password})
    # assert r.status_code == 200
    assert r.json() == {'email': email, 'message': 'logged in'}
    session_id = r.cookies.get('session_id')
    return session_id


def profile_unlogged() -> None:
    """test profile unlogged"""
    r = requests.get(f'{url}/profile')
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """test profile logged"""
    r = requests.get(f'{url}/profile', cookies={'session_id': session_id})
    assert r.status_code == 200
    assert r.json() == {'email': EMAIL}


def log_out(session_id: str) -> None:
    """test logout"""
    r = requests.delete(f'{url}/sessions', cookies={'session_id': session_id})
    assert r.status_code == 200
    assert r.history[0].status_code == 302


def reset_password_token(email: str) -> str:
    """test reset password token"""
    r = requests.post(f'{url}/reset_password', data={'email': email})
    # assert r.status_code == 200
    print(r.status_code)
    assert r.json().get('email') == email
    return r.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """test update password"""
    r = requests.put(
        f'{url}/reset_password',
        data={
            'email': email,
            'reset_token': reset_token,
            'new_password': new_password})
    # assert r.status_code == 200
    assert r.json() == {'email': email, 'message': 'Password updated'}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
