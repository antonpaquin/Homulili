def create(results, args):
    return {
        'id': results[0],
    }


def read(results, args):
    if results:
        return {
            'id': results[0],
            'manga_id': results[1],
            'url': results[2],
            'location': results[3],
            'downloaded': results[4],
            'ignore': results[5],
            'time_created': results[6],
            'time_updated': results[7],
            'parsed': results[8],
        }
    else:
        return None


def update(results, args):
    if results:
        return {
            'id': results[0],
            'manga_id': results[1],
            'url': results[2],
            'location': results[3],
            'downloaded': results[4],
            'ignore': results[5],
            'parsed': results[8],
            'time_created': results[6],
            'time_updated': results[7],
        }
    else:
        return None


def delete(results, args):
    return results


def index(results, args):
    res = [
        {
            'id': row[0],
            'url': row[1],
            'location': row[2],
            'downloaded': row[3],
            'ignore': row[4],
            'parsed': row[5],
        }
        for row in results
    ]
    return res
