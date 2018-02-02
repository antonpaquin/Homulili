from datetime import timedelta
import logging

from dataflow import DataFlow
from workers import get_manga_ids, urls_from_db, name_file, download_file, update_db


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='/var/log/homulili/scraper.log',
    filemode='w',
)
logger = logging.getLogger(__name__)


master_interval = timedelta(minutes=5).total_seconds()
madokami_file_interval = timedelta(seconds=30).total_seconds()

logger.info('Starting scraper')
df = DataFlow()
x = df.rate_limited_node(interval=master_interval, target=get_manga_ids)
x = df.node(input=x.out, target=urls_from_db)
x = df.node(input=x.out, target=name_file)
x = df.rate_limited_node(interval=madokami_file_interval, input=x.out, target=download_file)
x = df.node(input=x.out, target=update_db, num_outputs=0)

logger.debug('Scraper graph initialized')

df.run()
