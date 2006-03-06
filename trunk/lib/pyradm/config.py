__all__ = ["Config", "IOError", "ParseError"]

import pickle
import sys, os
from getopt import getopt, GetoptError

from pyradm import Options

class IOError(Exception):
  """TODO"""

  def __init__(self, msg = "Config.FileException"):

    self.__msg = msg

  def __str__(self):

    return str(self.__msg)

class ParseError(Exception):
  """TODO"""

  def __init__(self, msg = "Config.ParseException"):

    self.__msg = msg

  def __str__(self):

    return str(self.__msg)

class Config:
  """TODO"""

  __config = None
  __password = None

  def __setitem__(self, key, value):

    Config.__config[key] = value

  def __getitem__(self, key):

    return Config.__config[key]

  def __repr__(self):

    return str(Config.__config__)

  def __init__(self):
    """TODO"""

    if not Config.__config:
      Config.__config = {
        'default_server': None,
        'imap_servers': {}
      }

  def load(self):
    """TODO"""

    try:
      f = file(Options()['config'])
      Config.__config = pickle.load(f)

    except IOError:
      raise FileException("Can't load config file %s" % (Options()['config']))

  def save(self):
    """TODO"""

    try:
    
      f = file(Options()['config'], "w")
      pickle.dump(Config.__config, f)

    except IOError:
      raise FileException("Can't save config file %s" % (Options()['config']))

  def exists(self):
    """TODO"""

    try:
      file(Options()["config"]).close()
      exists = True
    except IOError:
      exists = False

    return exists

class Options:

  __options__ = None

  def __setitem__(self, key, value):

    Options.__options__[key] = value

  def __getitem__(self, key):

    return Options.__options__[key]

  def __repr__(self):

    return str(Options.__options__)

  def __init__(self):

    if not Options.__options__:
      Options.__options__ = {
        'config': os.getenv("HOME") + "/.pyradm",
        'help': False,
        'maintain': False
      }

  def getopt(self, args = sys.argv[1:]):
    """TODO"""

    try:
      options = getopt(args, "c:mh", ["config=", "maintain", "help"])
      
      for option in options[0]:
        if option[0] in ["-c", "--config"]:
          self['config'] = option[1]
        elif option[0] in ["-h", "--help"]:
          self['help'] = True
        elif option[0] in ["-m", "--maintain"]:
          self['maintain'] = True

    except GetoptError, e:
      raise OptionsException(str(e))

# vim:ts=2:sw=2:et
