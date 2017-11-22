from datetime import timedelta
import logging

from dataflow import DataFlow
from workers import head_url, node_url, newfile_filter, ignore_filter, file_to_db


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename='/var/log/homulili/scanner.log',
    filemode='w',
)
logger = logging.getLogger(__name__)


master_update_interval = timedelta(minutes=30).total_seconds()
madokami_stage_interval = timedelta(seconds=10).total_seconds()

logger.info('Starting scanner')
df = DataFlow()
x = df.rate_limited_node(target=head_url, interval=master_update_interval)
x = df.rate_limited_node(input=x.out, target=node_url, interval=madokami_stage_interval)
x = df.node(input=x.out, target=newfile_filter)
x = df.node(input=x.out, target=ignore_filter)
x = df.node(input=x.out, num_outputs=0, target=file_to_db)

logger.debug('Scanner graph initialized')

df.run()
