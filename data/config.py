#API_TOKEN = '887257503:AAGYnE_ReTm9HzkN047WXgrx2Wh9GKqHYQ8'
API_TOKEN = '1089789060:AAE1Y0dWyjZfsRLunoXPXP3TYbAz73c7eZM'
# PROXY_URL = 'socks5://194.242.126.235:8000'
# provider_token = "535936410:LIVE:1089789060_e7e9f8ef-74dc-4011-be12-c84cc861b72d" #Tranzzo
# provider_token = "410694247:TEST:b305b38f-0212-4427-8a60-f3125115e6dc" #Test
provider_token = "410694247:TEST:e3d567b8-c3c5-4bf0-9f3d-4adb5b0d3f2d"
publicKeyQIWI = "48e7qUxn9T7RyYE1MVZswX1FRSbE6iyCj2gCRwwF3Dnh5XrasNTx3BGPiMsyXQFNKQhvukniQG8RTVhYm3iPtoMap5fEJ7DxRtZW86kKJmVXxgA2xF7dxEzfwp2DCyiBaXHWxHTWxq6vNkuRTP3fe8UDCbb3iJmCULHj7VFQyozq2V61LuWSYEVQw6RcT"

import os
BOT_TOKEN = str(os.getenv(API_TOKEN))
admins = [765333440]
#
ip = os.getenv("ip")

aiogram_redis = {
    'host': ip,
}
redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}