#!/usr/bin/env python
import cli


terminator = cli.group('terminator')


@terminator.command('login',
  args=['email', 'password'],
  flags=['verbose'],
  kwargs=['test'])
def login(email, password, verbose=False, test='thing'):
  """ Logs a user in. """
  print('Login email:{} password:{} verbose:{} test:{}'
    .format(email, password, verbose, test))


def main():
  terminator.autoparse()
