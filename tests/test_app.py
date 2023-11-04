import pytest
from main import app  # Assuming your Flask application is named main.py

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_load_data_endpoint(client):
    """Test the /load-data endpoint."""
    response = client.get('/load-data')
    assert response.status_code == 200
    assert 'Data loaded into SQLite database successfully.' in response.data.decode('utf-8')

def test_draw_chart_endpoint(client):
    """Test the /draw-chart endpoint."""
    # First, ensure data is loaded
    client.get('/load-data')
    response = client.get('/draw-chart')
    assert response.status_code == 200
    assert response.content_type == 'image/png'

def test_export_data_endpoint(client):
    """Test the /export-data endpoint."""
    # First, ensure data is loaded
    client.get('/load-data')
    response = client.get('/export-data')
    assert response.status_code == 200
    assert response.content_type == 'text/csv'
    # More assertions can be added to check the contents of the CSV