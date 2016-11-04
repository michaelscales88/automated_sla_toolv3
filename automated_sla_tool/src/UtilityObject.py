import os


class UtilityObject:
    def __init__(self):
        pass

    def str_to_bool(self, bool_str):
        if type(bool_str) is bool:
            return bool_str
        elif bool_str in ('True', 'TRUE', 'true'):
            return True
        elif bool_str in ('False', 'false', 'FALSE'):
            return False
        else:
            raise ValueError("Cannot covert {} to a bool".format(bool_str))

    def get_sec(self, time_string):
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
        return self.convert_sec(h, m, s)

    def convert_sec(self, h, m, s):
        return (3600 * int(h)) + (60 * int(m)) + int(s)

    def convert_time_stamp(self, convert_seconds):
        minutes, seconds = divmod(convert_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "{0}:{1:02d}:{2:02d}".format(hours, minutes, seconds)

    def change_dir(self, the_dir):
        try:
            os.chdir(the_dir)
        except FileNotFoundError:
            try:
                os.makedirs(the_dir, exist_ok=True)
                os.chdir(the_dir)
            except OSError:
                pass
