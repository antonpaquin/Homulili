def create(results, args):
    return {
        'id': results[0],
    }


def read(results, args):
    if results:
        return {
            'id': results[0],
            'chapter_id': results[1],
            'sort_key': results[2],
            'file_name': results[3],
            'time_created': results[4],
            'time_updated': results[5],
        }
    else:
        return None


def update(results, args):
    if results:
        return {
            'id': results[0],
            'chapter_id': results[1],
            'sort_key': results[2],
            'file_name': results[3],
            'time_created': results[4],
            'time_updated': results[5],
        }
    else:
        return None


def delete(results, args):
    return results


def index(results, args):
    res = [
        {
            'id': row[0],
            'sort_key': row[1],
        }
        for row in results
    ]
    res.sort(key=lambda x: x['sort_key'])
    return res
