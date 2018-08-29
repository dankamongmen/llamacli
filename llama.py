import os
import cmd
import sys
import requests

payload = {
    'login': 'Login',
}

try:
    payload['username'] = os.environ['LLAMA']
    payload['password'] = os.environ['PASSWORD']
except KeyError:
    print("please define environment variables LLAMA and PASSWORD")
    sys.exit(1)

ui = cmd.Cmd()

llama = str.lower(payload['username'])

print(sys.argv)
print(llama)

with requests.Session() as s:
    p = s.post('https://www.learnedleague.com/ucp.php?mode=login', data=payload)
    # FIXME how to verify that we successfully logged in?
    r = s.get('https://learnedleague.com/profiles.php?' + llama)
    print(r.text)
    ui.cmdloop()
