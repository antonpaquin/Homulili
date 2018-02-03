def create(results, args):
    return {
        'new_key': results,
    }


def read(results, args):
    if results:
        return {
            'api_key': results[0],
            'permissions': {
                'create': results[1],
                'read': results[2],
                'update': results[3],
                'delete': results[4],
                'index': results[5],
                'command': results[6],
                'admin': results[7],
            },
        }
    else:
        return None


def update(results, args):
    if results:
        return {
            'api_key': results[0],
            'permissions': {
                'create': results[1],
                'read': results[2],
                'update': results[3],
                'delete': results[4],
                'index': results[5],
                'command': results[6],
                'admin': results[7],
            },
        }
    else:
        return None


def delete(results, args):
    return results
