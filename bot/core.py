"""
This module defines the TeamSpeakAFKBot class, which is used to manage AFK (Away From Keyboard)
users on a TeamSpeak server.

The bot checks if users are AFK based on their idle time and moves them to a specified AFK channel.
"""

import logging

from .ts3_api import TS3API


class TeamSpeakAFKBot:
    """
    A bot for managing AFK (Away From Keyboard) users on a TeamSpeak server.

    The bot checks if users are AFK based on their idle time and moves them to a specified AFK
    channel.

    Attributes:
        ts3_api (TS3API): An instance of the TS3API class for interacting with the TeamSpeak server.
        server_id (int): The ID of the server on which the bot operates.
        afk_channel_id (int): The ID of the channel to which AFK users are moved.
        max_idle_time (int): The maximum idle time (in seconds) before a user is considered AFK.
        channel_ids (list): A list of channel IDs to be considered based on the mode.
        mode (str): The mode of operation. Can be 'blacklist' or 'whitelist'.
    """

    def __init__(
        self,
        server,
        port,
        username,
        password,
        server_id,
        afk_channel_id,
        max_idle_time,
        channel_ids,
        mode,
    ):
        self.ts3_api = TS3API(server, port, username, password)
        self.server_id = server_id
        self.afk_channel_id = afk_channel_id
        self.max_idle_time = max_idle_time
        self.channel_ids = channel_ids or []
        self.mode = mode

    @staticmethod
    def should_process_channel(cid, afk_channel_id, mode, channel_ids):
        """
        Determines whether a given channel should be processed based on the bot's mode and
        channel IDs.

        Parameters:
        cid: The channel to check.

        Returns:
        bool: True if the channel should be processed, False otherwise.
        """
        channel_id = int(cid)

        is_valid_channel = channel_id is not None
        is_not_afk_channel = channel_id != afk_channel_id
        is_blacklisted = mode == "blacklist" and channel_id not in channel_ids
        is_whitelisted = mode == "whitelist" and channel_id in channel_ids

        should_process = (
            is_valid_channel
            and is_not_afk_channel
            and (is_blacklisted or is_whitelisted)
        )

        return should_process

    def is_user_afk(self, client_idle_time):
        """
        Check if a user is considered AFK based on idle time.

        :param client_idle_time: The idle time of the client.
        :return: True if the user is considered AFK, False otherwise.
        """
        return int(client_idle_time) > self.max_idle_time

    def move_client_to_afk(self, client_id, client_info):
        """
        Move a client to the AFK channel.

        :param client_id: unqiue identifier for the client.
        :param client_info: Information about the client to move.
        """
        client_nickname = client_info.get("client_nickname", "Unknown")

        try:
            self.ts3_api.move_client(client_id, self.afk_channel_id)
            logging.info(
                "Moved client %s (ID: %s) to AFK channel.", client_nickname, client_id
            )
        except Exception as e:
            logging.error(
                "An error occurred while moving client %s (ID: %s) to AFK channel: %s",
                client_nickname,
                client_id,
                e,
            )

    def should_move_client(self, client_info):
        """
        Determine if a client should be moved to the AFK channel based on the channel IDs and mode.
        """
        client_channel_id = int(client_info["cid"])
        client_idle_time = client_info["client_idle_time"]

        # If the user is not AFK, don't move them.
        if not self.is_user_afk(client_idle_time):
            return False

        return TeamSpeakAFKBot.should_process_channel(
            client_channel_id, self.afk_channel_id, self.mode, self.channel_ids
        )

    def run(self):
        """
        Main loop that checks clients and moves them to the AFK channel if necessary.
        """
        try:
            self.ts3_api.connect()
            self.ts3_api.use(self.server_id)
        except Exception as e:
            logging.error("An error occurred while connecting to the server: %s", e)
            return

        while True:
            try:
                clients = self.ts3_api.get_clients()
                if not clients:
                    logging.info("No clients were retrieved from the server.")
                    continue

                for client in clients:
                    client_id = client.get("clid")
                    if not client_id:
                        logging.warning(
                            "Client data does not contain 'clid', skipping this client: %s",
                            client,
                        )
                        continue

                    try:
                        client_info = self.ts3_api.get_client_info(client_id)
                        if not client_info:
                            logging.warning(
                                "No info retrieved for client with ID %s", client_id
                            )
                            continue

                        if self.should_move_client(client_info):
                            self.move_client_to_afk(client_id, client_info)
                    except Exception as e:
                        logging.error(
                            "An error occurred while processing client with ID %s: %s",
                            client_id,
                            e,
                        )

            except Exception as e:
                logging.error("An error occurred during main loop: %s", e)
                # Add a delay before retrying
                self.ts3_api.sleep(10)

            self.ts3_api.sleep(60)
