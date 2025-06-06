import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


def test_levels_redirect():
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 302
