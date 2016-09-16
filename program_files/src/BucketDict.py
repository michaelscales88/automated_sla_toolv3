class BetweenDict(dict):
    def __init__(self, d):
        super().__init__()
        for k, v in d.items():
            self[k] = v

    def __getitem__(self, key):
        for k, v in self.items():
            if k[0] < key <= k[1]:
                return v
        raise KeyError("Key '%s' is not between any values in the BetweenDict" % key)

    def __setitem__(self, key, value):
        try:
            if len(key) == 2:
                if key[0] < key[1]:
                    dict.__setitem__(self, (key[0], key[1]), value)
                else:
                    raise RuntimeError('First element of a BetweenDict key '
                                       'must be strictly less than the '
                                       'second element')
            else:
                raise ValueError('Key of a BetweenDict must be an iterable with length two')
        except TypeError:
            raise TypeError('Key of a BetweenDict must be an iterable with length two')

    def __contains__(self, key):
        try:
            return bool(self[key]) or True
        except KeyError:
            return False

    def add_range_item(self, key, found=None):
        # TODO: This seems inefficient looping through here + in __getitem__
        for k in self.keys():
            if k[0] < key <= k[1]:
                dict.__setitem__(self, (k[0], k[1]), self[key] + 1)
                found = True
        if not found:
            raise KeyError("Key '%s' is not between any values in the BetweenDict" % key)
