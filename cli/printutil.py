from __future__ import print_function
import getpass


__all__ = [
  'info', 'warn', 'error',
  'PURPLE', 'BLUE', 'GREEN', 'YELLOW', 'RED', 'RESET', 'BOLD', 'UNDERLINE'
]


# Color constants
AQUA      = '\033[96m'
PURPLE    = '\033[95m'
BLUE      = '\033[94m'
GREEN     = '\033[92m'
YELLOW    = '\033[93m'
RED       = '\033[91m'
RESET     = '\033[0m'
BOLD      = '\033[1m'
UNDERLINE = '\033[4m'


def info(message, newline=True):
  print('{}[info]{} {}'.format(AQUA, RESET, message),
    end='\n' if newline else '')

def warn(message, newline=True):
  print('{}[warn]{} {}'.format(YELLOW, RESET, message),
    end='\n' if newline else '')

def error(message, newline=True):
  print('{}[erro]{} {}'.format(RED, RESET, message),
    end='\n' if newline else '')

def yesno():
  response = raw_input().lower()
  if response in ('yes', 'y'):
    return True
  elif response in ('no', 'n'):
    return False
  warn('Please respond (y/n) ', newline=False)
  return yesno()

def password():
  return getpass.getpass()