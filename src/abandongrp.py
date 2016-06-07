# Contains client class which contains summed/averaged data from each spreadsheet


class AbandonGrp:

    def __init__(self):
        self.call_id = 0
        self.internal_party = 0
        self.external_party = 0
        self.bool_answered = False
        self.start_time = 0
        self.end_time = 0
        self.call_duration = 0

    def __hash__(self):
        return self.call_id

    def __eq__(self, right_hand_comparison):
        return self.call_id == right_hand_comparison.call_id

    def __str__(self):
        print("self.call_id: %s" % self.call_id)
        print("self.internal_party: %s" % self.internal_party)
        print("self.external_party: %s" % self.external_party)
        print("self.start_time: %s" % self.start_time)
        print("self.bool_answered: %r" % self.bool_answered)
        print("self.call_duration: %s" % self.call_duration)
        print("self.end_time: %s" % self.end_time)
   
    def set_call(self, call_id, internal_party, external_party,
                 bool_answered, start_time, end_time, call_duration):
        self.call_id = call_id
        self.internal_party = internal_party
        self.external_party = external_party
        self.bool_answered = bool_answered
        self.start_time = start_time
        self.end_time = end_time
        self.call_duration = call_duration

    def get_internal_party(self):
        return self.internal_party
    
    def get_call_id(self):
        return self.call_id
    
    def get_external_party(self):
        return self.external_party
    
    def get_bool_answered(self):
        return self.bool_answered
    
    def get_start_time(self):
        return self.start_time
    
    def get_end_time(self):
        return self.end_time
    
    def get_call_duration(self):
        return self.call_duration

