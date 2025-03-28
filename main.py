from parser_inputed_line import parse_input
from functions_block import *
from classes_for_program import *
from context_manager import *

def main():
    #using context manager from contextlib to open and close file safely. Logic of the manager is in the separate file named context_manager.py
    with record_manager() as book:
        print("Welcome to the assistant bot!")
        while True:
            user_input = input("Enter a command: ")
            command, *args = parse_input(user_input)

            if command in ["close", "exit"]:
                print("Good bye!")
                break

            elif command == "hello":
                print("How can I help you?")

            elif command == "add":
                print(add_contact(args, book))

            elif command == "change":
                print(change_contact(args, book))
            
            elif command == "phone":
                print(show_phone(args, book))
            
            elif command == "all":
                print(show_all(book))
            
            elif command == "add-birthday":
                print(add_birthday(args, book))

            elif command == "show-birthday":
                print(show_birthday(args, book))

            elif command == "birthdays":
                print(birthdays(book))
            
            else:
                print("Invalid command.")

if __name__ == "__main__":
    main()
