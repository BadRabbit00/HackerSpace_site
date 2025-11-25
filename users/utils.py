import hashlib
import hmac
from django.conf import settings

def verify_telegram_data(data):
    """
    Verifies the data received from Telegram login widget.
    """
    bot_token = settings.TELEGRAM_BOT_TOKEN
    if not bot_token:
        return False

    received_hash = data.get('hash')
    if not received_hash:
        return False

    data_check_arr = []
    for key, value in data.items():
        if key != 'hash':
            data_check_arr.append(f'{key}={value}')
    
    data_check_arr.sort()
    data_check_string = '\n'.join(data_check_arr)
    
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    
    return calculated_hash == received_hash
