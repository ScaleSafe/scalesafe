import pytest
from unittest.mock import patch, MagicMock
from scalesafe.generic import GenericMonitor
from scalesafe.exceptions import *
import os

# Setup as a fixture
@pytest.fixture
def monitor():
    return GenericMonitor(api_key='test_api_key', location='everywhere')

def test_init(monitor):
    assert monitor.init_api_key == 'test_api_key'
    assert monitor.location == 'everywhere'

@patch('builtins.print')  # Assuming you want to check print statements or suppress them.
def test_check_exceptions(mock_print, monitor):
    with pytest.raises(ValueError):
        monitor._checkExceptions(None)
    with pytest.raises(ScaleSafeTokenError):
        monitor._checkExceptions({"error": "Invalid API Key provided."})
    # Add more assertions for other exceptions here.

@pytest.fixture(autouse=True)
def env_setup_and_teardown():
    # Setup
    os.environ['SCALESAFE_API_KEY'] = 'env_api_key'
    yield
    # Teardown (if necessary)
    del os.environ['SCALESAFE_API_KEY']

def test_get_api_key(monitor):
    assert monitor._get_api_key() == 'test_api_key'  # Initial API Key
    assert monitor._get_api_key('direct_api_key') == 'direct_api_key'  # Direct API Key
    new_monitor = GenericMonitor()
    assert new_monitor._get_api_key() == 'env_api_key'  # Env API Key

@patch('requests.post')
def test_send_monitor(mock_post, monitor):
    mock_response = MagicMock()
    mock_response.json.return_value = {'status': 'ok'}
    mock_post.return_value = mock_response

    response = monitor._sendMonitor({'data': 'value'})
    assert response.json() == {'status': 'ok'}
    mock_post.assert_called_once()

@patch('requests.get')
def test_send_status(mock_get, monitor):
    mock_response = MagicMock()
    mock_response.json.return_value = {'status': 'Compliant'}
    mock_get.return_value = mock_response

    status = monitor._sendStatus()
    assert status == {'status': 'Compliant'}
    mock_get.assert_called_once()

@patch.object(GenericMonitor, '_sendStatus')
def test_status(mock_send_status, monitor):
    mock_send_status.return_value = {'status': 'Out of Compliance', 'message': 'Test message'}
    with pytest.raises(OutOfComplianceError):
        monitor.status()
