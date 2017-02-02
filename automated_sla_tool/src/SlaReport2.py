import operator
from datetime import time, timedelta, date
from dateutil.parser import parse
from collections import defaultdict, OrderedDict, namedtuple
from os.path import join, isfile
from pyexcel import get_sheet

from automated_sla_tool.src.BucketDict import BucketDict
from automated_sla_tool.src.AReport2 import AReport
from automated_sla_tool.src.EmailHunter import get_vm
from automated_sla_tool.src.utilities import valid_dt


# TODO Add feature to run report without call pruning. Ex. Call spike days where too many duplicates are removed


class SlaReport(AReport):
    def __init__(self, report_date=None):
        super().__init__(report_dates=report_date)
        if self.check_finished(sub_dir=self._settings['sub_dir_fmt'],
                               report_string=self._settings['file_fmt']):
            print('Report Complete for {date}'.format(date=self.dates))
        else:
            print('Building a report for {date}'.format(date=self.dates))
            self.req_src_files = [item.format(date=self.dates.strftime(self._settings['vm_fmt']))
                                  for item in self._settings['req_src_files']]
            self.load_and_prepare()
            self.sla_report = {}

            self.norm_day = self.day_of_wk not in (5, 6)

            self.orphaned_voicemails = None
            self.src_files[r'Voice Mail'] = defaultdict(list)
            self.get_voicemails()

    '''
    UI Section
    '''

    @property
    def settings(self):
        return self._settings

    def run(self):
        if self.fr.finished:
            return
        else:
            self.extract_report_information()
            self.process_report()
            self.save_report()

    def manual_input(self):
        input_opt = OrderedDict(
            [
                ('-4 Days', -4),
                ('-3 Days', -3),
                ('-2 Days', -2),
                ('Yesterday', -1)
            ]
        )
        return date.today() + timedelta(days=self.return_selection(input_opt))

    def load_and_prepare(self):
        super().load_documents()
        call_details_filters = [
            self.inbound_call_filter,
            self.zero_duration_filter,
            self.remove_internal_inbound_filter
        ]
        self.src_files[r'Call Details (Basic)'] = self.collate_wb_to_sheet(wb=self.src_files[r'Call Details (Basic)'])
        self.apply_formatters_to_sheet(sheet=self.src_files[r'Call Details (Basic)'],
                                       filters=call_details_filters)
        self.src_files[r'Call Details (Basic)'].name = 'call_details'
        self.compile_call_details()

        self.src_files[r'Group Abandoned Calls'] = self.collate_wb_to_sheet(wb=self.src_files[r'Group Abandoned Calls'])
        self.apply_formatters_to_sheet(sheet=(self.src_files[r'Group Abandoned Calls']),
                                       one_filter=self.answered_filter)
        self.src_files[r'Group Abandoned Calls'].name = 'abandon_grp'
        self.scrutinize_abandon_group()

        # self.src_files[r'Voice Mail'] = get_vm(self)
        # print(self.src_files[r'Voice Mail'])

    def extract_report_information(self):
        if self.fr.finished:
            return
        else:
            ans_cid_by_client = self.group_cid_by_client(self.src_files[r'Call Details (Basic)'])
            lost_cid_by_client = self.group_cid_by_client(self.src_files[r'Group Abandoned Calls'])
            for client_name, client_num, full_service in [(client,
                                                           int(values['client_num']),
                                                           self.str_to_bool(values['full_service']))
                                                          for client, values in self._settings['Clients'].items()]:
                self.sla_report[client_num] = Client(
                    name=client_num,
                    answered_calls=ans_cid_by_client.get(client_num, []),
                    lost_calls=lost_cid_by_client.get(client_num, []),
                    voicemail=self.src_files[r'Voice Mail'].get(client_name, []),
                    full_service=full_service
                )
                if not self.sla_report[client_num].is_empty():
                    # TODO this could perhaps be a try: ... KeyError...
                    if self.sla_report[client_num].no_answered() is False:
                        self.sla_report[client_num].extract_call_details(self.src_files[r'Call Details (Basic)'])
                    if self.sla_report[client_num].no_lost() is False:
                        self.sla_report[client_num].extract_abandon_group_details(
                            self.src_files[r'Group Abandoned Calls'])

    def process_report(self):
        if self.fr.finished:
            return
        else:
            headers = [self.dates.strftime('%A %m/%d/%Y'), 'I/C Presented', 'I/C Answered', 'I/C Lost', 'Voice Mails',
                       'Incoming Answered (%)', 'Incoming Lost (%)', 'Average Incoming Duration',
                       'Average Wait Answered',
                       'Average Wait Lost', 'Calls Ans Within 15', 'Calls Ans Within 30', 'Calls Ans Within 45',
                       'Calls Ans Within 60', 'Calls Ans Within 999', 'Call Ans + 999', 'Longest Waiting Answered',
                       'PCA']
            self.fr.row += headers
            self.fr.name_columns_by_row(0)
            total_row = dict((value, 0) for value in headers[1:])
            total_row['Label'] = 'Summary'
            for client_name, client_num in [(client, int(values['client_num']))
                                            for client, values in self._settings['Clients'].items()
                                            if self.str_to_bool(values['full_service']) or self.norm_day]:
                num_calls = self.sla_report[client_num].get_number_of_calls()
                this_row = dict((value, 0) for value in headers[1:])
                this_row['I/C Presented'] = sum(num_calls.values())
                this_row['Label'] = '{num} {name}'.format(num=client_num, name=client_name)
                if this_row['I/C Presented'] > 0:
                    ticker_stats = self.sla_report[client_num].get_call_ticker()
                    this_row['I/C Answered'] = num_calls['answered']
                    this_row['I/C Lost'] = num_calls['lost']
                    this_row['Voice Mails'] = num_calls['voicemails']
                    this_row['Incoming Answered (%)'] = (num_calls['answered'] / this_row['I/C Presented'])
                    this_row['Incoming Lost (%)'] = (
                        (num_calls['lost'] + num_calls['voicemails']) / this_row['I/C Presented'])
                    this_row['Average Incoming Duration'] = self.sla_report[client_num].get_avg_call_duration()
                    this_row['Average Wait Answered'] = self.sla_report[client_num].get_avg_wait_answered()
                    this_row['Average Wait Lost'] = self.sla_report[client_num].get_avg_lost_duration()
                    this_row['Calls Ans Within 15'] = ticker_stats[15]
                    this_row['Calls Ans Within 30'] = ticker_stats[30]
                    this_row['Calls Ans Within 45'] = ticker_stats[45]
                    this_row['Calls Ans Within 60'] = ticker_stats[60]
                    this_row['Calls Ans Within 999'] = ticker_stats[999]
                    this_row['Call Ans + 999'] = ticker_stats[999999]
                    this_row['Longest Waiting Answered'] = self.sla_report[client_num].get_longest_answered()
                    try:
                        this_row['PCA'] = ((ticker_stats[15] + ticker_stats[30]) / num_calls['answered'])
                    except ZeroDivisionError:
                        this_row['PCA'] = 0

                    self.accumulate_total_row(this_row, total_row)
                    self.add_row(this_row)
                else:
                    self.add_row(this_row)
            self.finalize_total_row(total_row)
            self.add_row(total_row)
            self.fr.name_rows_by_column(0)

    def save_report(self):
        if self.fr.finished:
            return
        else:
            # TODO build this into manifest E.g. tgt delivery
            self.validate_final_report()
            super().save(user_string=self._settings['file_fmt'],
                         sub_dir=self._settings['sub_dir_fmt'])
            try:
                super().save(user_string=self._settings['file_fmt'],
                             sub_dir=self._settings['sub_dir_fmt'],
                             alt_dir=self._settings['network_tgt_dir'])
            except OSError:
                print('passing os_error')

    '''
    Report Filters by row
    '''

    @staticmethod
    def blank_row_filter(row):
        result = [element for element in str(row[3]) if element != '']
        return len(result) == 0

    @staticmethod
    def answered_filter(row):
        try:
            answered = row[-5]
        except ValueError:
            answered = False
        return answered

    @staticmethod
    def inbound_call_filter(row):
        return row[0] not in ('Inbound', 'Call Direction')

    @staticmethod
    def zero_duration_filter(row):
        result = [element for element in row[-1] if element != '']
        return len(result) == 0

    @staticmethod
    def remove_internal_inbound_filter(row):
        return row[-2] == row[-3]

    '''
    SlaReport Functions
    '''

    def compile_call_details(self):
        if self.fr.finished:
            return
        else:
            hold_events = ('Hold', 'Transfer Hold', 'Park')
            additional_columns = OrderedDict(
                [
                    ('Wait Time', []),
                    ('Hold Time', [])
                ]
            )
            for row_name in self.src_files[r'Call Details (Basic)'].rownames:
                unhandled_call_data = {
                    k: 0 for k in hold_events
                }
                tot_call_duration = self.get_sec(self.src_files[r'Call Details (Basic)'][row_name, 'Call Duration'])
                talk_duration = self.get_sec(self.src_files[r'Call Details (Basic)'][row_name, 'Talking Duration'])
                call_id = row_name.replace(':', ' ')
                cradle_sheet = self.src_files[r'Cradle to Grave'][call_id]
                for event_row in cradle_sheet.rownames:
                    event_type = cradle_sheet[event_row, 'Event Type']
                    if event_type in hold_events:
                        unhandled_call_data[event_type] += self.get_sec(cradle_sheet[event_row, 'Event Duration'])
                raw_hold_time = sum(val for val in unhandled_call_data.values())
                raw_time_waited = tot_call_duration - talk_duration - raw_hold_time
                additional_columns['Hold Time'].append(self.convert_time_stamp(raw_hold_time))
                additional_columns['Wait Time'].append(self.convert_time_stamp(raw_time_waited))
            self.src_files[r'Call Details (Basic)'].extend_columns(additional_columns)

    def scrutinize_abandon_group(self):
        if self.fr.finished:
            return
        else:
            self.remove_calls_less_than_twenty_seconds()
            self.remove_non_distinct_callers()

    # TODO combine remove non-distinct and calls <20 into general filter function to remove multiple for loops
    def remove_non_distinct_callers(self):
        i_count = self.find_non_distinct(sheet=self.src_files[r'Group Abandoned Calls'], event_col='External Party')
        for dup_val, dup_call_ids in {k: reversed(sorted(v['rows']))
                                      for k, v in i_count.items() if v['count'] > 1}.items():
            for call_id in dup_call_ids:
                try:
                    prev_call = self.parse_to_sec(
                        self.src_files[r'Group Abandoned Calls'][next(dup_call_ids), 'End Time']
                    )
                except StopIteration:
                    pass  # catches attempt to iterate through last element of non-even length iterator
                else:
                    last_call = self.parse_to_sec(self.src_files[r'Group Abandoned Calls'][call_id, 'Start Time'])
                    if abs(last_call - prev_call) <= 60:
                        self.src_files[r'Group Abandoned Calls'].delete_named_row_at(call_id)

    def remove_calls_less_than_twenty_seconds(self):
        for row_name in reversed(self.src_files[r'Group Abandoned Calls'].rownames):
            call_duration = self.get_sec(self.src_files[r'Group Abandoned Calls'][row_name, 'Call Duration'])
            if call_duration < 20:
                self.src_files[r'Group Abandoned Calls'].delete_named_row_at(row_name)

    def validate_final_report(self):
        for row in self.fr.rownames:
            ticker_total = 0
            answered = self.fr[row, 'I/C Answered']
            ticker_total += self.fr[row, 'Calls Ans Within 15']
            ticker_total += self.fr[row, 'Calls Ans Within 30']
            ticker_total += self.fr[row, 'Calls Ans Within 45']
            ticker_total += self.fr[row, 'Calls Ans Within 60']
            ticker_total += self.fr[row, 'Calls Ans Within 999']
            ticker_total += self.fr[row, 'Call Ans + 999']
            if answered != ticker_total:
                raise ValueError('Validation error ->'
                                 'ticker total != answered for: '
                                 '{0}'.format(row[0]))

    def group_cid_by_client(self, report):
        report_details = defaultdict(list)
        for row_name in report.rownames:
            try:
                client = int(report[row_name, 'Internal Party'])
            except ValueError:
                client = self.handle_read_value_error(row_name)
            finally:
                report_details[client].append(row_name)
        return report_details

    def get_voicemails(self):
        file_fmt = self._settings['Voice Mail Data']['File Fmt Info']
        vm_f_path = join(
            self.src_doc_path, file_fmt['f_fmt'].format(file_fmt=self.dates.strftime(file_fmt['string_fmt']),
                                                        f_ext=file_fmt['f_ext'])
        )
        try:
            self.read_voicemail_data(vm_f_path)
        except FileNotFoundError:
            self.make_voicemail_data()
            self.write_voicemail_data(vm_f_path)

    def read_voicemail_data(self, vm_f_path):
        if isfile(vm_f_path):
            with open(vm_f_path) as f:
                content = f.readlines()
                for item in content:
                    client_info = item.replace('\n', '').split(',')
                    self.src_files[r'Voice Mail'][client_info[0]] = client_info[1:]
        else:
            raise FileNotFoundError()

    def retrieve_voicemail_emails(self):
        from automated_sla_tool.src.EmailGetter import EmailGetter
        mail = EmailGetter(self.dates, self.login_type)
        mail.login(self.user_name, self.password)
        mail.inbox()
        read_ids = mail.read_ids()
        return mail.get_voice_mail_info(read_ids)

    def modify_vm(self, inc_data):
        rtn_dict = {}
        if isinstance(inc_data, dict):
            c_vm = self.new_type_cradle_vm()
            for client_name, inc_data, c_vm in sorted(self.common_keys(inc_data, c_vm)):
                for match1, match2 in self.return_matches(inc_data, c_vm, match_val='phone_number'):
                    if abs(match1['time'] - match2['time']) < timedelta(seconds=15):
                        call_id = match1['call_id'] if match1.get('call_id', None) else match2['call_id']
                        client_info = rtn_dict.get(client_name, [])
                        client_info.append(call_id)
                        rtn_dict[client_name] = client_info
        return rtn_dict, self.new_type_cradle_vm()

    def new_type_cradle_vm(self):
        voice_mail_dict = defaultdict(list)
        for call_id_page in self.src_files[r'Cradle to Grave']:
            for row_name in call_id_page.rownames:
                row_event = call_id_page[row_name, 'Event Type']
                if 'Voicemail' in row_event:
                    receiving_party = call_id_page[row_name, 'Receiving Party']
                    if receiving_party.isalpha():
                        print('alpha {rp}'.format(rp=receiving_party))
                        # check if this is a valid client
                        pass  # should pass if client name is here
                    else:
                        print('non-alpha {rp}'.format(rp=receiving_party))
                        # should catch blanks and clients in ext fmt
                        print('need a way to fix blanks and numbers')
                    client_info = voice_mail_dict.get(receiving_party, [])
                    a_vm = {
                        'phone_number': ''.join([ch for ch in call_id_page[row_name, 'Calling Party'] if ch.isdigit()]),
                        'call_id': call_id_page.name,
                        'time': valid_dt(call_id_page[row_name, 'End Time'])
                    }
                    client_info.append(a_vm)
                    voice_mail_dict[receiving_party] = client_info
        return voice_mail_dict

    def retrieve_voicemail_cradle(self):
        voice_mail_dict = defaultdict(list)
        for call_id_page in self.src_files[r'Cradle to Grave']:
            try:
                col_index = call_id_page.colnames
                sheet_events = call_id_page.column['Event Type']
            except IndexError:
                pass
            else:
                if 'Voicemail' in sheet_events:
                    voicemail_index = sheet_events.index('Voicemail')
                    real_voicemail = call_id_page[
                                         voicemail_index, col_index.index('Receiving Party')] in self.clients_verbose
                    if real_voicemail:
                        voicemail = {}
                        receiving_party = call_id_page[voicemail_index, col_index.index('Receiving Party')]
                        telephone_number = str(call_id_page[voicemail_index, col_index.index('Calling Party')])[-4:]
                        if telephone_number.isalpha():
                            telephone_number = str(call_id_page[0, col_index.index('Calling Party')])[-4:]
                        call_time = call_id_page[voicemail_index, col_index.index('End Time')]
                        voicemail['call_id'] = call_id_page.name
                        voicemail['number'] = telephone_number
                        voicemail['call_time'] = call_time
                        voice_mail_dict[receiving_party].append(voicemail)
        return voice_mail_dict

    def make_voicemail_data(self):
        e_vm = self.retrieve_voicemail_emails()
        c_vm = self.retrieve_voicemail_cradle()
        for client, e_list in e_vm.items():
            c_list = c_vm.get(client, None)
            if c_list is None:
                self.src_files[r'Voice Mail'][client] = ['orphan-{}'.format(i.split(' + ')[0]) for i in e_list]
            else:
                for evoicemail in e_list:
                    email_number, email_time = evoicemail.split(' + ')
                    matched_call = next((l for l in c_list if l['number'] == email_number), None)
                    if matched_call is None:
                        self.src_files[r'Voice Mail'][client].append('orphan-{}'.format(email_number))
                    else:
                        email_datetime = parse(email_time)
                        cradle_datetime = parse(matched_call['call_time'])
                        difference = cradle_datetime - email_datetime
                        if difference < timedelta(seconds=31):
                            print('found a vm {call}'.format(call=matched_call['call_id']))
                            self.src_files[r'Voice Mail'][client].append(matched_call['call_id'])

    def write_voicemail_data(self, voicemail_file_path):
        text_file = open(voicemail_file_path, 'w')
        for voicemail_group in self.src_files[r'Voice Mail'].items():
            text_string = '{0},{1}\n'.format(voicemail_group[0], ",".join(voicemail_group[1]))
            text_file.write(text_string)
        text_file.close()

    '''
    Utilities Section
    '''

    @staticmethod
    def safe_div(num, denom):
        rtn_val = 0
        try:
            rtn_val = num / denom
        except ZeroDivisionError:
            pass
        return rtn_val

    def add_row(self, a_row):
        self.format_row(a_row)
        self.fr.row += self.return_row_as_list(a_row)

    def format_row(self, row):
        row['Average Incoming Duration'] = self.convert_time_stamp(row['Average Incoming Duration'])
        row['Average Wait Answered'] = self.convert_time_stamp(row['Average Wait Answered'])
        row['Average Wait Lost'] = self.convert_time_stamp(row['Average Wait Lost'])
        row['Longest Waiting Answered'] = self.convert_time_stamp(row['Longest Waiting Answered'])
        row['Incoming Answered (%)'] = '{0:.1%}'.format(row['Incoming Answered (%)'])
        row['Incoming Lost (%)'] = '{0:.1%}'.format(row['Incoming Lost (%)'])
        row['PCA'] = '{0:.1%}'.format(row['PCA'])

    @staticmethod
    def return_row_as_list(row):
        return [row['Label'],
                row['I/C Presented'],
                row['I/C Answered'],
                row['I/C Lost'],
                row['Voice Mails'],
                row['Incoming Answered (%)'],
                row['Incoming Lost (%)'],
                row['Average Incoming Duration'],
                row['Average Wait Answered'],
                row['Average Wait Lost'],
                row['Calls Ans Within 15'],
                row['Calls Ans Within 30'],
                row['Calls Ans Within 45'],
                row['Calls Ans Within 60'],
                row['Calls Ans Within 999'],
                row['Call Ans + 999'],
                row['Longest Waiting Answered'],
                row['PCA']]

    @staticmethod
    def accumulate_total_row(row, tr):
        tr['I/C Presented'] += row['I/C Presented']
        tr['I/C Answered'] += row['I/C Answered']
        tr['I/C Lost'] += row['I/C Lost']
        tr['Voice Mails'] += row['Voice Mails']
        tr['Average Incoming Duration'] += row['Average Incoming Duration'] * row['I/C Answered']
        tr['Average Wait Answered'] += row['Average Wait Answered'] * row['I/C Answered']
        tr['Average Wait Lost'] += row['Average Wait Lost'] * row['I/C Lost']
        tr['Calls Ans Within 15'] += row['Calls Ans Within 15']
        tr['Calls Ans Within 30'] += row['Calls Ans Within 30']
        tr['Calls Ans Within 45'] += row['Calls Ans Within 45']
        tr['Calls Ans Within 60'] += row['Calls Ans Within 60']
        tr['Calls Ans Within 999'] += row['Calls Ans Within 999']
        tr['Call Ans + 999'] += row['Call Ans + 999']
        if tr['Longest Waiting Answered'] < row['Longest Waiting Answered']:
            tr['Longest Waiting Answered'] = row['Longest Waiting Answered']

    @staticmethod
    def finalize_total_row(tr):
        if tr['I/C Presented'] > 0:
            tr['Incoming Answered (%)'] = operator.truediv(tr['I/C Answered'],
                                                           tr['I/C Presented'])
            tr['Incoming Lost (%)'] = operator.truediv(tr['I/C Lost'] + tr['Voice Mails'],
                                                       tr['I/C Presented'])
            tr['PCA'] = operator.truediv(tr['Calls Ans Within 15'] + tr['Calls Ans Within 30'],
                                         tr['I/C Presented'])
            if tr['I/C Answered'] > 0:
                tr['Average Incoming Duration'] = operator.floordiv(tr['Average Incoming Duration'],
                                                                    tr['I/C Answered'])
                tr['Average Wait Answered'] = operator.floordiv(tr['Average Wait Answered'],
                                                                tr['I/C Answered'])
            if tr['I/C Lost'] > 0:
                tr['Average Wait Lost'] = operator.floordiv(tr['Average Wait Lost'],
                                                            tr['I/C Lost'])

    def make_verbose_dict(self):
        return dict((value.name, key) for key, value in self.clients.items())

    def handle_read_value_error(self, call_id):
        sheet = self.src_files[r'Cradle to Grave'][call_id.replace(':', ' ')]
        hunt_index = sheet.column['Event Type'].index('Ringing')
        return sheet.column['Receiving Party'][hunt_index]

    def get_client_settings(self):
        client = namedtuple('client_settings', 'name full_service')
        settings_file = r'{0}\{1}'.format(self.path, r'settings\report_settings.xlsx')
        settings = get_sheet(file_name=settings_file, name_columns_by_row=0)
        return_dict = OrderedDict()
        is_weekend = self.dates.isoweekday() in (6, 7)
        for row in range(settings.number_of_rows()):
            is_fullservice = self.str_to_bool(settings[row, 'Full Service'])
            if is_weekend:
                if is_fullservice is True:
                    this_client = client(name=settings[row, 'Client Name'],
                                         full_service=is_fullservice)
                    return_dict[settings[row, 'Client Number']] = this_client
            else:
                this_client = client(name=settings[row, 'Client Name'],
                                     full_service=is_fullservice)
                return_dict[settings[row, 'Client Number']] = this_client
        return return_dict

    def __del__(self):
        try:
            if int(input('1 to open file: ')) is 1:
                super().open(user_string=self._settings['file_fmt'],
                             sub_dir=self._settings['sub_dir_fmt'])
        except ValueError:
            pass


