import re

class BaseValidator():
    regex=None #str

    def is_valid(self, data:str):
        if re.fullmatch(self.regex, data):
            return True
        return False

class EmailValidator(BaseValidator):
    regex=r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

class PasswordValidator(BaseValidator):
    regex=r'[A-Za-z0-9@#$%^&+=]{8,}'


def is_altered(object, new_data):
    altered=False
    #check email
    if new_data.email is not None:
        altered=True
    else:
        new_data.email = object.email

    #check is_staff
    if new_data.is_staff is not None:
        if object.is_staff != new_data.is_staff:
            altered=True
    else:
        new_data.is_staff = object.is_staff

    #check is_active
    if new_data.is_active is not None:
        if object.is_active != new_data.is_active:
            altered=True
    else:
        new_data.is_active = object.is_active

    #check is_complete
    if new_data.is_complete is not None:
        if object.is_complete != new_data.is_complete:
            altered=True
    else:
        new_data.is_complete = object.is_complete

    return altered