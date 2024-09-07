import itertools


def chunked_iterable(iterable: list, size) -> itertools.islice:
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk
