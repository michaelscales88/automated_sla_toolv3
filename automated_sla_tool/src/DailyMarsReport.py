import os
import re
import pyexcel as pe
import pypyodbc as ps
from datetime import datetime, time, timedelta
from collections import namedtuple
from automated_sla_tool.src.AReport import AReport
from automated_sla_tool.src.UtilityObject import UtilityObject
from automated_sla_tool.src.Notes import Notes


class DailyMarsReport(AReport):
    def __init__(self, day=None):
        # TODO: add xslx writer for spreadsheet formatting
        super().__init__(report_dates=day,
                         report_type='mars_report')
        if self.check_finished():
            print('Report Complete for {}'.format(self._inr))
        else:
            self.req_src_files = [r'Agent Time Card', r'Agent Realtime Feature Trace', r'Agent Calls']
            # TODO more testing on load documents + whether it is messing up duration/dnd
            self.load()
            spreadsheet = r'M:\Help Desk\Schedules for OPS.xlsx'
            self.tracker = EmployeeTracker(spreadsheet, self.get_data_measurements())
            self.notes = Notes()
            self.run2()

    '''
    UI Section
    '''

    # def run(self):
    #     if self.final_report.finished:
    #         return
    #     else:
    #         agents = self.tracker.get_tracker()
    #         self.final_report.set_header(self.tracker.get_header())
    #         for (ext, agent) in agents.items():
    #             if agent[self.day_of_wk]:
    #                 sheet_name = r'{0} {1}({2})'.format(agent.f_name, agent.l_name, ext)
    #                 try:
    #                     time_card = self.src_files['Agent Time Card'][sheet_name]
    #                 except KeyError:
    #                     agent.data['Absent'] = 1
    #                 else:
    #                     try:
    #                         self.read_time_card(time_card, agent)
    #                     except IndexError:
    #                         agent.data.add_note(self.notes.add_note(r'Data Error: No Valid Time Data'))
    #                     else:
    #                         feature_card = self.src_files['Agent Realtime Feature Trace'][sheet_name]
    #                         self.read_feature_card(feature_card, agent)
    #                         try:
    #                             agent_call_card = self.src_files['Agent Calls'][sheet_name]
    #                         except KeyError:
    #                             pass
    #                         else:
    #                             self.read_call_card(agent_call_card, agent)
    #                 finally:
    #                     # TODO this needs to be redone for the new FinalReport class
    #                     self.final_report.row += self.tracker[ext]
    #         self.finalize_report()

    def run2(self):
        if self._output.finished:
            return
        else:
            agents = self.tracker.get_tracker()
            for (ext, agent) in agents.items():
                if agent[self.day_of_wk]:
                    try:
                        rtn_data = self.read_time_card2(agent)
                        if agent.l_name == 'Rice':
                            print('inside corner case')
                            print(rtn_data)
                    except IndexError:
                        # agent.data.add_note(self.notes.add_note(r'Data Error: No Valid Time Data'))
                        rtn_data = {
                            'Late': 0,
                            'Logged In': 0,
                            'Logged Out': 0,
                            'Duration': 0,
                            'Absent': 1
                        }
                    if not self._output.colnames:
                        self._output.row += ([''] + sorted(rtn_data.keys()))
                        self._output.name_columns_by_row(0)
                    # sheet_name = r'{0} {1}({2})'.format(agent.f_name, agent.l_name, ext)

                    # try:
                    #     time_card = self.src_files['Agent Time Card'][sheet_name]
                    # except KeyError:
                    #     time_card = None
                    #     agent.data['Absent'] = 1
                    # else:
                    #     try:
                    #         self.read_time_card(time_card, agent)
                    #     except IndexError:
                    #         agent.data.add_note(self.notes.add_note(r'Data Error: No Valid Time Data'))
                    # print(rtn_data)
                    # try:
                    #     rtn_data2 = self.read_feature_card2(agent)
                    # except Exception as e:
                    #     print(e)
                    #     rtn_data2 = {}

                    # try:
                    #     feature_card = self.src_files['Agent Realtime Feature Trace'][sheet_name]
                    # except KeyError:
                    #     feature_card = None
                    # else:
                    #     self.read_feature_card(feature_card, agent)
                    # print(rtn_data2)
                    # try:
                    #     rtn_data3 = self.read_call_card2(agent)
                    # except Exception as e:
                    #     print(e)
                    #     rtn_data3 = {}
                    # print(rtn_data3)
                    # test = {**rtn_data, **rtn_data2, **rtn_data3}
                    # print(test)
                    # try:
                    #     agent_call_card = self.src_files['Agent Calls'][sheet_name]
                    # except KeyError:
                    #     agent_call_card = None
                    # else:
                    #     self.read_call_card(agent_call_card, agent)
                    # try:
                    #     test['Avail'] = self.get_percent_avail(test['Duration'],
                    #                                            self.convert_time_stamp(rtn_data['DND Duration']))
                    #     if test['DND Duration'] > test['Duration']:
                    #         test['DND Duration'] = test['Duration']
                    #     # self.final_report.row += self.tracker[ext]
                    # except KeyError:
                    #     pass
                    row_name = r'{0} {1}({2})'.format(agent.f_name, agent.l_name, ext)
                    row_portion = [rtn_data[k] for k in sorted(rtn_data.keys())]
                    self._output.row += [row_name] + row_portion

            self.finalize_report()

    def test(self):
        print(self._output)
        print(self._output.query_format())

    def save_report(self):
        pass

    '''
    Utilities Section
    '''

    def make_start_end(self):
        namedtuple()

    def finalize_report(self):
        notes_label = [self.notes.pop(0)]
        self._output.row += notes_label
        self._output.row += self.notes.get_notes()
        self._output.name_rows_by_column(0)

    def check_day_card(self, time_card, shift_start, shift_end):
        prev_day = self._inr - timedelta(days=1)
        self.remove_row_w_day(time_card, prev_day)
        start_time = self.get_start_time(time_card.column['Logged In'])
        end_time = self.get_end_time(time_card.column['Logged Out'])
        clocked_in = start_time >= time(hour=1)
        # TODO this needs to be refactored... possibly move the logic into start/end shift functions
        if len(time_card.column['Logged Out']) is 1 and '' in time_card.column['Logged Out']:
            clocked_out = False
        else:
            clocked_out = end_time <= time(hour=23)

        # TODO improve this... checking for agents who didn't clock out and are late
        if not clocked_in and time_card.number_of_rows() is 2:
            start_time = self.get_start_time(time_card.column['Logged In'], overnight=True)
            clocked_in = True
        return (start_time if clocked_in else shift_start,
                end_time if clocked_out else shift_end,
                clocked_in,
                clocked_out)

    def check_night_card(self, time_card, shift_start, shift_end):
        tomorrow = self._inr + timedelta(days=1)
        self.remove_row_w_day(time_card, tomorrow)
        start_time = self.get_start_time(time_card.column['Logged In'], overnight=True)
        end_time = self.get_end_time(time_card.column['Logged Out'])
        clocked_in = start_time >= time(hour=1)
        clocked_out = end_time <= time(hour=23)
        return (start_time if clocked_in else shift_start,
                end_time if clocked_out else shift_end,
                clocked_in,
                clocked_out)

    def remove_row_w_day(self, time_card, remove_date):
        try:
            for r_index, event in enumerate(time_card.rows()):
                for index in event:
                    if self.safe_parse_dt(index).date() == remove_date:
                        del time_card.row[r_index]
        except TypeError:
            print('Bad type: remove_date object'
                  '-> DailyMarsReport.remove_row_w_day')

    def read_sql(self):
        CONNECTION_STRING = ('Driver={SQL Server};'
                             'Server=10.1.3.43;'
                             'Database=IssueTracker;'
                             'uid=IssueTrackerWeblogin;'
                             'pwd=mw!2006')
        # SQL_COMMAND = (
        # "SELECT DISTINCT bugs.bg_reported_date, bug_posts.bp_bug, bug_posts.bp_user, "
        # "users.us_firstname, users.us_lastname "
        # "FROM bug_posts "
        # "INNER JOIN bugs ON (bug_posts.bp_bug = bugs.bg_id) "
        # "LEFT JOIN users ON (users.us_id = bug_posts.bp_user) "
        # "WHERE (bugs.bg_reported_date >= {0}) and (bugs.bg_reported_date <= {1}) and "
        # "(bug_posts.bp_user not like 4) and (bugs.bg_user_defined_attribute not like 15)"
        # ).format(self.dates.strftime('%m/%d/%Y'), (self.dates + timedelta(days=1)).strftime('%m/%d/%Y'))
        SQL_COMMAND = (
            '''
            SELECT DISTINCT bugs.bg_reported_date, bug_posts.bp_bug, bug_posts.bp_user,
            users.us_firstname, users.us_lastname
            FROM bug_posts
            INNER JOIN bugs ON (bug_posts.bp_bug = bugs.bg_id)
            LEFT JOIN users ON (users.us_id = bug_posts.bp_user)
            WHERE (bugs.bg_reported_date >= '{0}') and (bugs.bg_reported_date <= '{1}') and
            (bug_posts.bp_user not like 4) and
            (bugs.bg_user_defined_attribute not like 15)
            '''
        ).format(self._inr.strftime('%m/%d/%Y'), (self._inr + timedelta(days=1)).strftime('%m/%d/%Y'))

        SQL_COMMAND2 = (
            '''
            SELECT bg_id [id],
            bg_short_desc [desc],
            bg_reported_date [reported on],
            bg_last_updated_date [updated on],
            isnull(rpt.us_username,'') [reported by],
            isnull(pj_name,'') [project],
            isnull(og_name,'') [organization],
            isnull(ct_name,'') [category],
            isnull(pr_name,'') [priority],
            isnull(asg.us_username,'') [assigned to],
            isnull(lub.us_username,'') [last updated by],
            isnull(st_name,'') [status],
            isnull(udf_name,'') [Action Time],
            isnull([bg_cost_center],'') [bg_cost_center],
            isnull([bg_requested_completion],'') [bg_requested_completion],
            isnull([bg_estimated_hours],'') [bg_estimated_hours],
            isnull([bg_estimated_completion],'') [bg_estimated_completion],
            isnull([bg_help_desk_time_spent],'') [bg_help_desk_time_spent]
            FROM bugs WITH (nolock)
            LEFT OUTER JOIN users rpt WITH (nolock) ON rpt.us_id = bg_reported_user
            LEFT OUTER JOIN users asg WITH (nolock) ON asg.us_id = bg_assigned_to_user
            LEFT OUTER JOIN users lub WITH (nolock) ON lub.us_id = bg_last_updated_user
            LEFT OUTER JOIN projects WITH (nolock) ON pj_id = bg_project
            LEFT OUTER JOIN orgs WITH (nolock) ON og_id = bg_org
            LEFT OUTER JOIN categories WITH (nolock) ON ct_id = bg_category
            LEFT OUTER JOIN priorities WITH (nolock) ON pr_id = bg_priority
            LEFT OUTER JOIN statuses WITH (nolock) ON st_id = bg_status
            LEFT OUTER JOIN user_defined_attribute WITH (nolock) ON udf_id = bg_user_defined_attribute
            WHERE  bg_reported_user in (230,242,60,250,254,192,229,209,222,232,176,198,264,96,175,178,241,11,255,257,226,195,261,206,179,237,245,138,265,235,266,262,19,260,203)
            AND  bg_reported_date >= '{0}' AND  bg_reported_date <= '{1}'
            ORDER BY bg_id DESC
            '''
        ).format(self._inr.strftime('%m/%d/%Y'), (self._inr + timedelta(days=1)).strftime('%m/%d/%Y'))

        SQL_COMMAND3 = (
            '''
            SELECT bg_id [id],
            bg_short_desc [desc],
            bg_reported_date [reported on],
            bg_last_updated_date [updated on],
            isnull(rpt.us_username,'') [reported by],
            isnull(pj_name,'') [project],
            isnull(og_name,'') [organization],
            isnull(ct_name,'') [category],
            isnull(pr_name,'') [priority],
            isnull(asg.us_username,'') [assigned to],
            isnull(lub.us_username,'') [last updated by],
            isnull(st_name,'') [status],
            isnull(udf_name,'') [Action Time],
            isnull([bg_cost_center],'') [bg_cost_center],
            isnull([bg_requested_completion],'') [bg_requested_completion],
            isnull([bg_estimated_hours],'') [bg_estimated_hours],
            isnull([bg_estimated_completion],'') [bg_estimated_completion],
            isnull([bg_help_desk_time_spent],'') [bg_help_desk_time_spent]
            FROM bugs WITH (nolock)
            LEFT OUTER JOIN users rpt WITH (nolock) ON rpt.us_id = bg_reported_user
            LEFT OUTER JOIN users asg WITH (nolock) ON asg.us_id = bg_assigned_to_user
            LEFT OUTER JOIN users lub WITH (nolock) ON lub.us_id = bg_last_updated_user
            LEFT OUTER JOIN projects WITH (nolock) ON pj_id = bg_project
            LEFT OUTER JOIN orgs WITH (nolock) ON og_id = bg_org
            LEFT OUTER JOIN categories WITH (nolock) ON ct_id = bg_category
            LEFT OUTER JOIN priorities WITH (nolock) ON pr_id = bg_priority
            LEFT OUTER JOIN statuses WITH (nolock) ON st_id = bg_status
            LEFT OUTER JOIN user_defined_attribute WITH (nolock) ON udf_id = bg_user_defined_attribute
            WHERE  bg_last_updated_user in (230,242,60,250,254,192,229,209,222,232,176,198,264,96,175,178,241,11,255,257,
                                            226,195,261,206,179,237,245,138,265,235,266,262,19,260,203)
            AND  bg_status in (5)
            AND  bg_user_defined_attribute in (8,9,10,11,19,12,13,16,14)
            AND  bg_reported_date >= '{0}' AND  bg_reported_date <= '{1}'

            ORDER BY bg_id DESC
            '''
        ).format(self._inr.strftime('%m/%d/%Y'), (self._inr + timedelta(days=1)).strftime('%m/%d/%Y'))

        sql_commands = [SQL_COMMAND, SQL_COMMAND2, SQL_COMMAND3]

        try:
            cnx = ps.connect(CONNECTION_STRING)
            print('successful connection')
            cur = cnx.cursor()
            for command in sql_commands:
                cur.execute(command)
                sheet = pe.Sheet()
                sheet.row += [str(d[0]) for d in cur.description]
                sheet.name_columns_by_row(0)
                for row in cur.fetchall():
                    sheet.row += list(row)
                print('Query completed.')
                print(sheet)
                # try:
                #     cur.execute(SQL_COMMAND, values)
                #     cur.commit()
                # except ps.IntegrityError:
                #     print('Received integrity error'
                #           '-> DailyMarsReport.query_sql_server'
                #           )
                # for (ext, agent) in self.tracker.get_tracker().items():
                #     print(r'{0} has {1} tickets'.format(agent.l_name, sheet.column['us_lastname'].count(agent.l_name)))
        except Exception:
            print("General exception pushing to SQL")
            import sys
            import traceback
            error = traceback.format_exc()
            traceback.print_exc(file=sys.stderr)
            print(error)
        else:
            cur.close()
            cnx.close()
            print('successfully closed connection')

    def write_sqlite(self):
        local_db = os.path.join(self.path, r'db\automated_sla_tool.db')
        params1 = {
            'local_db': local_db,
        }
        params2 = {
            'database': 'chronicall',
            'user': 'Chronicall',
            'password': 'ChR0n1c@ll1337',
            'host': '10.1.3.17',
            'port': 9086
        }
        from automated_sla_tool.src.SqlWriter import SqlWriter as ps_write
        conn = ps_write(**params2)
        # conn = lite(**params1)
        # print(conn.get_tables())
        # if input('Drop mars_report?') == 1:
        #     conn.drop_table('mars_report')
        # print(conn.get_tables())
        # conn.insert(self.final_report)
        # print(self.final_report)

    def get_data_measurements(self):
        # print('{0} {1}'.format(self.dates, self.src_files.keys()))
        # TODO refactor this to collate src_files + take program provided names
        if self.is_empty_wb(self.src_files['Agent Time Card']):
            raise OSError('No agents for report')
        return self.src_files['Agent Time Card'][0].colnames

    def read_time_card(self, time_card, emp_data):
        shift_start = emp_data[self.day_of_wk].start
        shift_end = emp_data[self.day_of_wk].end
        is_normal_shift = time(hour=0) <= shift_start <= time(hour=18, minute=59)

        if is_normal_shift:
            (emp_data.data['Logged In'],
             emp_data.data['Logged Out'],
             clocked_in,
             clocked_out) = self.check_day_card(time_card, shift_start, shift_end)
        else:
            (emp_data.data['Logged In'],
             emp_data.data['Logged Out'],
             clocked_in,
             clocked_out) = self.check_night_card(time_card, shift_start, shift_end)
            if clocked_in:
                emp_data.data.add_note(self.notes.add_note(r'Logged in {}'.format(
                    self._inr - timedelta(days=1)))
                )
        if clocked_in is False:
            emp_data.data.add_note(self.notes.add_note(r'No Login'))
        if clocked_out is False:
            emp_data.data.add_note(self.notes.add_note(r'No Logout'))
        try:
            duration = (datetime.min +
                        (datetime.combine(self._inr, emp_data.data['Logged Out']) -
                         datetime.combine(self._inr, emp_data.data['Logged In']))).time()
        except OverflowError:
            duration = (datetime.min +
                        (datetime.combine(self._inr + timedelta(days=1), emp_data.data['Logged Out']) -
                         datetime.combine(self._inr, emp_data.data['Logged In']))).time()
        emp_data.data['Duration'] = duration
        late = self.read_time(emp_data.data['Logged In']) > self.check_grace_pd(shift_start,
                                                                                minutes=timedelta(minutes=5))
        if clocked_in and late:
            emp_data.data['Late'] = 1

    def read_feature_card(self, feature_card, emp_data):
        # TODO this needs to check for overnight
        num_dnd, dnd_sec = self.correlate_dnd_data(feature_card.column['Feature Type'],
                                                   feature_card.column['Duration'],
                                                   'Do Not Disturb')
        emp_data.data['numDND'] = num_dnd
        emp_data.data['Avail'] = self.get_percent_avail(emp_data.data['Duration'], dnd_sec)
        emp_data.data['DND Duration'] = 0 if dnd_sec is 0 else (datetime.min + timedelta(seconds=dnd_sec)).time()
        if emp_data.data['DND Duration'] > emp_data.data['Duration']:
            emp_data.data['DND Duration'] = emp_data.data['Duration']

    def read_call_card(self, call_card, emp_data):
        (inb_ans,
         inb_lost,
         inb_talk_dur) = self.count_inbound_calls(call_card.column['Call Direction'],
                                                  (call_card.column['Answered'], call_card.column['Talking Duration']),
                                                  'Inbound')
        (out_calls,
         out_talk_dur) = self.count_outbound_calls(call_card.column['Call Direction'],
                                                   call_card.column['Talking Duration'],
                                                   'Outbound')
        emp_data.data['Inbound Ans'] = inb_ans
        emp_data.data['Inbound Lost'] = inb_lost
        emp_data.data['Outbound'] = out_calls
        emp_data.data['Inbound Duration'] = 0 if inb_ans is 0 else (datetime.min +
                                                                    timedelta(seconds=inb_talk_dur // inb_ans)).time()
        emp_data.data['Outbound Duration'] = 0 if out_calls is 0 else (datetime.min +
                                                                       timedelta(
                                                                           seconds=out_talk_dur // out_calls)).time()

    def read_feature_card2(self, emp_data):
        # TODO this needs to check for overnight
        rtn_data = {}
        feature_card = self.open_rpt_pg('Agent Realtime Feature Trace',
                                        r'{0} {1}({2})'.format(emp_data.f_name, emp_data.l_name, emp_data.ext))
        num_dnd, dnd_sec = self.correlate_dnd_data(feature_card.column['Feature Type'],
                                                   feature_card.column['Duration'],
                                                   'Do Not Disturb')
        rtn_data['numDND'] = num_dnd
        rtn_data['DND Duration'] = 0 if dnd_sec is 0 else (datetime.min + timedelta(seconds=dnd_sec)).time()
        return rtn_data

    def read_call_card2(self, emp_data):
        rtn_data = {}
        call_card = self.open_rpt_pg('Agent Calls',
                                     r'{0} {1}({2})'.format(emp_data.f_name, emp_data.l_name, emp_data.ext))
        (inb_ans,
         inb_lost,
         inb_talk_dur) = self.count_inbound_calls(call_card.column['Call Direction'],
                                                  (call_card.column['Answered'], call_card.column['Talking Duration']),
                                                  'Inbound')
        (out_calls,
         out_talk_dur) = self.count_outbound_calls(call_card.column['Call Direction'],
                                                   call_card.column['Talking Duration'],
                                                   'Outbound')
        rtn_data['Inbound Ans'] = inb_ans
        rtn_data['Inbound Lost'] = inb_lost
        rtn_data['Outbound'] = out_calls
        rtn_data['Inbound Duration'] = 0 if inb_ans is 0 else (datetime.min +
                                                               timedelta(seconds=inb_talk_dur // inb_ans)).time()
        rtn_data['Outbound Duration'] = 0 if out_calls is 0 else (datetime.min +
                                                                  timedelta(
                                                                      seconds=out_talk_dur // out_calls)).time()
        return rtn_data

    def read_time_card2(self, emp_data):
        # TODO get into this in a serious way...
        rtn_data = {
            'Late': 0,
            'Logged In': 0,
            'Logged Out': 0,
            'Duration': 0,
            'Absent': 0
        }
        time_card = self.open_rpt_pg('Agent Time Card',
                                     r'{0} {1}({2})'.format(emp_data.f_name, emp_data.l_name, emp_data.ext))
        if time_card:
            if emp_data.l_name == 'Rice':
                print(time_card)
            shift_start = emp_data[self.day_of_wk].start
            shift_end = emp_data[self.day_of_wk].end
            is_normal_shift = time(hour=0) <= shift_start <= time(hour=18, minute=59)

            if is_normal_shift:
                (rtn_data['Logged In'],
                 rtn_data['Logged Out'],
                 clocked_in,
                 clocked_out) = self.check_day_card(time_card, shift_start, shift_end)
            else:
                if emp_data.l_name == 'Rice':
                    print('about to read')
                (rtn_data['Logged In'],
                 rtn_data['Logged Out'],
                 clocked_in,
                 clocked_out) = self.check_night_card(time_card, shift_start, shift_end)
                if emp_data.l_name == 'Rice':
                    print('done read')
                if clocked_in:
                    emp_data.data.add_note(self.notes.add_note(r'Logged in {}'.format(
                        self._inr - timedelta(days=1)))
                    )
                if emp_data.l_name == 'Rice':
                    print('cleared clocked in')
            if emp_data.l_name == 'Rice':
                print(rtn_data)
            if clocked_in is False:
                emp_data.data.add_note(self.notes.add_note(r'No Login'))
            if clocked_out is False:
                emp_data.data.add_note(self.notes.add_note(r'No Logout'))
            try:
                duration = (datetime.min +
                            (datetime.combine(self._inr, rtn_data['Logged Out']) -
                             datetime.combine(self._inr, rtn_data['Logged In']))).time()
            except OverflowError:
                duration = (datetime.min +
                            (datetime.combine(self._inr + timedelta(days=1), rtn_data['Logged Out']) -
                             datetime.combine(self._inr, rtn_data['Logged In']))).time()
            rtn_data['Duration'] = duration
            late = self.read_time(rtn_data['Logged In']) > self.check_grace_pd(shift_start,
                                                                               minutes=timedelta(minutes=5))
            if clocked_in and late:
                rtn_data['Late'] = 1
            if emp_data.l_name == 'Rice':
                print(rtn_data)
        else:
            rtn_data['Absent'] = 1
        if emp_data.l_name == 'Rice':
            print(rtn_data)
        return rtn_data

    def open_rpt_pg(self, rpt, rpt_pg):
        try:
            file = self.src_files[rpt][rpt_pg]
        except KeyError:
            print('couldnt open file {0}{1}'.format(rpt, rpt_pg))
            file = None
        return file

    def correlate_dnd_data(self, src_list, list_to_correlate, key):
        dnd_list = super().correlate_list_time_data(src_list, list_to_correlate, key)
        return len(dnd_list), sum(v for v in dnd_list)

    def count_inbound_calls(self, src_list, list_to_correlate, key):
        inbound_calls = super().correlate_list_val_data(src_list, list_to_correlate[0], key)
        talk_dur = super().correlate_list_time_data(src_list, list_to_correlate[1], key)
        return inbound_calls.count(True), inbound_calls.count(False), sum(v for v in talk_dur)

    def count_outbound_calls(self, src_list, list_to_correlate, key):
        talk_dur = super().correlate_list_time_data(src_list, list_to_correlate, key)
        return len(talk_dur), sum(v for v in talk_dur)

    def get_percent_avail(self, dt_time, div_sec):
        dt_delta = timedelta(hours=dt_time.hour, minutes=dt_time.minute, seconds=dt_time.second)
        dnd_delta = timedelta(seconds=div_sec)
        dt_delta = dnd_delta if dnd_delta > dt_delta else dt_delta
        return float(r'{0:.2f}'.format(((dt_delta - dnd_delta) / dt_delta) * 100))

    def get_start_time(self, column, overnight=False):
        if overnight:
            return_time = max(self.safe_parse_dt(item).time() for item in column)
        else:
            return_time = min(self.safe_parse_dt(item).time() for item in column)
        return return_time

    def get_end_time(self, column):
        return max(self.safe_parse_dt(item).time() for item in column)

    def get_page_as_num(self, sheet_name):  # TODO this needs to switch as the way to access agent sheet
        return_value = re.findall(r'\b\d+\b', sheet_name)
        if len(return_value) != 1:
            raise NameError('In MarsReport.get_page_as_num'
                            'Error reading page number'
                            '-> bad sheet name')
        return return_value[0]

    def check_grace_pd(self, dt_t, minutes):
        return self.add_time(dt_t, add_time=minutes)

    def __str__(self):
        return str(self._output)


class EmployeeTracker(UtilityObject):
    # TODO add overnight checking. should be a data attribute and should be a bool
    # TODO based on whether the current shift is after hours or not.
    def __init__(self, employee_data, report_data):
        super().__init__()
        data = self.load_data(employee_data)
        self.__data = self.create_schedule(data, report_data)

    def create_schedule(self, data, report_data):
        return_dict = {}
        new_schedule = namedtuple('this_emp', 'Monday Tuesday Wednesday Thursday Friday '
                                              'Saturday Sunday f_name l_name data ext')
        new_schedule.__new__.__defaults__ = (None,) * len(new_schedule._fields)
        for emp in data.rownames:
            emp_schedule = new_schedule(f_name=data[emp, 'First'],
                                        l_name=data[emp, 'Last'],
                                        ext=int(emp),
                                        Monday=self.date_factory(data[emp, 'Monday']),
                                        Tuesday=self.date_factory(data[emp, 'Tuesday']),
                                        Wednesday=self.date_factory(data[emp, 'Wednesday']),
                                        Thursday=self.date_factory(data[emp, 'Thursday']),
                                        Friday=self.date_factory(data[emp, 'Friday']),
                                        Saturday=self.date_factory(data[emp, 'Saturday']),
                                        Sunday=self.date_factory(data[emp, 'Sunday']),
                                        data=EmployeeData(report_data))
            return_dict[emp] = emp_schedule
        return return_dict

    def date_factory(self, date_string):
        dt = namedtuple('date', 'start end')
        try:
            (raw_start, raw_end) = self.split_str(date_string)
        except ValueError:
            return_dt = None
        else:
            dt_start = datetime.strptime(raw_start, '%H:%M').time()
            dt_end = datetime.strptime(raw_end, '%H:%M').time()
            return_dt = dt(start=dt_start, end=dt_end)
        return return_dt

    def split_str(self, t_string):
        return t_string.split('-')

    def __delitem__(self, ext):
        del self.__data[ext]

    def __getitem__(self, ext):
        agent_data = self.__data[ext]
        row_name = r'{0} {1}({2})'.format(agent_data.f_name, agent_data.l_name, ext)
        return [row_name] + agent_data.data.get_row()

    def get_tracker(self):
        return self.__data

    def get_header(self):
        return ['Employee'] + sorted(next(iter(self.__data.values())).data.keys())


class EmployeeData(object):
    def __init__(self, k_list):
        # TODO should provide these fields to the obj
        self.__dict = {}
        for key in k_list:
            self.__dict[key] = 0
        self.__dict['Inbound Ans'] = 0
        self.__dict['Inbound Lost'] = 0
        self.__dict['Outbound'] = 0
        self.__dict['Inbound Duration'] = 0
        self.__dict['Outbound Duration'] = 0
        self.__dict['Absent'] = 0
        self.__dict['Late'] = 0
        self.__dict['DND Duration'] = 0
        self.__dict['numDND'] = 0
        self.__dict['Avail'] = 0
        self.__dict['Notes'] = ''

    def increment_key(self, key, val):
        if key not in self.__dict:
            raise KeyError("The key {} is not defined.".format(key))
        self.__dict[key] += val

    def __setitem__(self, key, item):
        self.__dict[key] = item

    def __getitem__(self, key):
        try:
            return self.__dict[key]
        except KeyError:
            print('Key does not exist: {}'.format(key))

    def add_note(self, note):
        self.increment_key('Notes', r'{} '.format(note))

    def get_row(self):
        return [self.__dict[k] for k in sorted(self.__dict.keys())]

    def keys(self):
        return self.__dict.keys()
