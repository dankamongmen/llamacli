import os
import cmd
import sys
import requests

payload = {
    'login': 'Login',
}

print(sys.argv)

try:
    payload['username'] = os.environ['LLAMA']
    payload['password'] = os.environ['PASSWORD']
except KeyError:
    print("please define environment variables LLAMA and PASSWORD")
    sys.exit(1)

ui = cmd.Cmd()

with requests.Session() as s:
    p = s.post('https://www.learnedleague.com/ucp.php?mode=login', data=payload)
    print(p.text)
    ui.cmdloop()
