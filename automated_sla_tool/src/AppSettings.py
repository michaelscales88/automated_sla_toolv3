from configobj import ConfigObj
from os.path import join, dirname
from functools import reduce


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

    def format_settings(self, v=None, date=None):
        format_list = self.setting('Date Formats')
        for k, v in (v if v else self).items():
            if hasattr(v, 'items'):
                self.format_settings(v=v, date=date)
            else:
                try:
                    for fmt in format_list:
                        print(fmt)
                        print(format_list[fmt])
                        curr_setting = self.setting(k)
                        print(curr_setting)
                        try:
                            curr_setting.format(fmt=date.strftime(format_list[fmt]))
                        except KeyError:
                            pass
                except KeyError:
                    from time import sleep
                    sleep(1)
                    raise
                # print('trying to format: ')
                # print(k)
