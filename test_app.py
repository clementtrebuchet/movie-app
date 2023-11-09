# test_app.py
from unittest.mock import MagicMock, patch

import pytest

from app import app, generate_movie_release_chart


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_cursor():
    # This is a mock cursor that you can set up to return expected values
    cursor = MagicMock()
    cursor.fetchall.return_value = [('1995-10-30',), ('1999-11-18',)]
    return cursor


@pytest.fixture
def mock_conn(mock_cursor):
    # This is a mock connection that returns your mock cursor
    conn = MagicMock()
    conn.cursor.return_value = mock_cursor
    return conn


def test_load_data_endpoint(client):
    # This test would hit the '/load-data' endpoint and assert the response
    # It might also check if the database has been populated correctly
    response = client.get('/load-data')
    assert response.status_code == 200
    assert response.data == b'Data loaded successfully into the database'


def test_export_data(client):
    # This test would hit the '/export-data' endpoint and assert the response
    response = client.get('/export-data')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'text/csv'


def test_generate_movie_release_chart(tmp_path, mock_conn, mock_cursor):
    chart_path = tmp_path / "chart.png"

    with patch('sqlite3.connect', return_value=mock_conn):
        # Call the function to generate the chart
        generate_movie_release_chart(chart_path=chart_path)

        # Now check if the chart was saved correctly
        assert chart_path.exists()

        # You could also check if the cursor was called correctly
        mock_cursor.execute.assert_called_with("SELECT release_date FROM movies")
        mock_cursor.fetchall.assert_called()

        # And if the connection was closed
        mock_conn.close.assert_called()

    # Clean up the chart file after test
    if chart_path.exists():
        chart_path.unlink()
