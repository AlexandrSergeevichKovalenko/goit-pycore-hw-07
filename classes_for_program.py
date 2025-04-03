from collections import UserDict
from datetime import datetime, date, timedelta
import re
from pathlib import Path

#global variable(name of the file) for storaging all programm progress 
FILENAME = Path("addressbook.pkl")

class Field:
    def __init__(self, value):
      self.value = value

    def __str__(self):
      return str(self.value)

class Birthday(Field):
    def __init__(self, value):
        pattern = r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.\d{4}$"
        if re.fullmatch(pattern, value):
            format = "%d.%m.%Y"
            self.value = datetime.strptime(value, format)
        else:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Name(Field):
	pass

class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    #create a function to validate the phone number.
    @staticmethod
    def validate(number):
        return True if number.isdigit() and len(number) == 10 else False

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    # adding birthday date to the contact (validity of data is checked in the __init__ of Birthday class)
    def add_birthday(self, data: str):
        self.birthday = Birthday(data)

    #if phone is validated, create an Phone instance and add it to the phones in case validation fails - raise an error 
    def add_phone(self, phone_number: str):
        phone = Phone(phone_number)
        self.phones.append(phone)
    
    #remooving phone from the phones
    def remove_phone(self, phone_number: str):
        self.phones = [phone for phone in self.phones if phone.value !=phone_number]

    #editing a phone number, or raising the ValueError in case does not exist 
    def edit_phone(self, old_number: str, new_number: str):
        if not Phone.validate(new_number):
            raise ValueError("The new phone number is not valid. Please enter a valid 10-digit number.")
       
        for phone in self.phones:
            if phone.value == old_number:
                phone.value = new_number
                return
        raise ValueError("The phone number you entered does not exist")

    #finding a phone by its number
    def find_phone(self, num_phone:str):
        for phone in self.phones:
            if phone.value == num_phone:
                return phone
        raise ValueError("The number was not found")

    def __str__(self):
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "N/A"
        phones_string = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones_string}, birthday: {birthday_str}"


class AddressBook(UserDict):

    #adding a record to the dictionary 
    def add_record(self, note: Record):
        self.data[note.name.value] = note

    #return Record object 
    def find(self, name: str) -> Record:
        if name in self.data:
            return self.data[name]
        return None

    def delete(self, name:str) -> None:
        if name in self.data:
            del self.data[name]
    
    #def string_to_date(date_string):
        #return datetime.strptime(date_string, "%Y.%m.%d").date()

    @staticmethod
    def date_to_string(date):
        return date.strftime("%d.%m.%Y")

    @staticmethod
    def find_next_weekday(start_date, weekday):
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)

    @staticmethod
    def adjust_for_weekend(birthday):
        if birthday.weekday() >= 5:
            return AddressBook.find_next_weekday(birthday, 0)
        return birthday

    # Determining, who should be congratulated.
    def get_upcoming_birthdays(self, days=7):
        upcoming_birthdays = []
        today = date.today()

        for user, dict_record in self.data.items():
            #the first is to check if the dict_record object:Record has something in attribute birthday(it can happen, 
            # that there is a name and a phone, but there is no birthday date entered by user)
            if dict_record.birthday:
                birthday_this_year = dict_record.birthday.value.replace(year=today.year).date()
                if birthday_this_year < today:
                    birthday_this_year = dict_record.birthday.value.replace(year=today.year + 1).date() 

                if 0 <= (birthday_this_year - today).days <= days:
                    congratulation_date = AddressBook.adjust_for_weekend(birthday_this_year)
                    upcoming_birthdays.append({"name": user, "birthday": AddressBook.date_to_string(congratulation_date)})
        return upcoming_birthdays


    #str method is created to output the content in an understandable way
    def __str__(self):
        output = ["AddressBook: "]
        for key in self.data:
            contact_description_line = (f"name: {self.data[key].name.value}, phones: {'; '.join(phone.value for phone in self.data[key].phones)}")
            output.append(contact_description_line)
        total_info_line = "\n".join(output)
        return total_info_line

    
    