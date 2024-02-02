import logging

from .ts3_api import TS3API

class TeamSpeakAFKBot:
    def __init__(self, server, port, username, password, server_id, afk_channel_id, max_idle_time):
        self.ts3_api = TS3API(server, port, username, password)
        self.server_id = server_id
        self.afk_channel_id = afk_channel_id
        self.max_idle_time = max_idle_time

    def is_user_afk(self, client_idle_time):
        """
        Check if a user is considered AFK based on idle time.

        :param client_idle_time: The idle time of the client.
        :return: True if the user is considered AFK, False otherwise.
        """
        return int(client_idle_time) > self.max_idle_time

    def move_client_to_afk(self, client_id):
        """
        Move a client to the AFK channel.

        :param client_id: The client ID of the user to move.
        """
        try:
            self.ts3_api.move_client(client_id, self.afk_channel_id)
            logging.info(f"Moved client {client_id} to AFK channel.")
        except Exception as e:
            logging.error(f"An error occurred while moving client {client_id} to AFK channel: {e}")

    def run(self):
        """
        Main loop that checks clients and moves them to the AFK channel if necessary.
        """
        self.ts3_api.connect()
        self.ts3_api.use(self.server_id)

        while True:
            try:
                clients = self.ts3_api.get_clients()
                for client in clients:
                    client_id = client['clid']
                    client_info = self.ts3_api.get_client_info(client_id)
                    client_idle_time = client_info['client_idle_time']
                    client_channel_id = int(client_info['cid'])

                    if client_channel_id == self.afk_channel_id or not self.is_user_afk(client_idle_time):
                        continue

                    self.move_client_to_afk(client_id)

            except Exception as e:
                logging.error(f"An error occurred: {e}")

            self.ts3_api.sleep(60)

