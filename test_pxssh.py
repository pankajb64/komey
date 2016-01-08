#!/usr/bin/env python2.7
import os
import sys
from pxssh import pxssh as PXSSH
import getpass


class Debug_PXSSH(PXSSH):

    def sendline(self, input=''):
        sys.stderr.write('\n[sendline::input={!r}]'.format(input))
        return PXSSH.sendline(self, input)

    def try_read_prompt(self, timeout_multiplier):
        prompt = PXSSH.try_read_prompt(self, timeout_multiplier)
        sys.stderr.write('\n[try_read_prompt::prompt={!r}]'.format(prompt))
        sys.stderr.flush()
        return prompt

    def sync_original_prompt (self, sync_multiplier=1.0):
        from pexpect import TIMEOUT
        import time
        sys.stderr.write('\n[sync_original_prompt]')
        sys.stderr.flush()
        self.sendline()
        time.sleep(0.1)
        try:
            self.try_read_prompt(sync_multiplier)
        except TIMEOUT:
            pass
        self.sendline()
        x = self.try_read_prompt(sync_multiplier)
        self.sendline()
        a = self.try_read_prompt(sync_multiplier)
        self.sendline()
        b = self.try_read_prompt(sync_multiplier)
        ld = self.levenshtein_distance(a,b)
        len_a = len(a)
        if len_a == 0:
            sys.stderr.write('\n[len_a=0]')
            return False
        val = float(ld)/len_a
        sys.stderr.write('\n[val={}, ld={}, len_a={}]\n'
                         .format(val, ld, len_a))
        sys.stderr.flush()
        if val < 0.4:
            return True
        sys.stderr.write('\n[! distance too far:'
                         '\n{!r}\n{!r}]\n'.format(a, b))
        sys.stderr.flush()
        return False


# setup variables
username = os.environ['USER']
hostname = raw_input('hostname: ')
username = raw_input('username [{}]: '.format(username)).strip() or username
port = int(raw_input('port [22]: ').strip() or '22')
password = getpass.getpass('password: ')

# create and begin session,
session = Debug_PXSSH()
session.login(hostname, username, password, port)
session.sendline('uptime')
session.prompt()
sys.stderr.write('\n[session.before={!r}]'.format(session.before))
session.logout()
sys.stderr.write('\n')
