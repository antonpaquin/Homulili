import re

def guess_chapter(filename):
    try:
        cname = re.search('[cC][0-9]+', filename).group()
        return int(cname[1:])
    except Exception as e:
        logger.error('Couldn\'t guess chapter from filename -- {filename}'.format(
            filename=filename,
        ))
        raise e


def get_number(name):
    try:
        return int(re.search('[0-9]+', name).group())
    except Exception as e:
        logger.error('Couldn\'t find a number in name -- {name}'.format(
            name=name,
        ))
        raise e
