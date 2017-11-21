from datetime import timedelta
import logging

from dataflow import DataFlow

# noinspection PyUnresolvedReferences
from workers import files_from_db, get_manga_ids, printer, unzip, chapter_to_db, page_to_db

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='/var/log/homulili/parser.log',
    filemode='w',
)
logger = logging.getLogger(__name__)

master_interval = timedelta(minutes=5).total_seconds()

logger.info('Starting parser')
df = DataFlow()

x = df.rate_limited_node(interval=master_interval, target=get_manga_ids)
x = df.node(input=x.out, target=files_from_db)
x = df.node(input=x.out, target=unzip, num_outputs=2)
x.out[1].maxsize = 3
y = df.node(input=x.out[0], target=chapter_to_db, num_outputs=0)
y = df.node(input=x.out[1], target=page_to_db, num_outputs=0)

logger.debug('Parser graph initialized')

df.run()
