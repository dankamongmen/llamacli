import re
import os
import cmd
import sys
import requests
import html.parser

payload = {
    'login': 'Login',
}

try:
    payload['username'] = os.environ['LLAMA']
    payload['password'] = os.environ['PASSWORD']
except KeyError:
    print("please define environment variables LLAMA and PASSWORD")
    sys.exit(1)

class LLamaShell(cmd.Cmd):
    def __init__(self, session):
        cmd.Cmd.__init__(self)
        self.session = session

    intro = 'LLama, taboot, taboot! "help" lists commands.\n'
    prompt = '[' + payload['username'] + '] '
    def do_md(self, arg):
        args = arg.split()
        if len(args) != 2:
            print('usage: md <season> <day>')
            return False
        md = s.get('https://learnedleague.com/match.php?' + args[0] + '&' + args[1])
        print(md.text)

    def do_today(self, arg):
        print('go grab today\'s data')

    def do_quit(self, arg):
        return True

    def do_exit(self, arg):
        return True

class MDParser(html.parser.HTMLParser):
    checkdata = False
    checklabel = False
    gotlabel = False
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            for attr in attrs:
                if attr[0] == 'class' and attr[1] == 'current-label':
                    self.checklabel = True
        if tag == 'a':
            self.checkdata = True
    def handle_data(self, data):
        if self.checklabel:
            if data == 'LearnedLeague':
                self.gotlabel = True
            else:
                self.gotlabel = False
        if self.gotlabel and self.checkdata:
            if re.match('LL\\d\\d', data):
                print(data) #FIXME stash this
            elif re.match('Match Day', data):
                print(data) #FIXME stash this
    def handle_endtag(self, tag):
        if tag == 'div' or tag == 'a':
            self.checkdata = False
            self.checklabel = False

if __name__ == '__main__':
    llama = str.lower(payload['username'])
    with requests.Session() as s:
        hpage = s.get('https://learnedleague.com/')
        MDParser().feed(hpage.text)
        p = s.post('https://www.learnedleague.com/ucp.php?mode=login', data=payload)
        #print(p.status_code)
        #print(p.headers)
        # FIXME how to verify that we successfully logged in?
        r = s.get('https://learnedleague.com/profiles.php?' + llama)
        #print(r.text)
        #print(r.status_code)
        #print(r.headers)
        LLamaShell(s).cmdloop()
