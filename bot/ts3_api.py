"""
This module provides a Python interface to interact with a TeamSpeak 3 server.

It defines the TS3API class, which encapsulates the functionality for connecting to a TeamSpeak
server, managing clients and channels, and handling errors. The class uses the ts3 library to
interact with the
TeamSpeak 3 ServerQuery interface.

The TS3API class provides methods to connect and disconnect from the server, select a virtual
server, retrieve lists of clients and channels, retrieve information about a specific client,
move a client to a different channel, and sleep for a specified duration.
"""

import logging
import time

import ts3


class TS3API:
    """
    A class that encapsulates the functionality for interacting with a TeamSpeak 3 server.

    This class uses the ts3 library to interact with the TeamSpeak 3 ServerQuery interface.
    It provides methods for connecting and disconnecting from the server, selecting a virtual
    server, retrieving lists of clients and channels, retrieving information about a specific
    client, moving a client to a different channel, and sleeping for a specified duration.
    """

    def __init__(self, server, query_port, username, password):
        """
        Initialize the TS3API class.

        :param server: The TeamSpeak 3 server address.
        :param query_port: The query port of the TeamSpeak 3 server.
        :param username: The username to authenticate with.
        :param password: The password to authenticate with.
        """
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
                client_login_name=self.username, client_login_password=self.password
            )
        except Exception as e:
            logging.error(
                "An error occurred while connecting to the TeamSpeak server: %s", e
            )
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
                logging.error(
                    "An error occurred while selecting the virtual server: %s", e
                )
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
                logging.error(
                    "An error occurred while retrieving the client list: %s", e
                )
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
                logging.error(
                    "An error occurred while retrieving client information: %s", e
                )
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
                logging.error("An error occurred while moving the client: %s", e)
                raise e

    def list_channels(self):
        """
        Retrieve a list of channels from the TeamSpeak 3 server.

        :return: A list of channels.
        """
        if self.ts3conn:
            try:
                return self.ts3conn.channellist()
            except Exception as e:
                logging.error(
                    "An error occurred while retrieving the channel list: %s", e
                )
                raise e

    def sleep(self, duration):
        """
        Sleep for a certain duration. This is just a wrapper for time.sleep to keep everything
        encapsulated.

        :param duration: The duration to sleep in seconds.
        """
        time.sleep(duration)

    def disconnect(self):
        """
        Disconnect from the TeamSpeak 3 server.
        """
        if self.ts3conn:
            self.ts3conn.quit()
