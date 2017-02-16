from configobj import ConfigObj
from os.path import join, dirname
from functools import reduce
from datetime import datetime


class AppSettings(ConfigObj):

    def __init__(self, app=None, settings_file=None):
        if app or settings_file:
            self._my_app = app
            super().__init__(settings_file if settings_file else self.settings_file,
                             create_empty=True)
            self.format_settings()
        else:
            raise SystemError('No application for AppSettings')

    @property
    def settings_file(self):
        return join(self.settings_directory, '{f_name}.ini'.format(f_name=self._my_app.__class__.__name__))

    @property
    def settings_directory(self):
        return join(dirname(dirname(__file__)), 'settings')

    def setting(self, *keys):
        try:
            return reduce(dict.__getitem__, keys, self)
        except (KeyError, TypeError):
            print('Could not find settings: {settings}'.format(settings=keys))

    # TODO this is not working as intended. should go to nth depth, but is missing depth - 1
    def __iter__(self, v=None):
        for k, v in (v if v else self).items():
            if hasattr(v, 'items'):
                # print('diving deeper')
                # print(v)
                self.__iter__(v=v)
            else:
                # print('k {}'.format(k))
                # print('v {}'.format(v))
                yield k, v

    def format_settings(self, date=None):
        format_list = self.setting('Date Formats')
        date = datetime.today()
        for label, value in self:
            if label == 'file_fmt':
                print('label {}'.format(label))
                print('value {}'.format(value))
                # print('checking formats')
            for fmt in format_list:
                if label == 'file_fmt':
                    print(fmt)
                    print(format_list[fmt])
                    # print(date.strftime(format_list[fmt]))
                try:
                    print(value.format(fmt=date.strftime(format_list[fmt])))
                except KeyError:
                    print('keyerror')
                    print(fmt)
                    print(format_list[fmt])
                    print(date.strftime(format_list[fmt]))
                except AttributeError:
                    pass
                else:
                    print(value)
                    # for item in value:
                    #     print(item)
                # self[label] = value.format(fmt=date.strftime(format_list[fmt]))
            # print(self[label])
