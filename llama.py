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

llama = str.lower(payload['username'])

print(sys.argv)
print(llama)

class LLamaShell(cmd.Cmd):
    intro = 'LLama, taboot, taboot! "help" lists commands.\n'
    prompt = '[llcli] '
    def do_today(self, arg):
        print('go grab today\'s data')
    def do_exit(self, arg):
        return True

if __name__ == '__main__':
    with requests.Session() as s:
        p = s.post('https://www.learnedleague.com/ucp.php?mode=login', data=payload)
        # FIXME how to verify that we successfully logged in?
        r = s.get('https://learnedleague.com/profiles.php?' + llama)
        print(r.text)
        LLamaShell().cmdloop()
