#!/usr/bin/env python
from __future__ import print_function
import cli
import requests
import printutil


terminator = cli.group('terminator')


@terminator.command('login',
  args=['email', 'password'],
  flags=['verbose', 'remember'],
  kwargs=[])
def login(email, password, verbose=False, remember=False):
  ''' Logs a user in given a username and password '''
  if verbose: printutil.info('Sending login request')
  try:
    r = requests.post('https://mywebsite.com/api/login', json={"key": "value"})
  except requests.exceptions.SSLError:
    printutil.error('SSL Failed. Aborting')
    return
  if verbose: printutil.info('Login response received')
  if verbose: printutil.info('Login response status code: {}'.format(r.status_code))
  try:
    json = r.json()
    if verbose: printutil.info('Login response JSON correctly decoded')
  except ValueError:
    if verbose: printutil.error('Login response JSON incorrectly formatted')
    printutil.error('Login response was unreadable. Aborting')
    return
  print(json)
  printutil.info('Login successful')


@terminator.command('login',
  flags=['verbose'])
def login_from_remember(verbose=False):
  ''' Logs a user in based on their remembered credentials.
      This requires that you\'ve previously logged in using
      the --remember flag. '''
  login('test', 'this', verbose=verbose)


def main():
  terminator.autoparse()
