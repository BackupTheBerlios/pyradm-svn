__all__ = ["Config", "FileException", "Options", "OptionsException"]

import pickle
import sys, os
from getopt import getopt, GetoptError

class FileException(Exception):
  """TODO"""

  def __init__(self, msg = "Config.FileException"):

    self.__msg = msg

  def __str__(self):

    return str(self.__msg)

class ParseException(Exception):
  """TODO"""

  def __init__(self, msg = "Config.ParseException"):

    self.__msg = msg

  def __str__(self):

    return str(self.__msg)

class OptionsException(Exception):
  """TODO"""

  def __init__(self, msg = "Config.OptionsException"):

    self.__msg = msg

  def __str__(self):

    return str(self.__msg)

class Config:
  """TODO"""

  __config__ = {}

  def __setitem__(self, key, value):

    Config.__config__[key] = value

  def __getitem__(self, key):

    return Config.__config__[key]

  def __repr__(self):

    return str(Config.__config__)

  def __init__(self):
    """TODO"""

    if not Config.__config__:
      Config.__config__ = {}

  def load(self):
    """TODO"""

    try:
      f = file(self.__fileName)
      Config.__config__ = pickle.load(f)

    except IOError:
      raise FileException("Can't load config file %s" % (self.__fileName))

  def save(self):
    """TODO"""

    try:
    
      f = file(self.__fileName, "w")
      pickle.dump(Config.__config__, f)

    except IOError:
      raise FileException("Can't save config file %s" % (self.__fileName))

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
