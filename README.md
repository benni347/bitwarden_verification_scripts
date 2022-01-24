# bitwarden_verification_scripts
## How to use?
Export the data from your bitwarden account and place it in the same directory. Then run main.py with the required parameters.

## Parameters
```
-h, --help displays the help menu
-f, --file which json file it should use.
-c, --check which will check the URI's from the export and it will bypass onion and anroidapp domains.
-p, --passwords will check for password that dont have a zxcvbn 4 score rating.
-V, --version displays the version.
```