
class Session(object):
    STATUS_OPEN   = 'open'
    STATUS_CLOSED = 'closed'
    STATUS_DONE   = 'done'

    def __init__(self, session_id=None, status=None, participants=None, **kwargs):
        super().__init__()

        self.session_id   = session_id
        self.status       = status or Session.STATUS_OPEN
        self.participants = participants or []

    def to_dict(self):
        return {
            'session_id':   self.session_id,
            'status':       self.status,
            'participants': [p.to_dict() for p in self.participants]
        }

class Participant(object):
    def __init__(self, user_name):
        super().__init__()

        self.user_name = user_name

    def to_dict(self):
        return {
            'user_name':   self.user_name
        }
