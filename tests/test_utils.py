import unittest
from unittest.mock import patch

from bot.utils import get_env_var


class TestUtils(unittest.TestCase):

    @patch('bot.utils.os.getenv')
    def test_get_env_var_exists(self, mock_getenv):
        mock_getenv.return_value = 'test_value'
        result = get_env_var('TEST_VAR')

        self.assertEqual(result, 'test_value')
        mock_getenv.assert_called_once_with('TEST_VAR', None)

    @patch('bot.utils.os.getenv')
    def test_get_env_var_not_exists_required(self, mock_getenv):
        mock_getenv.return_value = None

        with self.assertRaises(SystemExit):
            get_env_var('TEST_VAR', required=True)

    @patch('bot.utils.os.getenv')
    def test_get_env_var_with_default(self, mock_getenv):
        mock_getenv.return_value = None

        result = get_env_var('TEST_VAR', default='default_value', required=False)

        self.assertEqual(result, 'default_value')

    @patch('bot.utils.os.getenv')
    def test_get_env_var_type_conversion(self, mock_getenv):
        mock_getenv.return_value = '123'

        result = get_env_var('TEST_VAR', var_type=int)

        self.assertEqual(result, 123)


if __name__ == '__main__':
    unittest.main()
