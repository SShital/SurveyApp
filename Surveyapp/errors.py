class PasswordError(Exception):
    def __init__(self,msg):
        self.msg =msg

    def __str__(self):
        return self.msg

class InvaliPassword(PasswordError):
    pass

class PasswordchangedDayago(PasswordError):
    pass
