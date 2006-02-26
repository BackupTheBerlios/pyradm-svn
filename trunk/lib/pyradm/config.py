import pickle
import sys, os
from getopt import getopt, GetoptError

class ConfigException(Exception):
  """TODO"""

  def __init__(self, msg = "ConfigException"):

    self.__msg = msg

  def __repr__(self):

    return str(self.__msg)

class OptionsException(Exception):
  """TODO"""

  def __init__(self, msg = "OptionsException"):

    self.__msg = msg

  def __repr__(self):

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

  def __init__(self, fileName):
    """TODO"""

    self.__fileName = fileName

    try:

      self.load()
      
    except ConfigException:

      try:
        self['server'] = {}
        self['credentials'] = {}
        self['connection'] = {}
        self['sharedMB'] = {}

        self['server']['host'] = "imap.ric.cad.ru"
        self['server']['port'] = 993
        self['credentials']['user'] = "cyrus"
        self['credentials']['passwd'] = ""
        self['connection']['ssl'] = True

        self['sharedMB']['defaultACL'] = [("anyone", "p"), ("cyrus", "lrswipcda")]
        self['sharedMB']['defaultChildrens'] = ["spam"]

        self.save()

      except ConfigException:
        raise ConfigException("Can't create config file %s\n" % (self.__fileName))

  def load(self):
    """TODO"""

    try:
      f = file(self.__fileName)
      Config.__config__ = pickle.load(f)

    except IOError:
      raise ConfigException("Can't load config file %s" % (self.__fileName))

  def save(self):
    """TODO"""

    try:
    
      f = file(self.__fileName, "w")
      pickle.dump(Config.__config__, f)

    except IOError:
      raise ConfigException("Can't save config file %s" % (self.__fileName))

class Options:

  __options__ = {}

  def __setitem__(self, key, value):

    Options.__options__[key] = value

  def __getitem__(self, key):

    return Options.__options__[key]

  def __repr__(self):

    return str(Options.__options__)

  def __init__(self, args = sys.argv[1:]):
    """TODO"""

    try:
      options = getopt(args, "c:mh", ["config=", "maintain", "help"])
      
      self["config"] = os.getenv("HOME") + "/.pyradm"
      self["help"] = False
      self["maintain"] = False

      for option in options[0]:
        if option[0] in ["-c", "--config"]:
          self["config"] = option[1]
        elif option[0] in ["-h", "--help"]:
          self["help"] = True
        elif option[0] in ["-m", "--maintain"]:
          self["maintain"] = True

    except GetoptError, e:
      raise OptionsError(str(e))

# vim:ts=2:sw=2:et
