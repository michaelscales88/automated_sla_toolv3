from collections import OrderedDict


from automated_sla_tool.src.FnLib import FnLib


class DataWorker(object):

    def __init__(self):
        self.fn_lib = FnLib()

    @staticmethod
    def my_business(obj):
        try:
            return obj.settings['JSON'].items()
        except AttributeError:
            return False

    @staticmethod
    def bind_keyword(keywords, bindings):
        return dict(zip(keywords.split(':'), bindings.split(':')))

    def prepare(self, obj):
        parsed_cmds = OrderedDict()
        for key, values in DataWorker.my_business(obj):
            parsed_cmds[key] = self._link(*values)
        else:
            print('in else')
        return parsed_cmds

    def _link(self, *words):
        fn = self.fn_lib[words[0]]
        parameters = DataWorker.bind_keyword(words[1], words[2])
        behavior = words[3:]
        return {'fn': fn, 'parameters': parameters, 'behavior': behavior}
