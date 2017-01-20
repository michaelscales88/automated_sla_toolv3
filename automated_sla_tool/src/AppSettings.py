from configobj import ConfigObj
from os import listdir, getcwd
from os.path import join, isdir, dirname, abspath
from functools import reduce


class AppSettings(ConfigObj):

    def __init__(self, app=None, settings_file=None):
        if app or settings_file:
            self._my_app = app
            super().__init__(settings_file if settings_file else self.settings_file,
                             create_empty=True)
        else:
            raise SystemError('No application for AppSettings')

    @property
    def settings_file(self):
        return join(self.settings_directory, '{f_name}.ini'.format(f_name=self._my_app.__class__.__name__))

    @property
    def settings_directory(self):
        settings_dir = None
        for part in listdir(dirname(abspath(__package__)) if __package__ else getcwd()):
            if isdir(part) and 'settings' in listdir(part):
                settings_dir = part
                break
        if settings_dir:
            return join(getcwd(), settings_dir, 'settings')
        else:
            raise SystemError('No settings directory found '
                              'for AppSettings:\n{app}'.format(app=self._my_app.__class__.__name__))

    def setting(self, *keys):
        try:
            return reduce(dict.__getitem__, keys, self)
        except (KeyError, TypeError):
            print('Could not find settings: {settings}'.format(settings=keys))


