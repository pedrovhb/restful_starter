import os

from starlette.testclient import TestClient
from main import app

client = TestClient(app)


def test_register_user():
    # Test register success
    r = client.post('/register/user', json={
        'name': 'Pedro von Hertwig Batista',
        'email': 'pedrovhb@gmail.com',
        'password': 'hunter2'
    })
    assert r.status_code == 200

    # Test failed registration because e-mail already exists in DB
    r = client.post('/register/user', json={
        'name': 'Someone else',
        'email': 'pedrovhb@gmail.com',
        'password': 'abc123'
    })
    assert r.status_code == 409

    # Test failed registration (password too short)
    r = client.post('/register/user', json={
        'name': 'An User',
        'email': 'user@example.com',
        'password': 'abc'
    })
    assert r.status_code == 422

    # Test failed registration (password too long)
    r = client.post('/register/user', json={
        'name': 'An User',
        'email': 'user@example.com',
        'password': 'abcde' * 100
    })
    assert r.status_code == 422

    # Test failed registration (name too short)
    r = client.post('/register/user', json={
        'name': 'A',
        'email': 'user@example.com',
        'password': 'abcdefg'
    })
    assert r.status_code == 422

    # Test failed registration (name too long)
    r = client.post('/register/user', json={
        'name': 'Looooong Name' * 100,
        'email': 'user@example.com',
        'password': 'abcdefg'
    })
    assert r.status_code == 422

    # Test failed registration (invalid e-mail)
    r = client.post('/register/user', json={
        'name': 'Looooong Name',
        'email': 'user@example',
        'password': 'abcdef'
    })
    assert r.status_code == 422


def test_invalid_auth():
    # Test no authentication
    r = client.get('/user_data')
    assert r.status_code == 401

    # Test invalid authentication
    r = client.get('/user_data', cookies={'Authorization': 'Bearer invalidauthlol'})
    assert r.status_code == 401


def test_login():
    # Test wrong password
    r = client.post('/login/user', json={
        'email': 'pedrovhb@gmail.com',
        'password': 'hunter3'
    })
    assert r.status_code == 403
    assert 'Authorization' not in r.cookies

    # Test no such user
    r = client.post('/login/user', json={
        'email': 'nobody@gmail.com',
        'password': 'hunter3'
    })
    assert r.status_code == 404
    assert 'Authorization' not in r.cookies

    # Test correct login info
    r = client.post('/login/user', json={
        'email': 'pedrovhb@gmail.com',
        'password': 'hunter2'
    })
    assert r.status_code == 200
    assert 'Authorization' in r.cookies


def test_get_user_data():
    # Test success in getting user data
    r = client.get('/user_data')
    assert r.json().get('email') == 'pedrovhb@gmail.com'
