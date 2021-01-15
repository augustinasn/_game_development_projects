
# Prerequisites:

from sys import exit
import datetime
import csv


# Classes and functions:

def validate_input(input_string):
    if input_string.isalpha():
        return input_string
    else:
        print("\n< Not a valid word - only alphabetical inputs are allowed. Remove spaces, special characters and numbers and try again.")
        return False

def check_dublicate(input_string, input_dict):
    if input_string.title() in input_dict.keys():
        return False
    else:
        return True

class Words:
    def __init__(self):
        self.w_dict = {}
        self.log = {}
        self.file_ready = True

    def load_words(self):
        try:
            input_w_file = csv.reader(open("data/words/words.txt", "r"))

        except:
            self.file_ready = False
            print("< File \"words.txt\" is not found in the data/words directory.")
            self.log[datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")] = "Unsuccesfully attempted to load \"words.txt\", file was not found"    

        else:
            for row in input_w_file:
                if row:
                    k, v = row
                    self.w_dict[k] = v
                else:
                    pass

            self.log[datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")] = " File \"words.txt\" successfuly loaded"

    def list_words(self):
        if self.w_dict:
            print("\n# Word, Hint")
            for entry in list(self.w_dict.keys()):
                print("-", entry, ':', self.w_dict[entry])
        else:
            print("\n- Empty.")

    def add_word(self):
        new_key = input("\n> Enter a word you'd like to add (use only alphabetical characters): ")
        new_hint = input("> Enter a one sentece hint for this word: ")

        if validate_input(new_key) and check_dublicate(new_key, self.w_dict):
            self.w_dict[new_key.title()] = new_hint.lower()
            self.log[datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")] = " Added to list: {} - {}.".format(new_key, new_hint)

            print("\n- A word \"{}\" with a hint - \"{}\" was added to the list of words.".format(new_key, new_hint))
        else:
            print("\n< Either there already is a \"{}\" entry in the list of words or the entry is not alphabetical.".format(new_key))
            self.add_word()

    def remove_word(self):
        print("\n- Words currently in the list:", ", ".join(list((self.w_dict).keys())))

        key_to_delete = input("\n> Enter the word that you'd like to delete: ")

        if not check_dublicate(key_to_delete, self.w_dict):
            del self.w_dict[key_to_delete.title()]
            print("\n< Word \"{}\" successfuly deleted from the list.".format(key_to_delete))
            self.log[datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")] = " Deleted from list: {}.".format(key_to_delete)

        else:
            print("\n< Word \"{}\" is not in the list - nothing to delete.".format(key_to_delete))
            self.remove_word()

    def unload_files(self):

        output_w_file = csv.writer(open("data/words/words.txt", "w"))
        output_log_file = csv.writer(open("logs/20" + datetime.datetime.now().strftime("%y-%m-%d %H-%M") + ".txt", "w"))

        for entry in list(self.w_dict.keys()):
            output_w_file.writerow([entry, self.w_dict[entry]])

        self.log[datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")] = " File \"words.txt\" successfuly exported"

        for entry in list(self.log.keys()):
            output_log_file.writerow([entry, self.log[entry]])


# Application runtime:

words_object = Words()
words_object.load_words()

print("\n" * 20)

while words_object.file_ready:
    user_input = input("\n> Enter a command (type 'help' for a list of possible options):  ")
    if user_input.lower() == "list" or user_input.lower() == "l" :
        words_object.list_words()

    elif user_input.lower() == "add" or user_input.lower() == "a":
        words_object.add_word()

    elif user_input.lower() == "remove" or user_input.lower() == "r":
        words_object.remove_word()

    elif user_input.lower() == "quit" or user_input.lower() == "q":
        if input("\n> Would you like to save the changes made? Y/N: ").lower() == "y":
            words_object.unload_files()
            exit() 
        else:
            exit()

    elif user_input.lower() == "help" or user_input.lower() == "h":
        print("\n- \"list\" / \"l\" - lists all current words;\n- \"add\" / \"a\" - to add a new entry to a word list;\n- \"remove\" / \"r\" - to remove an entry from word list;\n- \"quit\" / \"q\" - to quit the application.")

    else:
        print("\n< Not a valid command.")
