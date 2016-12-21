import inspect
from automated_sla_tool.src.FinishedDecorator import FinishedDecorator as check_set
from automated_sla_tool.src.stacked_traceback_decorator import stacked_traceback_decorator as tb_decorator
from automated_sla_tool.src.for_all_methods_decorator import for_all_methods_decorator as decorate_all


@decorate_all(decorator=tb_decorator)
class GenericUi(object):

    obj_set = False

    def __init__(self, exclusions=None):
        super().__init__()
        self._finished = False
        self._obj = None
        self._ui = None
        self._exclusions = ['__init__', exclusions]

    def run(self):
        while not self.finished:
            self.display_ui()

    @property
    def finished(self):
        return self._finished

    @property
    def object(self):
        return self._obj

    @object.setter
    @check_set(obj_set)
    def object(self, raw_obj):
        obj = raw_obj
        obj_ui = {
            **dict(inspect.getmembers(obj, predicate=inspect.ismethod)),
            **{'Quit': self.exit}
        }
        for e in self._exclusions:
            obj_ui.pop(e, None)
        self._obj = obj
        self._ui = obj_ui
        GenericUi.obj_set = True

    def clear_obj(self):
        self._obj = None
        self._ui = None
        GenericUi.obj_set = False

    def display_ui(self):
        return self.exc_fnc()

    def exc_fnc(self):
        selection = dict(enumerate(sorted(self._ui.keys()), start=1))
        self.display_selection(selection)
        func = self._ui[selection[int(input('Make a selection: '))]]
        return func()

    def exit(self):
        self._finished = True

    def display_selection(self, selection):
        print('GenericUI: {0}'.format(self._obj), flush=True)
        print("\n".join(['{k}: {v}'.format(k=k, v=v) for k, v in sorted(selection.items())]))

    def __del__(self):
        print('quitting')
