# Functions which retrieve data from workbooks to store in each class. Will take wb and return values

from collections import defaultdict

from src.CONSTANTS import (HUNT_GROUP_FIRST_PAGE_NAME,
                           CALL_DETAILS_FIRST_PAGE_NAME,
                           ABANDON_CALLS_GROUP_PAGE_NAME,
                           HUNT_GRP_ROW)
from src.utils import get_sec
from .cradle2grave import CallId
from src.input_valididation import valid_input


def process_hunt_group_report(wb):
    ws = wb.get_sheet_by_name(HUNT_GROUP_FIRST_PAGE_NAME)

    call_15sec = valid_input('O', HUNT_GRP_ROW, ws, 'N')
    try:
        call_15sec += valid_input('P', HUNT_GRP_ROW, ws, 'N')
    except TypeError:
        pass
    call_30sec = valid_input('Q', HUNT_GRP_ROW, ws, 'N')
    call_45sec = valid_input('S', HUNT_GRP_ROW, ws, 'N')
    call_60sec = valid_input('T', HUNT_GRP_ROW, ws, 'N')
    call_g60sec = valid_input('U', HUNT_GRP_ROW, ws, 'N')
    calls_answered = valid_input('E', HUNT_GRP_ROW, ws, 'N')
    avg_call_ans = valid_input('L', HUNT_GRP_ROW, ws, 'N')
    longest_time_ans = valid_input('V', HUNT_GRP_ROW, ws, 'N')
    avg_call_dur_seconds = valid_input('J', HUNT_GRP_ROW, ws, 'N')
    return (calls_answered,
            avg_call_dur_seconds,
            avg_call_ans,
            longest_time_ans,
            call_15sec,
            call_30sec,
            call_45sec,
            call_60sec,
            call_g60sec)


def process_abandon_calls(wb, name):
    ws = wb.get_sheet_by_name(ABANDON_CALLS_GROUP_PAGE_NAME)
    lost_calls = 0
    lost_call_duration = 0
    for row_number in range(5, ws.max_row + 1):
        bool_call_answered = (valid_input('G', row_number, ws, 'B'))
        internal_client_name = valid_input('E', row_number, ws, 'N')
        call_duration_seconds = valid_input('K', row_number, ws, 'N')
        if internal_client_name == name and bool_call_answered is False:
            if call_duration_seconds >= 20:
                lost_calls += 1
                lost_call_duration += call_duration_seconds
    if lost_calls == 0:
        return 0, 0
    return int(lost_calls), int(lost_call_duration/lost_calls)


def process_call_details_ticker(wb, name, bool_is_24hr):
    number_of_calls_less_than_15sec = 0
    number_of_calls_less_than_30sec = 0
    number_of_calls_less_than_45sec = 0
    number_of_calls_less_than_60sec = 0
    number_of_calls_greater_than_60sec = 0
    ws = wb.get_sheet_by_name(CALL_DETAILS_FIRST_PAGE_NAME)
    for rowNumber in range(4, ws.max_row + 1):
        internal_client_name = valid_input('G', rowNumber, ws, 'N')
        call_answered = valid_input('L', rowNumber, ws, 'B')
        start_time = valid_input('D', rowNumber, ws, 'S')
        start_time = get_sec(start_time[-8:])
        talk_duration = valid_input('M', rowNumber, ws, 'N')
        bool_good_call = is_good_call(name, internal_client_name, call_answered, start_time, bool_is_24hr)
        if bool_good_call is True:
            if talk_duration <= 15:
                number_of_calls_less_than_15sec += 1
            elif talk_duration <= 30:
                number_of_calls_less_than_30sec += 1
            elif talk_duration <= 45:
                number_of_calls_less_than_45sec += 1
            elif talk_duration <= 60:
                number_of_calls_less_than_60sec += 1
            elif talk_duration > 60:
                number_of_calls_greater_than_60sec += 1
            else:
                pass
    return (number_of_calls_less_than_15sec,
            number_of_calls_less_than_30sec,
            number_of_calls_less_than_45sec,
            number_of_calls_less_than_60sec,
            number_of_calls_greater_than_60sec)


def process_call_details_report(wb, name, bool_is_24hr):
    call_details_sheet = wb.get_sheet_by_name(CALL_DETAILS_FIRST_PAGE_NAME)

    (number_of_calls_less_than_15sec,
     number_of_calls_less_than_30sec,
     number_of_calls_less_than_45sec,
     number_of_calls_less_than_60sec,
     number_of_calls_greater_than_60sec) = process_call_details_ticker(wb, name, bool_is_24hr)

    true_calls = 0
    talk_dur = 0
    hold_time = 0
    longest_hold = 0

    for row_number in range(4, call_details_sheet.max_row + 1):
        call_answered = (valid_input('L', row_number, call_details_sheet, 'B'))
        internal_client_name = valid_input('G', row_number, call_details_sheet, 'N')
        call_hold_time = valid_input('M', row_number, call_details_sheet, 'N')
        call_talk_duration = valid_input('J', row_number, call_details_sheet, 'N')
        start_time = valid_input('D', row_number, call_details_sheet, 'S')
        start_time = get_sec(start_time[-8:])

        bool_good_call = is_good_call(name, internal_client_name, call_answered, start_time, bool_is_24hr)

        if bool_good_call is True:
            true_calls += 1
            talk_dur += call_talk_duration
            hold_time += call_hold_time
            if call_hold_time >= longest_hold:
                longest_hold = call_hold_time
    if true_calls == 0:
        return 0, 0, 0, 0, 0, 0, 0, 0, 0
    return (true_calls,
            talk_dur,
            hold_time,
            longest_hold,
            number_of_calls_less_than_15sec,
            number_of_calls_less_than_30sec,
            number_of_calls_less_than_45sec,
            number_of_calls_less_than_60sec,
            number_of_calls_greater_than_60sec)


