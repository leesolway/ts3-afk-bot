from bot.utils import get_env_var

TS3_SERVER = get_env_var('TS3_SERVER', required=True)
QUERY_PORT = get_env_var('QUERY_PORT', default='10011', var_type=int)
SERVER_ID = get_env_var('SERVER_ID', default='1', var_type=int)
QUERY_USERNAME = get_env_var('QUERY_USERNAME', required=True)
QUERY_PASSWORD = get_env_var('QUERY_PASSWORD', required=True)

AFK_CHANNEL_ID = get_env_var('AFK_CHANNEL_ID', var_type=int, required=True)
CHANNEL_IDS = [int(cid) for cid in get_env_var('CHANNEL_IDS', default='', var_type=str).split(',') if cid]
MODE = get_env_var('MODE', required=True, default="blacklist")  # 'blacklist' or 'whitelist'

MAX_IDLE_TIME = get_env_var('MAX_IDLE_TIME', default='1800000', var_type=int)  # 30 minutes in milliseconds

# Check to ensure MODE is either 'blacklist' or 'whitelist'
if MODE not in ['blacklist', 'whitelist']:
    raise ValueError("MODE must be either 'blacklist' or 'whitelist'")