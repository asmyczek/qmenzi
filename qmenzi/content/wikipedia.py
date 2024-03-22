import logging
import requests
from functools import reduce
from qmenzi import config
from qmenzi.utils import html2txt

logger = logging.getLogger("qmenzi-wikipedia")

SSL_VERIFY = config('global.ssl_verify')
WIKI_PARSE_QUERY = 'https://en.wikipedia.org/w/api.php?action=parse&format=json&page={page_name}&{params}'


class ContentDoesNotExist(Exception):
    pass


def query_wikipedia_api(url):
    resp = requests.get(url, timeout=10, verify=SSL_VERIFY)
    return resp.json()


def get_page_section_ids(page_name):
    resp = query_wikipedia_api(
        WIKI_PARSE_QUERY.format(
            page_name=page_name,
            params='prop=sections&disabletoc=1'))
    def add_section(scs, s):
        scs[s['line'].replace(' ', '_')] = s['index']
        return scs
    return reduce(add_section, resp['parse']['sections'], {})


def get_page_section_by_section_id(page_name, section_id):
    resp = query_wikipedia_api(
        WIKI_PARSE_QUERY.format(
            page_name=page_name,
            params=f'prop=text&section={section_id}&disabletoc=1'))
    return resp


def remove_cite_errors(html_string):
    # TODO: remove span section with cite errors
    return html_string


def get_page_section_by_section_name(page_name, section_name):
    sections = get_page_section_ids(page_name)
    logger.info(f'Fetched {len(sections)} sections from {page_name}.')
    section_id = sections.get(section_name)
    logger.info(f'{section_name} section id is {section_id}.')
    if section_id:
        sresp = get_page_section_by_section_id(page_name, section_id)
        content = html2txt(sresp['parse']['text']['*'])
        return remove_cite_errors(content)
    else:
        raise ContentDoesNotExist(f'{section_name} does not exist in {page_name}.')

