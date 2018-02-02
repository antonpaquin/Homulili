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
            'time_created': results[4],
            'time_updated': results[5],
            'state': results[6],
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
            'time_created': results[4],
            'time_updated': results[5],
            'state': results[6],
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
            'state': row[3],
        }
        for row in results
    ]
    return res
