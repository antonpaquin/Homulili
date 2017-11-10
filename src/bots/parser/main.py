from datetime import timedelta

from dataflow import DataFlow

# noinspection PyUnresolvedReferences
from workers import files_from_db, get_manga_ids, printer, unzip, chapter_to_db, page_to_db


master_interval = timedelta(minutes=5).total_seconds()


df = DataFlow()

x = df.rate_limited_node(interval=master_interval, target=get_manga_ids)
x = df.node(input=x.out, target=files_from_db)
x = df.node(input=x.out, target=unzip)
x = df.node(input=x.out, target=chapter_to_db)
x = df.node(input=x.out, target=page_to_db, num_outputs=0)

df.run()
