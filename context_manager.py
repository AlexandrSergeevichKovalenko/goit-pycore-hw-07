from contextlib import contextmanager
from functions_block import load_data, save_data

#using context manager to operate safely 
@contextmanager
def record_manager():
    book = load_data()
    try:
        yield book
        # after yield the functions freezes and control goes to the main logic. 
        # After closing or unexpacted program interruption - finally block will run the function save_data() and close the file.  
    finally:
        save_data(book)
