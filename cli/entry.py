#!/usr/bin/env python
import cli


cli = cli.Parser('terminator', description='foobar')


class login(cli.SubCommand):
  args = ['email', 'password']
  flags = ['verbose:v']
  kwargs = ['test:t']
  description = 'foo bar baz'
  
  def execute(self, email, password, verbose=None, test='thing'):
    print 'Login email:{} password:{} verbose:{} test:{}'.format(email, password, verbose, test)


def main():
  cli.autoparse()
