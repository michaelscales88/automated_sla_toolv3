import wave
from os.path import join
from re import search, M, I, DOTALL
from collections import defaultdict
from datetime import datetime, timedelta
from pyexcel import Book

from automated_sla_tool.src.ImapConnection import ImapConnection
from automated_sla_tool.src.AudioTranscription import AudioTranscription as Scribe
from automated_sla_tool.src.utilities import valid_dt


def get_email_data(parent=None):
    if parent and parent.__class__.__name__ == 'SlaReport':
        conn = SlaSrcHunter(None, parent)
        conn.go_to_box('Inbox')
        print(conn.get_f_list(parent.dates, parent.req_src_files))
        print(conn.get_vm(parent.dates))
    # try:
    #     unverified_payload = _read_f_data(f_path=src_f)
    # except (FileNotFoundError, TypeError):
    #     conn = SlaSrcHunter(settings, parent)
    #     conn.go_to_box('Inbox')
    #     return conn.get_vm()
    #     # rtn = conn.all_ids(datetime.today().date() - timedelta(days=1))
    #     # print(rtn)
    #     # rtn = conn.get_f_list(datetime.today().date() - timedelta(days=1),
    #     #                       'FROM "Chronicall Reports"',
    #     #                       ['Realtime Feature Trace', 'All Group Abandoned', 'All Call Details'])
    #     # a_scribe = Scribe()
    #     # for subject in rtn.keys():
    #     #     payload = rtn[subject]['payload']
    #     #     for text in a_scribe.transcribe([obj.name for obj in payload.values() if not isinstance(obj, Book)]):
    #     #         print(text)
    #         # for obj in payload.keys():
    #         #     print('My payload is: {obj} {o_type}'.format(obj=payload[obj], o_type=type(payload[obj])))
    # else:
    #     pass


def _read_f_data(f_path):
    rtn_stuff = {}
    with open(f_path) as f:
        for item in f.readlines():
            row_name, *args = item.strip().split(',')
            line = rtn_stuff.get(row_name, [])
            line.extend([item for item in args])
            rtn_stuff[row_name] = line
    return rtn_stuff


def _write_f_data(data, f_path):
    with open(f_path, 'w') as f:
        for row_name, row_data in data.items():
            f.write(
                '{row_name}, {row_data}\n'.format(row_name=row_name,
                                                  row_data=','.join(row_data))
            )


class SlaSrcHunter(ImapConnection):

    @staticmethod
    def tokenize(full_string, pivot):  # create settings option which creates an OrdDict that executes instructions
        if full_string:
            search_object = search('\(([^()]+)\)', full_string, M | I | DOTALL)
            try:
                val1, val2 = search_object.groups()[0].split(pivot)
            except AttributeError:
                val1 = val2 = False
            return val1, val2

    def get_f_list(self, on, f_list):
        payload = {}
        ids = super().get_ids(on, 'FROM "Chronicall Reports"')
        for f in f_list:
            payload[f] = ids.get(f, None)
        return payload

    def get_vm(self, on):
        payload = {}
        ids = super().get_ids(on, 'FROM "vmpro@mindwireless.com"')
        for k, v in ids.items():
            phone_number, client_name = self.tokenize(v.pop('subject', None), pivot=' > ')
            if client_name:
                client_data = payload.get(client_name, [])
                a_vm = {
                    'phone_number': phone_number,
                    'time': valid_dt(v['dt'])
                }
                client_data.append(a_vm)
                payload[client_name] = client_data
        return payload

    def date(self, on):
        if isinstance(on, datetime):
            on = on.strftime("")