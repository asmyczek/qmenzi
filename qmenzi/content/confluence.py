import logging
from atlassian import Confluence
from functools import reduce
from qmenzi import config
from qmenzi.content.utils import html2txt

logger = logging.getLogger("qmenzi-confluence")

CONFLUENCE_BASE_URL = config('confluence.confluence_base_url')
USER_NAME = config('confluence.user_name')
AUTH_TOKEN = config('confluence.auth_token')
SSL_VERIFY = config('global.ssl_verify')


class Client(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Client, cls).__new__(cls) 
            cls.instance.confluence = Confluence(url=CONFLUENCE_BASE_URL,
                                                 username=USER_NAME,
                                                 password=AUTH_TOKEN,
                                                 cloud=True,
                                                 verify_ssl=SSL_VERIFY)
        return cls.instance


def list_page_ids_by_owner(user_id):
    resp = Client().confluence.cql(f'type=page AND creator="{user_id}"', start=0, limit=100)
    return list(map(lambda p: p['content']['id'], resp['results']))
    

def get_content_for_page_id(page_id):
    content = Client().confluence.get_page_by_id(page_id, expand='body.storage')['body']['storage']['value']
    return html2txt(content)
    

def collect_content_for_page_ids(page_ids, min_words, min_content_length):
    def collect(agg,  page_id):
        content, wc = agg
        if wc > min_words:
            return content, wc
        else:
            logger.info(f'Fetching content for page id {page_id}.')
            new_content = get_content_for_page_id(page_id)
            wc += len(new_content.split())
            logger.info(f'Aggregated content length is {wc}.')
            return f'{content}{new_content}', wc
    content = reduce(collect, page_ids, ('', 0))[0]
    return [line for line in content.split('\n') if len(line) > min_content_length]


def scrap_content_for_user_id(user_id, min_words=5000, min_content_length=50):
    page_ids = list_page_ids_by_owner(user_id)
    return collect_content_for_page_ids(page_ids, min_words, min_content_length)
