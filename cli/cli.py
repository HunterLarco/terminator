__all__ = [
  'CommandGroup', 'Command', 'Parser',
  'group'
]


class Parser(object):
  def __init__(self, args, kwargs, flags):
    self.args = frozenset(args)
    self.kwargs = frozenset(kwargs)
    self.flags = frozenset(flags)
  
  def matches(self, tokens):
    ''' Returns true/false '''
  
  def parse(self, tokens):
    ''' Returns (args, kwargs, flags) '''
    pass


class CommandGroup(object):
  def __init__(self, name):
    self.name = name
  
  def command(self, name, args=None, kwargs=None, flags=None):
    def helper(function):
      pass
    return helper
  
  def autoparse(self):
    pass
  
  def parse(self, tokens):
    pass


class Command(object):
  def __init__(self, name, function, args, kwargs, flags):
    self.name = name
    self.function = function
    self.parser = Parser(args, kwargs, flags)
  
  def autoparse(self):
    pass
  
  def parse(self, tokens):
    ''' Returns true/false if executed or not '''
    pass


group = CommandGroup
