# Generate quiz images from prompt
# Reference: https://github.com/flowese/IdeogramWrapper

from ideogram_wrapper import IdeogramWrapper
from qmenzi import config


SSL_VERIFY = config('global.ssl_verify')
SESSION_COOKIE = config('ideogram.session_cookie')
ASPECT_RATIO = config('ideogram.aspect_ratio')
OUTPUT_FOLDER = config('ideogram.output_folder')
ENABLE_LOGGING = config('ideogram.enable_logging')

### Important, to run this add 'verify_ssl' IdeogramWrapper in your local repo

def generate_image_for_prompt(prompt):
    ideogram = IdeogramWrapper(
        session_cookie_token=SESSION_COOKIE,
        prompt=prompt,
        aspect_ratio=ASPECT_RATIO,  
        output_dir=OUTPUT_FOLDER,
        enable_logging=ENABLE_LOGGING,
        #verify_ssl=SSL_VERIFY
    )
    ideogram.inference()

