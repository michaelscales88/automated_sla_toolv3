import sys
import functools


class MyError(Exception):
    pass


def stacked_traceback_decorator(fn):
    @functools.wraps(fn)
    def decorated(*args, **kwargs):
        try:
            fn(*args, **kwargs)
        except Exception as e:
            et, ei, tb = sys.exc_info()
            raise MyError(e).with_traceback(tb)
    return decorated
