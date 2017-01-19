from os.path import join
from re import search, M, I, DOTALL
from collections import defaultdict

from automated_sla_tool.src.EmailGetter import EmailGetter
from automated_sla_tool.src.utilities import valid_dt


def get_email(report, get='Email Src Settings'):
    email_data = report.settings.get(get, None)
    if not email_data:
        print('No settings for {report}'.format(report=report.__class__.__name__))
    else:
        src_files = report.settings('req_src_files', None)
        if src_files:
            EmailHunter(report.dates, email_data['Login Info']).dl_f_list(f_list=src_files, tgt_dir=report.src_doc_path)


def get_vm(report, get='Voice Mail Data'):
    vm_data = report.settings.get(get, None)
    if not vm_data:
        print('No settings for {report}'.format(report=report.__class__.__name__))
    else:
        verified_data = {}
        # check_data = {}
        try:
            f_fmt_info = vm_data.get('File Fmt Info', None)
            f_path = join(
                report.src_doc_path,
                f_fmt_info['f_fmt'].format(file_fmt=report.dates.strftime(f_fmt_info['string_fmt']),
                                           f_ext=f_fmt_info['f_ext'])
            )
        except TypeError:
            print('Incorrect email settings for {report} {type}'
                  'Modifications can be made in /settings'.format(report=report.__class__.__name__,
                                                                  type=get))
        else:

            try:
                verified_data = _read_f_data(f_path)
            except FileNotFoundError:
                try:
                    raw_data = EmailHunter(report.dates, vm_data['Login Info']).return_vm_data()
                except KeyError:
                    from traceback import format_exc
                    from time import sleep
                    sleep(1)
                    print(format_exc())
                else:
                    verified_data, check_data = report.modify_vm(raw_data)
                    _write_f_data(verified_data, f_path)
        # print('verified dataa')
        # print(verified_data)
        # print(check_data)
        # print(type(check_data))
        # raw_list_indexed = {}
        # for client, data in verified_data.items():
        #     # print(client)
        #     # print(data)
        #     for item in data:
        #         raw_list_indexed[item] = {'call_id': item,
        #                                   'client': client}
        #
        # for client, data in check_data.items():
        #     print(client)
        #     for call in data:
        #         if call['call_id'] in raw_list_indexed:
        #             print('found call: {call}'.format(call=call['call_id']))
        #         else:
        #             print('not found call: {call}'.format(call=call['call_id']))
        # for call in data:
        #         raw_list_indexed[call['call_id']] = call
        # for client in verified_data:
        #     for call in client:
        #         if call in raw_list_indexed:
        #             print('found')
        #             print(call)
        #         else:
        #             print('not found')
        #             print(call)


        # for item in check_data.keys():
        #     data_list = verified_data.get(item, [])
        #     raw_list = check_data[item]
        #
        #     for call in raw_list:
        #         raw_list_indexed[call['call_id']] = call
        #     if data:
        #         for call in data:
        #             if call in check_data[item]:
        #                 print('call found')
        #                 print(call)
        #             else:
        #                 print('not found')
        #                 print(call)
        # print('count: {count}'.format(count=len([value for client, value in verified_data.items()])))
        return verified_data


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


class EmailHunter(EmailGetter):
    def __init__(self, date, login_info):
        print('inside EmailHunter')
        super().__init__(use_date=date, login_type=login_info['login_type'])
        self.login(username=login_info['user_name'], password=login_info['pw'])
        self.go_to_box("Inbox")

    def return_vm_data(self):
        return self.get_vm_dict(self.read_ids())

    def tokenize(self, full_string, pivot):  # create settings option which creates an OD that executes instructions
        raw_subject_line, raw_date_string = full_string.split(pivot[0])
        dt_token = valid_dt(raw_date_string)
        search_object = search('\(([^()]+)\)', raw_subject_line, M | I | DOTALL)
        try:
            val1, val2 = search_object.groups()[0].split(pivot[1])
        except AttributeError:
            val1 = val2 = False
        return dt_token, val1, val2

    def get_vm_dict(self, all_emails):
        voice_mails = defaultdict(list)
        for subject_line in all_emails:
            dt_token, phone_number, client_name = self.tokenize(subject_line, pivot=(', ', ' > '))
            if client_name:
                client_data = voice_mails.get(client_name, [])
                a_vm = {
                    'phone_number': phone_number,
                    'time': dt_token
                }
                client_data.append(a_vm)
                voice_mails[client_name] = client_data
        return voice_mails

    def dl_f_list(self, f_list, tgt_dir=None, on_time=None):
        super().dl_f_list(f_list, tgt_dir)
