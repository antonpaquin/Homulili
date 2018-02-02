from copy import deepcopy
import re


def required(template):
    res = deepcopy(template)
    res['required'] = True
    if 'default' in res:
        del res['default']
    return res


def guess_bool(res):
    if res is None:
        return None

    if res in {
        'True', 'true', 'T', 't', '1', 1, 'Y', 'y', 'Yes', 'yes',
    }:
        return True

    if res in {
        'False', 'false', 'F', 'f', '0', 0, 'N', 'n', 'No', 'no',
    }:
        return False

    return None


# url_regex = "http[s]?://([\w]*\.){1,2}([\w]*)(\/[\w%.&?+!~-]+)*"
url_regex = 'http[s]?://manga.madokami.al/.*\.zip'
