from queue import Queue
import logging

import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth

import secret
from dataflow.utils import input_protection
from workers.head_url import HeadUrl

logger = logging.getLogger(__name__)

madokami_auth = HTTPBasicAuth(secret.madokami_uname, secret.madokami_pass)


class NodeUrl:
    def __init__(self, manga_id, url):
        self.manga_id = manga_id
        self.url = url


@input_protection()
def node_url(input: HeadUrl, output: Queue):
    logger.debug('Entering node_url')
    logger.info('Fetching manga {manga_id} from madokami'.format(
        manga_id=input.manga_id,
    ))
    x = requests.get(input.url, auth=madokami_auth)
    x = BeautifulSoup(x.text, 'html5lib')
    x = x.find_all('tr')
    x = filter(lambda tag: tag.has_attr('data-record'), x)
    x = map(lambda tag: tag.find('a')['href'], x)
    for result in x:
        output.put(NodeUrl(
            manga_id=input.manga_id,
            url='https://manga.madokami.al{location}'.format(location=result)
        ))
