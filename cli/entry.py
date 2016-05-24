#!/usr/bin/env python
import cli


cli = cli.Parser('terminator', description='foobar')


class login(cli.SubCommand):
  args = ['email', 'password']
  flags = ['verbose']
  kwargs = ['test']
  description = 'foo bar baz'
  
  def __call__(email, password, verbose=None, test='thing'):
    pass


def main():
  cli.autoparse()
