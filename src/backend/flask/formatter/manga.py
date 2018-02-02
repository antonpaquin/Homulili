def create(results, args):
    return {
        'id': results[0],
    }


def read(results, args):
    if results:
        return {
            'id': results[0],
            'name': results[1],
            'author': results[2],
            'madokami_url': results[3],
            'active': results[4],
            'time_created': results[5],
            'time_updated': results[6],
        }
    else:
        return None


def update(results, args):
    if results:
        return {
            'id': results[0],
            'name': results[1],
            'author': results[2],
            'madokami_url': results[3],
            'active': results[4],
            'time_created': results[5],
            'time_updated': results[6],
        }
    else:
        return None


def delete(results, args):
    return results


def index(results, args):
    res = []
    for row in results:
        res.append({
            'id': row[0],
            'name': row[1]
        })

    return res

