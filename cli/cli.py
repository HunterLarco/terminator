from __future__ import print_function
import sys
from collections import defaultdict


__all__ = [
  'CommandGroup', 'Command',
  'Parser', 'BasicTokenIterator', 'TokenIterationException',
  'group'
]


class TokenIterationException(Exception):
  pass


class BasicTokenIterator(object):
  def __init__(self, args, kwargs, flags, tokens):
    self.args = iter(args)
    self.kwargs = kwargs
    self.flags = flags
    self.tokens = iter(tokens)
  
  def __iter__(self):
    return self
  
  def __next__(self):
    token = self._get_next_token()
    if token.startswith('-'):
      token = token.strip('-')
      return self._parse_optional(token)
    return self._parse_argument(token)
  next = __next__
  
  def _get_next_token(self):
    try:
      token = self.tokens.next()
    except StopIteration:
      self._verify_completion()
      raise
    return token
  
  def _verify_completion(self):
    try:
      next_arg = self.args.next()
      raise TokenIterationException('Argument not provided {}'.format(next_arg))
    except StopIteration:
      pass
  
  def _parse_optional(self, token):
    if token in self.flags:
      return token, self._parse_flag(token)
    elif token in self.kwargs:
      return token, self._parse_kwarg(token)
    else:
      raise TokenIterationException('Unknown flag {}'.format(token))
  
  def _parse_flag(self, token):
    return True
  
  def _parse_kwarg(self, token):
    try:
      value = self.tokens.next()
    except StopIteration:
      raise TokenIterationException('Keyword Argument without a value {}'.format(token))
    return value
  
  def _parse_argument(self, token):
    try:
      arg = self.args.next()
    except StopIteration:
      raise TokenIterationException('Unexpected argument {}'.format(token))
    return arg, token


class Parser(object):
  TokenIterator = BasicTokenIterator
  
  def __init__(self, args, kwargs, flags):
    self.args = frozenset(args)
    self.kwargs = frozenset(kwargs)
    self.flags = frozenset(flags)
  
  def describe(self):
    args = ('<{}>'.format('> <'.join(self.args))
      if self.args else '')
    kwargs = ('--{} <value>'.format(' -- <value>'.join(self.kwargs))
      if self.kwargs else '')
    flags = ('--{}'.format(' --'.join(self.flags))
      if self.flags else '')
    return ' '.join(filter(None, [args, kwargs, flags]))
  
  def matches(self, tokens):
    ''' Returns true/false '''
    iterator = self.TokenIterator(self.args, self.kwargs, self.flags, tokens)
    try:
      list(iterator)
      return True
    except TokenIterationException:
      return False
  
  def parse(self, tokens):
    ''' Returns (args, kwargs, flags) '''
    parsed_args = []
    parsed_kwargs = {}
    parsed_flags = {}
    
    iterator = self.TokenIterator(self.args, self.kwargs, self.flags, tokens)
    for token, value in iterator:
      if token in self.args:
        parsed_args.append(value)
      elif token in self.kwargs:
        parsed_kwargs[token] = value
      elif token in self.flags:
        parsed_flags[token] = value
    
    return parsed_args, parsed_kwargs, parsed_flags


class Command(object):
  def __init__(self, name, function, args, kwargs, flags):
    self.name = name
    self.function = function
    self.parser = Parser(args, kwargs, flags)
  
  def describe(self):
    docstr = self.function.__doc__
    if not docstr: docstr = '<Missing Documentation>'
    docstr = '\n'.join(['> {}'.format(line.strip()) for line in docstr.split('\n')])
    parserstr = self.parser.describe()
    return '{} {}\n{}'.format(self.name, parserstr, docstr)
  
  def matches(self, tokens):
    if len(tokens) == 0 or not self.name == tokens[0]:
      return False
    return self.parser.matches(tokens[1:])
  
  def parse(self, tokens):
    ''' Returns true/false if executed or not '''
    args, kwargs, flags = self.parser.parse(tokens[1:])
    combined_kwargs = dict(kwargs.items() + flags.items())
    self.function(*args, **combined_kwargs)


class CommandGroup(object):
  def __init__(self, name):
    self.name = name
    self.commands = defaultdict(list)
    self._insert_help_command()
  
  def _insert_help_command(self):
    @self.command('help')
    def help():
      ''' Provides information about each function '''
      print()
      print('Run \'help <command>\' for more information on a specific command')
      print('[ Commands ]')
      for command_name in self.commands:
        print('    {}'.format(command_name))
      print()
    
    @self.command('help', args=['command_name'])
    def help_with_command(command_name):
      ''' Provides information about a specific function '''
      if not command_name in self.commands:
        print('\nCommand \'{}\' not found\nTry running help for more info\n'
          .format(command_name))
      else:
        print()
        command = self.commands[command_name]
        for signature in command:
          print(signature.describe())
          print()
  
  def command(self, name, args=None, kwargs=None, flags=None):
    if not args: args = []
    if not kwargs: kwargs = []
    if not flags: flags = []
    def decorator(function):
      command = Command(name, function, args, kwargs, flags)
      self.commands[name].append(command)
      return function
    return decorator
  
  def autoparse(self):
    tokens = sys.argv[1:]
    return self.parse(tokens)
  
  def parse(self, tokens):
    if len(tokens) > 0:
      command_name = tokens[0]
      command = self.commands[command_name]
      for signature in command:
        if signature.matches(tokens):
          signature.parse(tokens)
          return
    self.parse(['help'])
    

group = CommandGroup
