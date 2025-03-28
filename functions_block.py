from decor import input_error
from classes_for_program import *

"""
Here are functions whose names clearly matches their logic.

"""
@input_error(expected_arg_count=2)
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error(expected_arg_count=3)
def change_contact(args, book: AddressBook):
    name, old_number, new_number, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(old_number, new_number)
        return "Contact updated."
    else:
        return f"There is no person with {name} name"

@input_error(expected_arg_count=1)
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    phone_result = f"{name}'s phone is "
    if record:
        for r in record.phones:
            phone_result += f"{r.value} "
        return phone_result
    else:
        return f"The name {name} you have asked for does not exist."
    
def show_all(book: AddressBook):
    if len(book.data) != 0:
        return str(book)
    else:
        return "There is no data to output."

@input_error(expected_arg_count=2)
def add_birthday(args, book):
    name, birthday_day, *_ = args
    message = "Birthday adedd."
    record = book.find(name)

    if record is None:
        return f"There is no person with {name} name"
    
    # to be sure that a user will not enter date, which is not exist, like 31.02.2020 (there is a check in __init__, but only for the correct format of an inputted data).
    try:
        record.add_birthday(birthday_day)
        return message
    except ValueError as e:
        return str(e)

@input_error(expected_arg_count=1)
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return f"There is no person with {name} name."
    else:
        if record.birthday is not None:
            return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}"
        else:
            return f"{name} does not have a birthday set."

# forming a string of names of the persons, who should be congratulated and their respective birthday dates.
def birthdays(book):
    str = ""
    if len(book.get_upcoming_birthdays()) != 0:
        for i in book.get_upcoming_birthdays():
            str += f"{i}\n"
        return str
    else:
        return f"The data base is empty."









