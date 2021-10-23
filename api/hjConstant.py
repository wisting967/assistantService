import sys

class Const(object):
    class ConsError(TypeError):
        G_ERROR_UNKNOW = 'e001'

    class ConstCaseError(ConsError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise (self.ConsError, "Can't change const.%s" % name)
        if not name.isupper():
            raise (self.ConstCaseError, "const name '%s' is not all uppercase" % name)
        self.__dict__[name] = value

class GeneralErrorConst(Const):
    G_ERROR_UNKNOW = 'g001'

class DBErrorConst(Const):
    G_DB_ERROR = "-1"
    MY_SECOND_CONSTANT = 2
    MY_THIRD_CONSTANT = 'a'
    MY_FORTH_CONSTANT = 'b'

class UserErrorConst(Const):
    G_USER_NOLOGIN = 'u001'