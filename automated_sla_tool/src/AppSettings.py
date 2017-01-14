from configobj import ConfigObj
from os import listdir, getcwd
from os.path import join, isdir, dirname, abspath


class AppSettings(ConfigObj):

    def __init__(self, app=None):
        if not app:
            raise SystemError('No application for AppSettings')
        else:
            self._my_app = app
            super().__init__(self.settings_file, create_empty=True)

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
