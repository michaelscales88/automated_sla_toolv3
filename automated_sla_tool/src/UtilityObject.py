from os import makedirs


class UtilityObject(object):

    @staticmethod
    def str_to_bool(bool_str):
        if type(bool_str) is bool:
            return bool_str
        elif bool_str in ('True', 'TRUE', 'true'):
            return True
        elif bool_str in ('False', 'false', 'FALSE'):
            return False
        else:
            raise ValueError("Cannot covert {} to a bool".format(bool_str))

    @staticmethod
    def get_sec(time_string):
        try:
            h, m, s = [int(float(i)) for i in time_string.split(':')]
        except TypeError:
            return 0
        except ValueError:
            try:
                h, m = [int(float(i)) for i in time_string.split(':')]
                s = 0
            except ValueError:
                return 0
        return UtilityObject.convert_sec(h, m, s)

    @staticmethod
    def convert_sec(h, m, s):
        return (3600 * int(h)) + (60 * int(m)) + int(s)

    @staticmethod
    def convert_time_stamp(convert_seconds):
        minutes, seconds = divmod(convert_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return r"{0}:{1:02d}:{2:02d}".format(hours, minutes, seconds)

    @staticmethod
    def make_dir(the_dir):
        makedirs(the_dir, exist_ok=True)
