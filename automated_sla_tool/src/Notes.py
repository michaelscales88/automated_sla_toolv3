from datetime import datetime


class Notes(object):
    def __init__(self):
        self.__counter = 0
        self.__dict = {0: "Notes"}

    def __getitem__(self, key):
        return self.__dict[key]

    def add_time_note(self, note):
        self.__dict[self.__counter + 1] = note
        self.__counter += 1
        return r'{0}'.format(self.__counter)

    def print_notes(self):
        for (k, v) in self.__dict.items():
            print('k: {0} v: {1}'.format(k, v))

    def pop(self, key):
        return self.__dict.pop(key)

    def get_notes(self):
        return [[r'{0} {1}'.format(k, v)] for (k, v) in self.__dict.items()]
