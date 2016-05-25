__all__ = ['Parse']


import sys


def SubCommandFactory(parser):
  class SubCommandMetaClass(type):
    def __init__(cls, name, bases, classdict):
      super(SubCommandMetaClass, cls).__init__(name, bases, classdict)
      cls._init_cls()
      if cls.__name__ != 'SubCommand':
        parser._sub_commands[cls.__name__] = cls
  
  class SubCommand(object):
    __metaclass__ = SubCommandMetaClass
    
    args = None
    kwargs = None
    flags = None
    _kwarg_shortcuts = None
    _flag_shortcuts = None
    description = None
    
    @classmethod
    def _init_cls(cls):
      cls.description = [] if not cls.description else cls.description
      cls._load_arguments()
    
    @classmethod
    def _load_arguments(cls):
      if not cls.args: cls.args = []
      if not cls.flags: cls.flags = []
      if not cls.kwargs: cls.kwargs = []
      cls.flags, cls._flag_shortcuts, used = cls._load_shortcuts(cls.flags)
      cls.kwargs, cls._kwarg_shortcuts, _ = cls._load_shortcuts(cls.kwargs, used=used)
    
    @classmethod
    def _load_shortcuts(cls, args, used=None):
      primary_args = []
      arg_shortcuts = {}
      used = [] if not used else used[:]
      
      for arg in args:
        aliases = arg.split(':')
        primary = aliases[0]
        if primary in used:
          raise ValueError(
            '{} argument has been used in multiple locations'.format(primary))
        primary_args.append(primary)
        used.append(primary)
        if not ':' in arg: continue
        shortcuts = aliases[1:]
        for shortcut in shortcuts:
          if shortcut in used:
            raise ValueError(
              '{} argument has been used in multiple locations'.format(shortcut))
          arg_shortcuts[shortcut] = primary
          used.append(shortcut)
      
      return primary_args, arg_shortcuts, used
    
    def execute(self):
      pass
    
    @classmethod
    def order(cls, args):
      iterator = iter(args)
      arg_index = 0
      parsed_kwargs = { flag: False for flag in cls.flags }
      parsed_args = []
      
      for arg in iterator:
        if arg.startswith('-'):
          arg = arg.strip('-')
          if arg in cls._kwarg_shortcuts: arg = cls._kwarg_shortcuts[arg]
          if arg in cls._flag_shortcuts: arg = cls._flag_shortcuts[arg]
          if arg in cls.kwargs:
            try:
              value = iterator.next()
              if value.startswith('-'):
                raise Exception('Kwarg value cannot be another flag')
              parsed_kwargs[arg] = value
            except StopIteration:
              raise Exception('Kwarg missing value')
          elif arg in cls.flags:
            parsed_kwargs[arg] = True
          else:
            raise Exception('Flag not expected')
        else:
          if arg_index >= len(cls.args):
            raise Exception('Too many args')
          parsed_args.append(arg)
          arg_index += 1
      
      if len(parsed_args) != len(cls.args):
        raise Exception('Too few args')
      
      return parsed_args, parsed_kwargs
    
  return SubCommand


def HelpCommandFactory(SubCommand):
  def execute(self):
    pass
  
  helpcommand = type('help', (SubCommand,), {'execute': execute})
  return helpcommand


class Parser(object):
  # === Properties set by __init__ ===
  # _sub_commands = {}
  # _help_command
  # name
  # description
  # SubCommand
  
  def __init__(self, name, description=None):
    self._sub_commands = {}
    self.name = name
    self.description = description
    self.SubCommand = SubCommandFactory(self)
    self._help_command = HelpCommandFactory(self.SubCommand)
  
  def autoparse(self):
    args = sys.argv[1:]
    arg_string = ' '.join(args)
    return self.parse(arg_string)
  
  def parse(self, arg_string):
    raw_args = arg_string.split(' ') if arg_string.strip() else []
    command_name = raw_args[0]
    args = raw_args[1:]
    
    if not command_name in self._sub_commands:
      self._help_command().execute()
      return
    
    sub_command = self._sub_commands[command_name]
    args, kwargs = sub_command.order(args)
    sub_command().execute(*args, **kwargs)
  
  