class Client:
    earliest_call = time(hour=7)
    latest_call = time(hour=20)

    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.full_service = kwargs.get('full_service', False)
        self.answered_calls = kwargs.get('answered_calls', [])
        self.lost_calls = kwargs.get('lost_calls', [])
        self.voicemails = kwargs.get('voicemail', [])
        self.remove_voicemails()
        self.longest_answered = 0
        self.call_details_duration = timedelta(seconds=0)
        self.abandon_group_duration = timedelta(seconds=0)
        self.wait_answered = []
        self.call_details_ticker = BucketDict(
            {(-1, 15): 0, (15, 30): 0, (30, 45): 0, (45, 60): 0, (60, 999): 0, (999, 999999): 0}
        )

    def __str__(self):
        print('name: {}'.format(self.name))
        print('ans: {}'.format(self.answered_calls))
        print('lost: {}'.format(self.lost_calls))
        print('vm: {}'.format(self.voicemails))

    def remove_voicemails(self):
        '''
        Should never find a voicemail call since they're excluded when Call Details loads
        :return:
        '''
        for voicemail in self.voicemails:
            if voicemail in self.lost_calls:
                self.lost_calls.remove(voicemail)
            if voicemail in self.answered_calls:
                self.answered_calls.remove(voicemail)

    def is_empty(self):
        return len(self.answered_calls) == 0 and len(self.lost_calls) == 0 and len(self.voicemails) == 0

    def no_answered(self):
        return len(self.answered_calls) == 0

    def no_lost(self):
        return len(self.lost_calls) == 0

    def convert_datetime_seconds(self, datetime_obj):
        return 60 * (datetime_obj.hour * 60) + datetime_obj.minute * 60 + datetime_obj.second

    def extract_call_details(self, call_details):
        self.call_details_duration = self.read_report(report=call_details,
                                                      call_group=self.answered_calls,
                                                      call_ticker=self.call_details_ticker,
                                                      wait_answered=self.wait_answered)

    def extract_abandon_group_details(self, abandon_group):
        self.abandon_group_duration = self.read_report(report=abandon_group,
                                                       call_group=self.lost_calls)

    def read_report(self, report=None, call_group=None, call_ticker=None, wait_answered=None):
        duration_counter = timedelta(seconds=0)
        for call_id in reversed(call_group):
            start_time = report[call_id, 'Start Time']
            if self.valid_time(parse(start_time)) or self.full_service:
                duration_datetime = parse(report[call_id, 'Call Duration'])
                converted_seconds = self.convert_datetime_seconds(duration_datetime)
                if report.name == 'call_details' or converted_seconds >= 20:
                    duration_counter += timedelta(seconds=converted_seconds)
                    if call_ticker is not None:
                        hold_duration = parse(report[call_id, 'Wait Time'])
                        hold_duration_seconds = self.convert_datetime_seconds(hold_duration)
                        wait_answered.append(hold_duration_seconds)
                        call_ticker.add_range_item(hold_duration_seconds)
                        if hold_duration_seconds > self.longest_answered:
                            self.longest_answered = hold_duration_seconds
                else:
                    call_group.remove(call_id)
            else:
                call_group.remove(call_id)
        return duration_counter

    def valid_time(self, call_datetime):
        # TODO: call ID are ordered -> check first and last instead of whole call_ID list
        call_time = call_datetime.time()
        return self.earliest_call <= call_time <= self.latest_call

    def get_longest_answered(self):
        return self.longest_answered

    def get_avg_call_duration(self):
        return self.get_avg_duration(current_duration=self.call_details_duration.total_seconds(),
                                     call_group=self.answered_calls)

    def get_avg_lost_duration(self):
        return self.get_avg_duration(current_duration=self.abandon_group_duration.total_seconds(),
                                     call_group=self.lost_calls)

    def get_avg_wait_answered(self):
        return self.get_avg_duration(current_duration=sum(self.wait_answered),
                                     call_group=self.wait_answered)

    def get_avg_duration(self, current_duration=None, call_group=None):
        return_value = current_duration
        try:
            return_value //= len(call_group)
        except ZeroDivisionError:
            pass
        return int(return_value)

    def get_number_of_calls(self):
        return {
            'answered': len(self.answered_calls),
            'lost': len(self.lost_calls),
            'voicemails': len(self.voicemails)
        }

    def chop_microseconds(self, delta):
        return delta - timedelta(microseconds=delta.microseconds)

    def get_call_ticker(self):
        return self.call_details_ticker

    def is_full_service(self):
        return self.full_service
