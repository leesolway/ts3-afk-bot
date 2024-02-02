import logging
import time
import ts3


class TS3API:
    def __init__(self, server, query_port, username, password):
        self.server = server
        self.query_port = query_port
        self.username = username
        self.password = password
        self.ts3conn = None

    def connect(self):
        """
        Establish a connection to the TeamSpeak 3 server.
        """
        try:
            self.ts3conn = ts3.query.TS3Connection(self.server, self.query_port)
            self.ts3conn.login(
                client_login_name=self.username,
                client_login_password=self.password
            )
        except Exception as e:
            logging.error(f"An error occurred while connecting to the TeamSpeak server: {e}")
            raise e

    def use(self, server_id):
        """
        Select the virtual TeamSpeak 3 server.

        :param server_id: The server ID to use.
        """
        if self.ts3conn:
            try:
                self.ts3conn.use(sid=server_id)
            except Exception as e:
                logging.error(f"An error occurred while selecting the virtual server: {e}")
                raise e

    def get_clients(self):
        """
        Retrieve a list of clients from the TeamSpeak 3 server.

        :return: A list of clients.
        """
        if self.ts3conn:
            try:
                return self.ts3conn.clientlist()
            except Exception as e:
                logging.error(f"An error occurred while retrieving the client list: {e}")
                raise e

    def get_client_info(self, client_id):
        """
        Retrieve information for a specific client.

        :param client_id: The client ID to get information for.
        :return: A dictionary of client information.
        """
        if self.ts3conn:
            try:
                return self.ts3conn.clientinfo(clid=client_id)[0]
            except Exception as e:
                logging.error(f"An error occurred while retrieving client information: {e}")
                raise e

    def move_client(self, client_id, channel_id):
        """
        Move a client to a different channel.

        :param client_id: The client ID to move.
        :param channel_id: The channel ID to move the client to.
        """
        if self.ts3conn:
            try:
                self.ts3conn.clientmove(clid=client_id, cid=channel_id)
            except Exception as e:
                logging.error(f"An error occurred while moving the client: {e}")
                raise e

    def sleep(self, duration):
        """
        Sleep for a certain duration. This is just a wrapper for time.sleep to keep everything encapsulated.

        :param duration: The duration to sleep in seconds.
        """
        time.sleep(duration)

    def disconnect(self):
        """
        Disconnect from the TeamSpeak 3 server.
        """
        if self.ts3conn:
            self.ts3conn.quit()
