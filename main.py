import pickle
from classes_definitions import *
from functions_definitions import *

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено

def main():
    # Create dictionary of contacts.
    book = load_data()
    print('Welcome to the assistant bot!')
    while True:
        # Print "Menu".
        print('Please select one of the following commands.\n\
              - Input "Hello" to greet the assistant!\n\
              - Imput "add [name] [phone]" to add a phone.\n\
              - Input "change [name] [old phone] [new phone]" to change a phone.\n\
              - Input "phone [name]" to print list of phones.\n\
              - Input "add-birthday [name] [birthday]" to add the birthday in the format "DD.MM.YYYY".\n\
              - Input "show-birthday [name]" to show the birthday.\n\
              - Input "birthdays" to show birthdays for the next 7 days\n\
                with dates when they should be congratulated.\n\
              - Input "all" to print all saved contacts.\n\
              - If you want to complete the work with the assistant, then input "close" or "exit".')
        user_input = input('Enter a command: ')
        # Parse the string entered by the user into a command and its arguments.
        command, *args = parse_input(user_input) 

        # React to the command.
        match command:

            # Input "Hello" to greet the assistant!
            case 'hello':
                print('How can I help you?')
            
            # Imput "add [name] [phone]" to add a phone.
            case 'add':
                message_of_add = add_contact(args,book)
                if message_of_add:
                    print(message_of_add)
            
            # Input "change [name] [old phone] [new phone]" to change a phone.
            case 'change':
                message_of_change = change_contact(args,book)
                if message_of_change:
                    print(message_of_change)

            # Input "phone [name]" to print list of phones.
            case 'phone':
                show_phone(args,book)

            # Input "add-birthday [name] [birthday]" to add the birthday in the format "DD.MM.YYYY".
            case 'add-birthday':
                add_birthday(args, book)

            # Input "show-birthday [name]" to show the birthday.
            case 'show-birthday':
                show_birthday(args, book)

            # Input "birthdays" to show birthdays for the next 7 days
            # with dates when they should be congratulated.
            case 'birthdays':
                print(birthdays(book))
            
            # Input "all" to print all saved contacts.
            case 'all':
                print(book)
            
            # If you want to complete the work with the assistant, then input "close" or "exit".
            case 'close' | 'exit':
                print('Good bye!')
                save_data(book)
                break
            
            # Another case.
            case _:
                print('Invalid command.')

if __name__ == '__main__':
    main()
