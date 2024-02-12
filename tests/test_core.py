# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring
import unittest
from unittest.mock import MagicMock

from bot.core import TeamSpeakAFKBot


class TestTeamSpeakAFKBot(unittest.TestCase):
    def setUp(self):
        self.mock_ts3api = MagicMock()

        # Initialize the TeamSpeakAFKBot with the mock TS3API object
        self.bot = TeamSpeakAFKBot(
            server="fake_server",
            port=10011,
            username="fake_user",
            password="fake_password",
            server_id=1,
            afk_channel_id=2,
            max_idle_time=300000,
            channel_ids=[2, 3, 4],
            mode="whitelist",
        )
        self.bot.ts3_api = self.mock_ts3api

    def test_is_user_afk(self):
        # Test case where user should be considered AFK
        self.assertTrue(self.bot.is_user_afk(300001))

        # Test case where user should not be considered AFK
        self.assertFalse(self.bot.is_user_afk(299999))

    def test_move_client_to_afk(self):
        client_id = 123
        client_info = {
            "clid": client_id,
            "client_nickname": "TestUser",
            "cid": 5,
            "client_idle_time": "300001",
        }
        self.mock_ts3api.move_client.return_value = None
        self.mock_ts3api.get_client_info.return_value = client_info

        # Action
        self.bot.move_client_to_afk(client_info)

        # Assert
        self.mock_ts3api.move_client.assert_called_once_with(
            client_id, self.bot.afk_channel_id
        )


if __name__ == "__main__":
    unittest.main()
