import pytest
from unittest.mock import patch, MagicMock
from scalesafe.generic import GenericMonitor
from scalesafe.exceptions import *
import os

# Test exceptions on GenericMonitor
@pytest.fixture
def monitor_exceptions():
    monitor = GenericMonitor()
    
    os.environ['SCALESAFE_API_KEY'] = ""
    with patch.dict(os.environ, {'SCALESAFE_API_KEY': ''}):
        with pytest.raises(ScaleSafeTokenError):
            monitor._get_api_key()
    
    with pytest.raises(ScaleSafeTokenError):
        monitor.monitor(data = {'data':'temp'}, api_key='wrong_key')

    with pytest.raises(ResourceNotFoundError):
        monitor.monitor(data = {'data':'temp'}, api_key=os.environ['SCALESAFE_API_KEY_TEST'])
    
# Test API key workflows
@pytest.fixture
def monitor_api_key():
    api_key_constructor = 'test_api_key_constructor'
    monitor = GenericMonitor(api_key = api_key_constructor)
    assert monitor._get_api_key() == api_key_constructor
    api_key_pass = 'test_api_key_pass'
    assert monitor._get_api_key(api_key_pass) == api_key_pass
