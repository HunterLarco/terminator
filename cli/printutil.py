from __future__ import print_function


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


def info(message):
  print('{}[info]{} {}'.format(AQUA, RESET, message))

def warn(message):
  print('{}[warn]{} {}'.format(YELLOW, RESET, message))

def error(message):
  print('{}[erro]{} {}'.format(RED, RESET, message))
