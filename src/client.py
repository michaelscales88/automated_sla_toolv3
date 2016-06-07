# Contains client class which contains summed/averaged data from each spreadsheet
from .utils import convert_time_stamp


class Client:

    def __init__(self, name):
        self.name = name
        self.calls_answered = 0
        self.avg_call_duration_answered = 0
        self.avg_wait_calls_answered = 0
        self.longest_answered_time = 0
        self.calls_lost = 0
        self.avg_call_duration_lost = 0
        self.call_15sec = 0
        self.call_30sec = 0
        self.call_45sec = 0
        self.call_60sec = 0
        self.call_g60sec = 0
        self.duplicates = 0
        self.voice_mails = 0
        self.calls_that_were_voice_mails = 0
        self.twenty_four_hour = False

    # Setters
    def set_abandon_grp(self, lost_calls, average_wait_lost):
        self.calls_lost = lost_calls
        self.avg_call_duration_lost = average_wait_lost

    def set_call_details_calls(self, combined_calls):
        self.calls_answered = combined_calls

    def set_call_duration(self, average_duration, average_wait_answered):
        self.avg_call_duration_answered = average_duration
        self.avg_wait_calls_answered = average_wait_answered

    def set_longest_wait_answered(self, new_longest_answered):
        self.longest_answered_time = new_longest_answered

    def set_hunt_grp(self, calls_answered, average_duration, average_wait_answered, longest_answered):
        self.calls_answered = calls_answered
        self.avg_call_duration_answered = average_duration
        self.avg_wait_calls_answered = average_wait_answered
        self.longest_answered_time = longest_answered
        
    def set_ticker(self, call_15sec, call_30sec, call_45sec, call_60sec, call_g60sec):
        self.call_15sec = call_15sec
        self.call_30sec = call_30sec
        self.call_45sec = call_45sec
        self.call_60sec = call_60sec
        self.call_g60sec = call_g60sec

    def add_ticker(self, call_15sec, call_30sec, call_45sec, call_60sec, call_g60sec):
        self.call_15sec += call_15sec
        self.call_30sec += call_30sec
        self.call_45sec += call_45sec
        self.call_60sec += call_60sec
        self.call_g60sec += call_g60sec

    def set_voice_mails(self, number_of_voice_mails, number_of_voice_mails_removed):
        self.voice_mails = number_of_voice_mails
        self.calls_that_were_voice_mails = number_of_voice_mails_removed

    def set_duplicates(self, duplicates):
        self.duplicates = duplicates

    def set_24hr(self, is24hr):
        self.twenty_four_hour = is24hr

    def set_remove_lost_calls(self, lost_calls):
        self.calls_lost -= lost_calls

    # Getters
    def get_24hr(self):
        return self.twenty_four_hour

    def get_average_call_duration(self):
        return self.avg_call_duration_answered

    def get_calls_answered(self):
        return self.calls_answered

    def get_avg_wait_calls_answered(self):
        return self.avg_wait_calls_answered

    def get_name(self):
        return self.name

    def get_string_name(self):
        return str(self.name)

    def get_longest_answered(self):
        return self.longest_answered_time

    def get_voice_mails(self):
        return self.voice_mails

    def get_total_calls(self):
        unaccounted_calls = 0
        if self.voice_mails > (self.calls_answered + self.calls_lost):
            unaccounted_calls = self.voice_mails
        return self.calls_answered + self.calls_lost + unaccounted_calls

    def get_true_calls_lost(self):
        return self.calls_lost - self.calls_that_were_voice_mails

    def get_average_duration_time_stamp(self):
        return convert_time_stamp(self.avg_call_duration_answered)

    def get_average_wait_answered_time_stamp(self):
        return convert_time_stamp(self.avg_wait_calls_answered)

    def get_average_wait_lost_time_stamp(self):
        return convert_time_stamp(self.avg_call_duration_lost)

    def get_longest_answered_time_stamp(self):
        return convert_time_stamp(self.longest_answered_time)

    def get_ticker(self):
        return (self.call_15sec,
                self.call_30sec,
                self.call_45sec,
                self.call_60sec,
                self.call_g60sec)

    # Utilities
    def __str__(self):
        print("Client #%d" % self.name)
        print("Lost calls: %d Avg wait (lost): %s Calls answered: %d" %
              (self.calls_lost, convert_time_stamp(self.avg_call_duration_lost), self.calls_answered))
        print("Avg call dur: %s Longest wait (ans): %s Avg wait (ans): %s" %
              (convert_time_stamp(self.avg_call_duration_answered), convert_time_stamp(self.longest_answered_time),
               convert_time_stamp(self.avg_wait_calls_answered)))
        print("Duplicate calls found: %d voiceMails: %d removeAbandonGRP: %d" %
              (self.duplicates, self.voice_mails, self.calls_that_were_voice_mails))

    def print_ticker(self):
        print("Client # %s" % self.name)
        print("<15: %d <30: %d <45: %d" % (self.call_15sec, self.call_30sec, self.call_45sec))
        print("<60: %d >60: %d" % (self.call_60sec, self.call_g60sec))

    def reset(self):
        self.calls_answered = 0
        self.avg_call_duration_answered = 0
        self.avg_wait_calls_answered = 0
        self.longest_answered_time = 0
        self.calls_lost = 0
        self.avg_call_duration_lost = 0
        self.call_15sec = 0
        self.call_30sec = 0
        self.call_45sec = 0
        self.call_60sec = 0
        self.call_g60sec = 0
        self.duplicates = 0
        self.voice_mails = 0
        self.calls_that_were_voice_mails = 0
        self.twenty_four_hour = False
