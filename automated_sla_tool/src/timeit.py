from datetime import datetime


def timeit(f):
    def timed(*args, **kw):

        ts = datetime.now()
        result = f(*args, **kw)
        te = datetime.now()
        print('Started {fn} at {t1}'.format(fn=f.__name__,
                                            t1=ts.time()))
        print('Stopped {fn} at {t2}'.format(fn=f.__name__,
                                            t2=te.time()))
        print('func:{0} args:[{1}, {2}] took: {3} sec'.format(f.__name__, args, kw, te-ts))
        return result
    return timed
