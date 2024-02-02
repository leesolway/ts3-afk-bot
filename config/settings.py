from bot.utils import get_env_var

TS3_SERVER = get_env_var('TS3_SERVER', required=True)
QUERY_PORT = get_env_var('QUERY_PORT', default='10011', var_type=int)
SERVER_ID = get_env_var('SERVER_ID', default='1', var_type=int)
QUERY_USERNAME = get_env_var('QUERY_USERNAME', required=True)
QUERY_PASSWORD = get_env_var('QUERY_PASSWORD', required=True)

AFK_CHANNEL_ID = get_env_var('AFK_CHANNEL_ID', default='2', var_type=int)
MAX_IDLE_TIME = get_env_var('MAX_IDLE_TIME', default='1800000', var_type=int)  # 30 minutes in milliseconds

