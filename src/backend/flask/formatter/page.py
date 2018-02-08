def create(results, args):
    return {
        'id': results[0],
    }


def read(results, args):
    if results:
        page, mirrors = results
        return {
            'id': page[0],
            'chapter_id': page[1],
            'sort_key': page[2],
            'file_name': page[3],
            'time_created': page[4],
            'time_updated': page[5],
            'mirrors': [m[0] for m in mirrors]
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
    res = {}
    for row in results:
        if row[0] not in res:
            res[row[0]] = {
                'id': row[0],
                'sort_key': row[1],
                'mirrors': [],
            }
        res[row[0]]['mirrors'].append(row[2])
    res = sorted(res.values(), key=lambda x: x['sort_key'])
    return res
