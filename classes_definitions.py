from collections import UserDict
from datetime import datetime, date, timedelta


class Field:
    """
    Base class for record fields.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    """
    A class for storing a contact name. 
    """

class PhoneLengthError(Exception):
    def __init__(self, message='Must be 10 digits.'):
        self.message = message
        super().__init__(self.message)

class Phone(Field):
    """
    A class for storing a phone number.
    """
    def __init__(self, value):
        # The class has format validation (10 digits).
        if len(value) == 10:
            super().__init__(value)
        else:
            raise PhoneLengthError

    def __eq__(self, other):
        if not isinstance(other, Phone):
            return NotImplemented
        return self.value == other.value   
    
    def __str__(self):
        return f'{self.value}'
    
    def __repr__(self):
        return f'{self.value}'

class BirthdayFormatError(Exception):
    def __init__(self, message='Invalid date format. Use DD.MM.YYYY'):
        self.message = message
        super().__init__(self.message)

class Birthday(Field):
    """
    A class for storing a birthday.
    """
    def __init__(self, value: str):
        try:
            # Convert a date string in the format 'DD.MM.YYYY' to a datetime object.
            self.value = datetime.strptime(value, '%d.%m.%Y').date()
        except ValueError:
            raise BirthdayFormatError
    
    def __str__(self):
        return self.value.strftime('%d.%m.%Y')
    
    def __repr__(self):
        return self.value.strftime('%d.%m.%Y')

class Record:
    """
    A class for storing contact information, including name, phone list and birthday.
    """
    def __init__(self, name):
        self.name = Name(name)
        self.phones: list[Phone] = []
        self.birthday: Birthday = None

    def add_phone(self, phone: str) -> str:
        """
        Adding a phone.
        """
        message = 'Phone added.'
        try:
            new_phone = Phone(phone)
            if new_phone not in self.phones:
                self.phones.append(new_phone)
            else:
                message = 'Phone already exists.'
        except PhoneLengthError as excpt:
            message = f'Phone not added: {excpt}'
        return message

    def remove_phone(self, wanted_phone: str):
        """
        Deleting a phone.
        """
        self.phones.remove(Phone(wanted_phone))

    def edit_phone(self, old_phone: str, new_phone: str):
        """
        Editing a phone.
        """
        find_old_phone = False
        find_new_phone = False
        # Look for an old phone and a new phone.
        for phone in self.phones:
            if phone.value == old_phone:
                find_old_phone = True
            if phone.value == new_phone:
                find_new_phone = True

        # Inform about the result of the search. 
        # If everything is ok, then we change the phone.
        message = 'Phone changed.'
        if find_old_phone == False:
            message = 'The phone cannot be edited. An old phone is not in the list.'
        elif find_new_phone == True:
            if old_phone == new_phone:
                message = 'An old phone is equal to a new phone. The phone already exists.'
            else:
                self.remove_phone(old_phone)
                message = 'A new phone already exists. An old phone deleted.'
        else:
            message_of_add_phone = self.add_phone(new_phone)
            try:
                if message_of_add_phone != 'Phone added.':
                    raise PhoneLengthError
                else:
                    self.remove_phone(old_phone)
            except PhoneLengthError as excpt:
                message = f'Phone not changed: {excpt}'
        return message

    def find_phone(self, wanted_phone: str):
        """
        Phone search.
        """
        # We are looking for a phone.
        for phone in self.phones:
                if phone.value == wanted_phone:
                     wanted_phone = phone
                     break
        return wanted_phone if wanted_phone in self.phones else None
    
    def add_birthday(self, birthday: str):
        """
        Adding the birthday.
        """
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f'Contact name: {self.name.value}, ' + \
            f'phones: {"; ".join(phone.value for phone in self.phones)}, ' + \
            f'birthday: {self.birthday.value}'


class AddressBook(UserDict):
    """
    A class for storing and managing records.
    Object of the class has format {name1: info1, name2: info2, ... nameN: infoN}
    """
    def add_record(self, record: Record):
        """
        Adding a record.
        """
        self.data[record.name.value] = record

    def find(self, wanted_name: str):
        """
        Search a record by name.
        """
        result = [self.data[key] for key in self.data \
                  if self.data[key].name.value == Record(wanted_name).name.value]
        return result[0] if len(result) != 0 else None
    
    def delete(self, name: str):
        """
        Deleting a record by name.
        """
        self.data.pop(Record(name).name.value)

    def get_upcoming_birthdays(self, days=7) -> list:
        """
        Show birthdays for the next 7 days with dates when they should be congratulated.
        """
        upcoming_birthdays = []
        today = date.today()

        # key_name is Record(...).name.value
        for key_name in self.data:
            birthday_this_year = self.data[key_name].birthday.value.replace(year=today.year)
            # Add a check to see if the birthday will be next year already.
            if birthday_this_year < today:
                birthday_this_year = self.data[key_name].birthday.value.replace(year=today.year+1)

            if 0 <= (birthday_this_year - today).days < days:

                # Add the postponement of the greeting date to the next working day 
                # if the birthday falls on a weekend.
                def find_next_weekday(start_date, weekday):
                    days_ahead = weekday - start_date.weekday()
                    if days_ahead <= 0:
                        days_ahead += 7
                    return start_date + timedelta(days=days_ahead)
                
                def adjust_for_weekend(birthday: datetime) -> datetime:
                    if birthday.weekday() >= 5:
                        return find_next_weekday(birthday, 0)
                    return birthday
                
                if adjust_for_weekend(birthday_this_year) != birthday_this_year:
                    birthday_this_year = adjust_for_weekend(birthday_this_year)
                

                congratulation_date_str = birthday_this_year.strftime("%d.%m.%Y")
                upcoming_birthdays.append({'name': self.data[key_name].name.value, 
                                           'congratulation': Birthday(congratulation_date_str)
                                           })
        return upcoming_birthdays

    def __str__(self):
        result = 'Address Book\n'
        for record in self.data.values():
             result += (f'  Name: {record.name.value}, '
             f'phone(s): {"; ".join(phone.value for phone in record.phones) if record.phones else "unknown"}, '
             f'birthday: {record.birthday if record.birthday else "unknown"}\n')
        return result.strip()