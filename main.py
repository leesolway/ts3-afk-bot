import os
import ts3
import time
import socket
import logging
import signal
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

TS3_SERVER = os.getenv('TS3_SERVER')
QUERY_PORT = int(os.getenv('QUERY_PORT', '10011'))
SERVER_ID = int(os.getenv('SERVER_ID', '1'))
QUERY_USERNAME = os.getenv('QUERY_USERNAME')
QUERY_PASSWORD = os.getenv('QUERY_PASSWORD')
AFK_CHANNEL_ID = int(os.getenv('AFK_CHANNEL_ID', '2'))
MAX_IDLE_TIME = int(os.getenv('MAX_IDLE_TIME', '300000'))

if not TS3_SERVER or not QUERY_USERNAME or not QUERY_PASSWORD:
    logging.error("Critical configuration is missing. Please set TS3_SERVER, QUERY_USERNAME, and QUERY_PASSWORD environment variables.")
    sys.exit(1)

def is_user_afk(client_idle_time):
    return int(client_idle_time) > MAX_IDLE_TIME

def signal_handler(sig, frame):
    logging.info('Shutdown signal received. Exiting.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

try:
    with ts3.query.TS3Connection(TS3_SERVER, QUERY_PORT) as ts3conn:
        ts3conn.login(
            client_login_name=QUERY_USERNAME,
            client_login_password=QUERY_PASSWORD
        )

        ts3conn.use(sid=SERVER_ID)

        while True:
            try:
                clients = ts3conn.clientlist()
                for client in clients:
                    clid = client['clid']
                    client_info = ts3conn.clientinfo(clid=clid)[0]
                    client_idle_time = client_info['client_idle_time']

                    if is_user_afk(client_idle_time):
                        ts3conn.clientmove(clid=clid, cid=AFK_CHANNEL_ID)
                        logging.info(f"Moved client {clid} to AFK channel.")

            except Exception as e:
                logging.error(f"An error occurred: {e}")

            time.sleep(60)
except socket.gaierror:
    logging.error(f"Could not resolve hostname {TS3_SERVER}. Please check the server address and your network connection.")
except ts3.query.TS3QueryError as e:
    logging.error(f"An error occurred with the TeamSpeak server query: {e}")
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
