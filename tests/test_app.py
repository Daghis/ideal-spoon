import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, LEVEL_NUMBERS


def test_levels_redirect():
    """Root should redirect to the level selection menu."""
    with app.test_client() as client:
        resp = client.get('/')
        assert resp.status_code == 302
        assert resp.headers['Location'].endswith('/levels')


def test_invalid_level_redirect():
    """Requesting an unknown level should redirect to the menu."""
    with app.test_client() as client:
        resp = client.get('/level/99')
        assert resp.status_code == 302
        assert resp.headers['Location'].endswith('/levels')


def test_level_completion_and_menu_unlocks():
    """Complete level 1 and verify next level unlocks in the menu."""
    with app.test_client() as client:
        # Complete level 0 first
        resp = client.get('/level/0')
        assert resp.status_code == 200
        resp = client.post('/level/0', data={'num': '1'})
        assert b'Level complete!' in resp.data
        # Start level 1
        resp = client.get('/level/1')
        assert resp.status_code == 200
        # Press all numbers for level 1
        total = LEVEL_NUMBERS[1]
        for n in range(1, total + 1):
            resp = client.post('/level/1', data={'num': str(n)})
        # After completion the success message should appear
        assert b'Level complete!' in resp.data
        # Next level link should be enabled
        assert b'href="/level/2"' in resp.data

        # Menu should show level 0,1 and 2 unlocked, 3 disabled
        resp = client.get('/levels')
        body = resp.get_data(as_text=True)
        assert '<a href="/level/0">Level 0</a>' in body
        assert '<a href="/level/1">Level 1</a>' in body
        assert '<a href="/level/2">Level 2</a>' in body
        assert 'Level 3</li>' in body and 'href="/level/3"' not in body


def test_restart_clears_progress():
    """Restart should reset clicked numbers for the current level."""
    with app.test_client() as client:
        client.get('/level/1')
        client.post('/level/1', data={'num': '1'})
        # Restart the current level
        resp = client.get('/restart')
        assert resp.status_code == 302
        # After restart, no numbers should be clicked
        with client.session_transaction() as sess:
            assert sess.get('clicked') == []


def test_order_enforced_level_2():
    """Level 2 requires numbers clicked in ascending order."""
    with app.test_client() as client:
        client.get('/level/2')
        # Wrong first click
        resp = client.post('/level/2', data={'num': '2'})
        assert b'Wrong order!' in resp.data
        # Correct sequence
        for n in range(1, 10):
            resp = client.post('/level/2', data={'num': str(n)})
        assert b'Level complete!' in resp.data


def test_reverse_order_level_3():
    """Level 3 requires numbers clicked in descending order."""
    with app.test_client() as client:
        client.get('/level/3')
        # Wrong first click
        resp = client.post('/level/3', data={'num': '1'})
        assert b'Wrong order!' in resp.data
        # Correct sequence
        for n in range(9, 0, -1):
            resp = client.post('/level/3', data={'num': str(n)})
        assert b'Level complete!' in resp.data


def test_wrong_order_resets_level_2():
    """Level 2 should reset when a wrong number is pressed."""
    with app.test_client() as client:
        client.get('/level/2')
        client.post('/level/2', data={'num': '1'})
        resp = client.post('/level/2', data={'num': '3'})
        assert b'Wrong order!' in resp.data
        with client.session_transaction() as sess:
            assert sess.get('clicked') == []
        resp = client.post('/level/2', data={'num': '1'})
        with client.session_transaction() as sess:
            assert sess.get('clicked') == [1]

