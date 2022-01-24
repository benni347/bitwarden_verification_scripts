import json
import pprint
from datetime import datetime

from zxcvbn import zxcvbn
# import os
import urllib.request
import urllib.parse


class Bitwarden:
    def __init__(self, filename: str):
        self.pwd = None
        self.data = None
        self.good_request_codes = None
        self.set_good_request_codes([200, 201, 202, 203, 204, 202, 301, 302, 303, 307])
        with open(filename, "r") as f:
            self.set_data(json.load(f))
            self.set_pwd(self.get_data())
            f.close()

    def set_good_request_codes(self, codes):
        self.good_request_codes = codes

    def get_good_request_codes(self):
        return self.good_request_codes

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def set_pwd(self, pwd):
        self.pwd = pwd

    def get_pwd(self):
        return self.pwd

    def check_all_uris(self):
        good_items = []
        for item in self.data['items']:
            try:
                for uri in item['login']['uris']:
                    try:
                        if self.ping_uri(uri['uri']):
                            print("Found uri: " + uri['uri'])
                            good_items.append(item)
                        else:
                            print("uri not found: " + uri['uri'] + "\t" + item['name'])
                    except Exception as e:
                        print("Error: " + str(e))
                        print("uri not found 1: " + uri['uri'] + "\t" + item['name'])
                        # print("uri not found 1")
            except Exception as e:
                print("Error: " + str(e))
                print("uris not found 2")
        # self.set_data(self.get_data() | return_items)
        # pprint.pprint(return_items)
        data = self.get_data()
        data['items'] = good_items
        self.set_data(data)

    def ping_uri(self, uri):
        # if the uri has .onion, it's a tor uri and don't ping it
        uri_parsed = urllib.parse.urlparse(uri)

        # Skip "onion" and "androidapp:" uris
        if uri_parsed.hostname.split(".")[-1].lower() == "onion" or uri_parsed.scheme == "androidapp":
            return True

        try:
            req = urllib.request.Request(
                uri,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, '
                                  'like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
            )
            uri_response = urllib.request.urlopen(req, timeout=5)
            if uri_response.getcode() in self.get_good_request_codes():
                return True
        except IOError:
            return False
        except Exception:
            return False

    def check_weak_passwords(self):
        print("Checking for weak passwords can take time, please be patient.")
        weak_pwds = []
        for item in self.data['items']:
            try:
                pw = item['login']['password']
                results = zxcvbn(pw, user_inputs=[])
                if results['score'] != 4:  # calculate password entropy and if it's less than 4, it's weak
                    weak_pwds.append(item)
            except:
                pass
        pwd_data = self.get_pwd()
        pwd_data['items'] = weak_pwds
        self.set_pwd(pwd_data)

    def write_weak_pwd_to_file(self):
        filename = datetime.now().strftime("weak_pwd_%Y-%m-%d_%H-%M-%S.json")
        with open(filename, "w") as f:
            f.write(json.dumps(self.get_pwd(), indent=4, sort_keys=False))
            f.close()

    def write_to_file(self):
        # make a variable to hold the file name with date and time in iso-8601 format
        file_name = datetime.now().strftime("bitwarden_%Y-%m-%dT%H%M%S.json")
        # pprint.pprint(self.get_data())
        with open(file_name, "a", encoding="utf-8") as f:
            f.write(json.dumps(self.get_data(), indent=4, sort_keys=False))
            f.close()
