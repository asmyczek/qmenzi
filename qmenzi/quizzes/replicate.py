import os
import logging
from qmenzi import config

logger = logging.getLogger("qmenzi-quizzes-ideogram")

AUTH_TOKEN = config('replicate.api_token')

def authenticate():
    os.environ['REPLICATE_API_TOKEN'] = AUTH_TOKEN

