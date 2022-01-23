#!/usr/bin/env python3
"""
This is a script to verify the accounts from bitwarden to check if the URI still exists.
"""

import json
import sys


class main():
    def __init__(self):
        # set self.data to empty string
        self.data = ""

    def load_data(self, file_name: str):
        with open(file_name, 'r') as f:
            self.data = json.load(f)
        return self.data

    def action(self, action):
        """This method will ask the user what action to perform"""
        # format the input to lowercase and remove spaces and remove the '-' and '--'
        # cut it to only first letter
        action = action.lower().replace(' ', '').replace(
            '-', '').replace('--', '')[0]
        if action == "l":
            print("load a file")
        elif action == "c":
            self.check_uri()
        elif action == "p":
            print("Check for weak passwords")
        elif action == "L":
            print("Login to your account")
        else:
            print("This is the help menu")
            print("-h For this menu")
            print("-l Load a file")
            print("-c Check the uris")
            print("-p Check for weak passwords")
            print("-L To login to your account")

    def check_uri(self):
        for ci in self.data['items']:
            try:
                for uri in ci['login']['uris']:
                    try:
                        uri = uri['uri']
                        print(f"uri → {uri}")
                    except:
                        print("uri not found")
            except:
                print("uris not found")


if __name__ == "__main__":
    # ask the user for the file
    # file = input("Enter the file name: ")
    # append .json to file
    # file = file + ".json"
    # print(f"file → {file}")
    # pass the file to load_data
    # data = main().load_data(file)
    # call the main class
    main = main()
    if len(sys.argv) > 1:
        main.action(sys.argv[1])
    else:
        main.action("--help")
    # pass action_terminal to action
