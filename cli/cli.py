from __future__ import print_function
import sys


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
    self.commands = []
    self._insert_help_command()
  
  def _insert_help_command(self):
    @self.command('help')
    def help():
      print('Help')
    
    @self.command('help', args=['command_name'])
    def help_with_command(command_name):
      print('Help {}'.format(command_name))
  
  def command(self, name, args=None, kwargs=None, flags=None):
    if not args: args = []
    if not kwargs: kwargs = []
    if not flags: flags = []
    def decorator(function):
      command = Command(name, function, args, kwargs, flags)
      self.commands.append(command)
      return function
    return decorator
  
  def autoparse(self):
    tokens = sys.argv[1:]
    return self.parse(tokens)
  
  def parse(self, tokens):
    for command in self.commands:
      if command.matches(tokens):
        command.parse(tokens)
        break
    else:
      self.parse(['help'])


group = CommandGroup
