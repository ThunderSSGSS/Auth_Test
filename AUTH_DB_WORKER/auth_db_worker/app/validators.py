import re

class BaseValidator():
    regex=None #str

    def is_valid(self, data:str):
        if re.fullmatch(self.regex, data):
            return True
        return False

class EmailValidator(BaseValidator):
    regex=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'