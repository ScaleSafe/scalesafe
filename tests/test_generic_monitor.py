

import unittest
from unittest.mock import patch, MagicMock
from scalesafe.generic import GenericMonitor
from scalesafe.exceptions import *
import os

class TestGenericMonitor(unittest.TestCase):

    def setUp(self):
        self.monitor = GenericMonitor(api_key='test_api_key', location='everywhere')

    def test_init(self):
        self.assertEqual(self.monitor.init_api_key, 'test_api_key')
        self.assertEqual(self.monitor.location, 'everywhere')

    @patch('builtins.print')  # Assuming you want to check print statements or suppress them.
    def test_check_exceptions(self, mock_print):
        self.assertRaises(ValueError, self.monitor._checkExceptions, None)
        self.assertRaises(ScaleSafeTokenError, self.monitor._checkExceptions, {"error": "Invalid API Key provided."})
        # Add more assertions for other exceptions here.

    @patch.dict(os.environ, {'SCALESAFE_API_KEY': 'env_api_key'})
    def test_get_api_key(self):
        self.assertEqual(self.monitor._get_api_key(), 'test_api_key')  # Initial API Key
        self.assertEqual(self.monitor._get_api_key('direct_api_key'), 'direct_api_key')  # Direct API Key
        new_monitor = GenericMonitor()
        self.assertEqual(new_monitor._get_api_key(), 'env_api_key')  # Env API Key

    @patch('requests.post')
    def test_send_monitor(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'ok'}
        mock_post.return_value = mock_response

        response = self.monitor._sendMonitor({'data': 'value'})
        self.assertEqual(response.json(), {'status': 'ok'})
        mock_post.assert_called_once()

    @patch('requests.get')
    def test_send_status(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {'status': 'Compliant'}
        mock_get.return_value = mock_response

        status = self.monitor._sendStatus()
        self.assertEqual(status, {'status': 'Compliant'})
        mock_get.assert_called_once()

    @patch.object(GenericMonitor, '_sendStatus')
    def test_status(self, mock_send_status):
        mock_send_status.return_value = {'status': 'Out of Compliance', 'message': 'Test message'}
        self.assertRaises(OutOfComplianceError, self.monitor.status)

if __name__ == '__main__':
    unittest.main()
