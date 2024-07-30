from classes_definitions import *


def parse_input(user_input: str):
    """
    Parse the string entered by the user into a command and its arguments.
    """
    # Arguments may consist of username, phone.
    command, *args = user_input.split()
    command = command.strip().lower()
    return command, *args



# Begin decorators definition.

def input_error_add_contact(func):
    """
    Add exeptions to the function add_contact().
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            print('Error. Give me a name and a phone please.')
        except IndexError:
            print('Error. Give me a name please.')
        except KeyError:
            print('Error. No such contact exists.')
    return inner

def input_error_change_contact(func):
    """
    Add exeptions to the function change_contact().
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            print('Error. Give me an existing name, and old phone and a new phone please.')
        except AttributeError:
            print('Error. Give me an existing name please.')
    return inner

def input_error_show_phone(func):
    """
    Add exeptions to the function show_phone().
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            print('Error. Give me an existing name and a phone please.')
        except AttributeError:
            print('Error. Give me an existing name please.')
        except KeyError:
            print('Error. No such contact exists.')
    return inner

def input_error_add_birthday(func):
    """
    Add exeptions to the function add_birthday().
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, AttributeError):
            print('Error. Give me an existing name and birthday please.')
        except BirthdayFormatError as excpt:
            print(excpt)
    return inner

def input_error_show_birthday(func):
    """
    Add exeptions to the function show_birthday().
    """
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, AttributeError):
            print('Error. Give me an existing name please.')
    return inner

# End decorators definition.



@input_error_add_contact
def add_contact(args, book: AddressBook):
    """
    The function adds the contact.
    """
    name, phone, *_ = args
    record = book.find(name)
    message = 'Contact updated.'
    # Check the presence of a contact.
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = 'Contact added.'
    message_of_add_phone = record.add_phone(phone)
    return message if message_of_add_phone == 'Phone added.' else message_of_add_phone

@input_error_change_contact
def change_contact(args, book: AddressBook):
    """
    The function changes the contact.
    """
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    message = 'Contact updated.'
    message_of_edit_phone = record.edit_phone(old_phone, new_phone)
    return message if message_of_edit_phone == 'Phone changed.' else message_of_edit_phone

@input_error_show_phone
def show_phone(args, book: AddressBook):
    """
    The function show list of phone numbers.
    """
    name, *_ = args
    record = book.find(name)
    print(record.phones)

@input_error_add_birthday
def add_birthday(args, book: AddressBook):
    """
    The function adds the birthday.
    """
    name, birthday, *_ = args
    record = book.find(name)
    message = 'Birthday added.'
    record.add_birthday(birthday)
    print(message)

@input_error_show_birthday
def show_birthday(args, book: AddressBook):
    """
    Show birthday for the contact.
    """
    name, *_ = args
    record = book.find(name)
    print(record.birthday if record.birthday else 'unknown')

def birthdays(book: AddressBook):
    """
    Show birthdays for the next 7 days with dates when they should be congratulated.
    """
    return book.get_upcoming_birthdays()
