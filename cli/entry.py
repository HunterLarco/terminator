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
  ''' Logs a user in given an email address and password '''
  if verbose: printutil.info('Sending login request')
  try:
    r = requests.post('https://mywebsite.com/api/login', json={"key": "value"})
  except requests.exceptions.SSLError:
    printutil.error('SSL Failed. Aborting')
    return
  except requests.exceptions.ConnectionError:
    printutil.error('Could not form internet connection. Aborting')
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


@terminator.command('signup',
  args=['email'],
  flags=['verbose'])
def signup(email, verbose=False):
  ''' Signs up a new user given a email address '''
  printutil.info('Are you sure you want to signup with')
  printutil.info('the email address \'{}\'? (y/n) '.format(email), newline=False)
  try:
    signup_validated = printutil.yesno()
  except EOFError:
    # creates a newline since canceling the input
    # would mean newline was never added to stdin
    # so the warning message would be written inline
    # with the previous print statement
    print()
    printutil.warn('Input canceled. Aborting')
    return
  if not signup_validated:
    printutil.info('Signup canceled')
    return
  print('Please enter your account password')
  password = printutil.password()
  print('Please verify your account password')
  verification = printutil.password()
  if password != verification:
    printutil.warn('Your passwords did not match. Aborting')
    return
  try:
    r = requests.post('https://mywebsite.com/api/signup', json={"key": "value"})
  except requests.exceptions.SSLError:
    printutil.error('SSL Failed. Aborting')
    return
  except requests.exceptions.ConnectionError:
    printutil.error('Could not form internet connection. Aborting')
    return


def main():
  terminator.autoparse()
