import os
from qmenzi import config

AUTH_TOKEN = config('replicate.api_token')

def authenticate():
    os.environ['REPLICATE_API_TOKEN'] = AUTH_TOKEN

