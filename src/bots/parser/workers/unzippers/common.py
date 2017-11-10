import re


def guess_chapter(filename):
    try:
        cname = re.search('[cC][0-9]+', filename).group()
        return int(cname[1:])
    except Exception:
        pass

    print(filename)
    raise Exception


def get_number(name):
    try:
        return int(re.search('[0-9]+', name).group())
    except Exception:
        pass

    print(name)
    raise Exception
