from datetime import timedelta
from json import dumps


from automated_sla_tool.src.ReportUtilities import ReportUtilities


class DataCenter(object):

    # TODO needs some form of transaction log/manifest
    # TODO push all Report loading and preparing into DataCenter
    # Reports should be able to request data and have DataCenter prepare and make available
    def __init__(self):
        # this would actually be a dB
        self.json_layer = {}
        self._doc = None
        self.util = ReportUtilities()
    
    @property
    def doc(self):
        return self._doc
        
    @doc.setter
    def doc(self, doc):
        if self.doc is None:
            self._doc = doc
            for sheet_name in doc.sheet_names():
                self.get_data(sheet_name)

    def cache(self, key):
        return {
            'Call Duration': sum([item for item in self.doc[key].column['Event Duration'] if isinstance(item, timedelta)],
                                 timedelta(0)),
            'Start Time': min(self.doc[key].column['Start Time']),
            'End Time': max(self.doc[key].column['End Time']),
            'Answered': 'Talking' in self.doc[key].column['Event Type'],
            'Talking Duration': sum(
                [e_time for e_type, e_time in
                 zip(self.doc[key].column['Event Type'], self.doc[key].column['Event Duration']) if
                 e_type == 'Talking' and isinstance(e_time, timedelta)],
                timedelta(0)
            ),
            'Receiving Party': self.util.phone_number(self.doc[key].column['Receiving Party'][0]),
            'Calling Party': self.util.phone_number(self.doc[key].column['Calling Party'][0]),
            'Call Direction': 1 if self.doc[key].column['Receiving Party'][0] == 'Ringing' else 2
        }
    
    def get_data(self, key):
        try:
            data = self.json_layer[key]
        except KeyError:
            data = self.cache(key)
            self.json_layer[key] = data
        return data

    # Currently using settings file to control the extension for saving
    # TODO beef this up to identify the extension type from the file type
    def save(self, file, full_path):
        try:
            file.save_as(filename=full_path)
        except FileNotFoundError:
            self.util.make_dir(
                self.util.dir(full_path)
            )
            file.save_as(filename=full_path)
        except OSError:
            print('encountered an issue saving the file')

    def dispatch(self, file):
        self.util.start(report=file)

    def __repr__(self):
        return str(dumps(self.json_layer, indent=4, default=self.util.datetime_handler))

    def print_record(self, record):
        print(dumps(record, indent=4, default=self.util.datetime_handler))

    # TODO Modify this to use the __iter__ for the current src
    # e.g. return <current doc>.__iter__()
    def __iter__(self):
        for key, data in sorted(self.json_layer.items()):
            yield key, data
