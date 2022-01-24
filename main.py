#!/usr/bin/env python3
"""
This is a script to verify the accounts from bitwarden to check if the URI still exists.
"""

import json
import sys
import scripts.bitwarden as bw
import argparse
import pprint


class BitwardenScripts():
    def __init__(self, params):
        # set self.data to empty string
        self.data = None
        self.params = None
        self.version = None

        self.set_data("")
        # Store parameters
        self.set_params(params)
        self.set_version("1.0")

    def get_version(self):
        """This method will return the version"""
        return self.version

    def set_version(self, version):
        """This method will set the version"""
        self.version = version

    def get_params(self):
        """This method will return the parameters"""
        return self.params

    def get_data(self):
        """This method will return the data"""
        return self.data

    def set_data(self, data):
        """This method will set the data"""
        self.data = data

    def set_params(self, params):
        """This method will set the parameters"""
        self.params = params

    def parse_params(self):
        """This method will parse the parameters"""
        parser = argparse.ArgumentParser(
            description="This script will check the uri's from bitwarden")
        parser.add_argument("-f", "--file", help="Bitwarden export file to use", required=True)
        parser.add_argument("-c", "--check", action="store_true",
                            help="Check the uri's")
        parser.add_argument("-p", "--passwords", action="store_true",
                            help="Check the weak passwords")
        parser.add_argument("-V", "--version", action="version", version="0.0.1", help="Show version",
                            default=False)
        # self.params = parser.parse_args(self.get_params())
        self.params = parser.parse_args(self.get_params())

    def run(self):
        """This method will perform the actions the user has specified"""

        bw_checks = bw.Bitwarden(self.get_params().file)

        if self.get_params().check:
            bw_checks.check_all_uris()
            bw_checks.write_to_file()
        if self.get_params().passwords:
            bw_checks.check_weak_passwords()
            bw_checks.write_weak_pwd_to_file()
        if self.get_params().version:
            print(self.get_version())

if __name__ == "__main__":
    bwscripts = BitwardenScripts(sys.argv[1:])
    bwscripts.parse_params()
    bwscripts.run()
