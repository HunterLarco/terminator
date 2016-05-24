__all__ = ['Parse']


import sys


def SubCommandFactory(parser):
  class SubCommandMetaClass(type):
    def __init__(cls, name, bases, classdict):
      super(SubCommandMetaClass, cls).__init__(name, bases, classdict)
      parser._subcommands.append(cls)
  
  class SubCommand(object):
    __metaclass__ = SubCommandMetaClass
    
    args = None
    kwargs = None
    flags = None
    description = None
    
    def __init__(self):
      if not self.args: self.args = []
      if not self.kwargs: self.kwargs = []
      if not self.flags: self.flags = []
      if not self.description: self.description = []
    
    def execute(self):
      pass
    
    @classmethod
    def order(cls):
      pass
    
    @classmethod
    def matches(cls):
      pass
    
  return SubCommand


def HelpCommandFactory(SubCommand):
  def execute(self):
    pass
  
  helpcommand = type('help', (SubCommand,), {'execute': execute})
  return helpcommand


class Parser(object):
  # === Properties set by __init__ ===
  # _subcommands = []
  # _helpcommand
  # name
  # description
  # SubCommand
  
  def __init__(self, name, description=None):
    self._subcommands = []
    self.name = name
    self.description = description
    self.SubCommand = SubCommandFactory(self)
    self._helpcommand = HelpCommandFactory(self.SubCommand)
  
  def autoparse(self):
    args = sys.argv[1:]
    print(args)
  
  def parse(self, *args, **kwargs):
    for subcommand in self._subcommands:
      if subcommand.matches(*args, **kwargs):
        args, kwargs = subcommand.order(*args, **kwargs)
        subcommand().execute(*args, **kwargs)
        break
    else:
      self._helpcommand().execute()
  
  
