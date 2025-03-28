# decorator function
def input_error(expected_arg_count=None):
    
    # dictionary with possible errors
    error_messages = {
        "ValueError": "Please provide a valid name and phone number.",
        "IncorrectDataInput": "Please provide correct information: comand Name phone",
        "TypeError": "Invalid input type",
        "IndexError": "You did not provide arguments to proceed.",
        "NoNameError": "You did not provide name whos phone you want to see",
        "InvalidName": "Invalid format for name. Please use alphabetic characters only.",
        "InvalidPhone": "Invalid format for phone. Please use numeric characters only."
    }

    def decorator(func):
        def inner(*args, **kwargs):
            try:
                # checking arguments availability
                if not args:
                    raise IndexError(error_messages["IndexError"])
                if not args[0] and func.__name__ in ["show_phone"]:
                    raise ValueError(error_messages["NoNameError"])
                if expected_arg_count is not None and len(args[0]) != expected_arg_count:
                    if func.__name__ in ["add_contact", "change_contact"]:
                        raise ValueError(error_messages["IncorrectDataInput"])
                # checking additionaly some spesific functions
                if func.__name__ in ["add_contact", "change_contact"]:
                    if not args[0][0].isalpha():
                        raise ValueError(error_messages["InvalidName"])
                    if not args[0][1].isdigit():
                        raise ValueError(error_messages["InvalidPhone"])
                
                return func(*args, **kwargs)
            
            except Exception as e:
                return str(e)
        
        return inner
    
    return decorator
