from configobj import ConfigObj
from os.path import join, dirname
from functools import reduce


class AppSettings(ConfigObj):

    def __init__(self, app=None, settings_file=None):
        if app or settings_file:
            self._my_app = app
            super().__init__(settings_file if settings_file else self.settings_file,
                             create_empty=True)
            self.init_keywords()
            self.apply_custom_format(lvl=self)
        else:
            raise SystemError('No application or settings for AppSettings')

    @property
    def settings_file(self):
        return join(self.settings_directory, '{f_name}.ini'.format(f_name=self._my_app.__class__.__name__))

    @property
    def settings_directory(self):
        return join(dirname(dirname(__file__)), 'settings')

    def setting(self, *keys, rtn_val=()):
        try:
            rtn_val = reduce(dict.__getitem__, keys, self)
        except (KeyError, TypeError):
            print('Could not find settings: {settings}'.format(settings=keys))
        return rtn_val

    # TODO this needs better logic since my_app is being used for ImapConnection and SlaReport. Ea. has diff 2nd cond
    def init_keywords(self):
        try:
            if self._my_app and self._my_app.interval:
                for k, v in self.setting('Keyword Formats', rtn_val={}).items():
                    self['Keyword Formats'][k] = self._my_app.interval.strftime(v)
        except AttributeError:
            pass

    # TODO this is not working as intended. should go to nth depth, but is going to n - 1
    def __iter__(self, v=None):
        for kvl, vvl in (v if v else self).items():
            if hasattr(vvl, 'items'):
                self.__iter__(v=vvl)
            else:
                yield kvl, vvl

    def apply_custom_format(self, lvl=None):
        for k, v in lvl.items():
            if hasattr(v, 'items'):
                self.apply_custom_format(lvl=v)
            else:
                try:
                    lvl[k] = v.format(**self.setting('Keyword Formats', rtn_val={}))
                except (AttributeError, KeyError):
                    pass
