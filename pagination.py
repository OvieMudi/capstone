from flask import request

ITEMS_PER_PAGE = 10


def paginate_results(results):
    'Paginate list of results'
    page = request.args.get('page', 1, int)
    start = (page - 1) * ITEMS_PER_PAGE
    end = start + ITEMS_PER_PAGE

    return results[start:end]