def is_good_call(name, internal_client_name, call_answered, start_time, bool_is_24hr):
    if bool_is_24hr is True:
        good_call = (internal_client_name == name) and call_answered is True
    else:
        good_call = (internal_client_name == name
                     and call_answered is True
                     and 25200 <= start_time < 68400)
    return good_call


def find_duplicates_abandon_group_report(wb):
    ws = wb.get_sheet_by_name(ABANDON_CALLS_GROUP_PAGE_NAME)
    all_call_dictionary = get_duplicates_from_worksheet(ws)
    list_of_phone_numbers = list(all_call_dictionary.keys())
    duplicate_call_dictionary = remove_single_calls(all_call_dictionary, list_of_phone_numbers)

    final_duplicate_dict = {}
    for phone_number in duplicate_call_dictionary:
        check_position = duplicate_call_dictionary[phone_number][0]
        check_client = duplicate_call_dictionary[phone_number][1]
        found_duplicates = 0
        number_of_duplicate_calls = int(len(duplicate_call_dictionary[phone_number]) / 2)
        for value_position in range(1, number_of_duplicate_calls):
            row_number = duplicate_call_dictionary[phone_number][value_position + value_position]
            client_name = duplicate_call_dictionary[phone_number][(value_position + value_position) + 1]
            second_position = get_sec(ws['I%s' % row_number].value[-8:])
            first_position = get_sec(ws['J%s' % check_position].value[-8:])
            difference_in_seconds = second_position - first_position
            if difference_in_seconds < 360 and check_client == client_name:
                found_duplicates += 1
                check_position = row_number
                check_client = client_name
        try:
            final_duplicate_dict[client_name] += found_duplicates
        except KeyError:
            final_duplicate_dict[client_name] = found_duplicates
    return final_duplicate_dict


def get_duplicates_from_worksheet(ws):
    all_call_dictionary = defaultdict(list)
    for row_number in range(5, ws.max_row + 1):
        cell_number = valid_input('F', row_number, ws, 'S')
        call_time = valid_input('K', row_number, ws, 'N')
        call_answered = valid_input('G', row_number, ws, 'B')
        client_number = valid_input('E', row_number, ws, 'N')
        last_seven_call_number = cell_number[-7:]
        if call_time >= 20 and call_answered is False:
            all_call_dictionary[last_seven_call_number].append(row_number)
            all_call_dictionary[last_seven_call_number].append(client_number)
        else:
            pass
    return all_call_dictionary


def remove_single_calls(all_call_dictionary, list_of_phone_numbers):
    for phone_number in list_of_phone_numbers:
        has_more_than_one_call = len(all_call_dictionary[phone_number]) < 3
        if has_more_than_one_call is True:
            del all_call_dictionary[phone_number]
        else:
            pass
    return all_call_dictionary


def parse_chronicall_report(cradle_report):
    call_id_list = []
    cradle_to_grave = cradle_report.get_sheet_names()

    for index, call in enumerate(cradle_to_grave):
        created_call = CallId(cradle_to_grave[index])
        cradle_ws = cradle_report.get_sheet_by_name(created_call.name)

        (had_transfer_hold,
         conference_call,
         transfer_hold_row) = check_for_transfer_hold_and_conference_call(created_call, cradle_ws)

        if had_transfer_hold is True and conference_call is False:
            for remaining_rows in range(transfer_hold_row, cradle_ws.max_row + 1):
                cell_value = valid_input('B', remaining_rows, cradle_ws, 'S')
                if cell_value == "Talking":
                    created_call.set_hold(valid_input('I', remaining_rows, cradle_ws, 'N'))
                else:
                    pass
        created_call.set_total_hold_time()
        call_id_list.append(created_call)
    return call_id_list


def check_for_transfer_hold_and_conference_call(created_call, cradle_ws):
    had_transfer_hold = False
    conference_call = False
    transfer_hold_row = 0
    for row_number in range(4, cradle_ws.max_row + 1):
        cell_value = valid_input('B', row_number, cradle_ws, 'S')
        hold_event_duration = valid_input('I', row_number, cradle_ws, 'N')
        if cell_value == "Transfer Hold":
            created_call.set_transfer_hold(hold_event_duration)
            had_transfer_hold = True
            transfer_hold_row = row_number
        elif cell_value == "Hold":
            created_call.set_hold(hold_event_duration)
        elif cell_value == "Park":
            created_call.set_park(hold_event_duration)
        elif cell_value == "Conference":
            conference_call = True
        else:
            pass
    return had_transfer_hold, conference_call, transfer_hold_row
