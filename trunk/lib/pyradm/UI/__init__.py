__all__ = ["CLI"]

from string import split, strip
from pyIMAP import IMAPError
from pyradm.Config import Config
import readline
import handlers

    
class CLI:
  """TODO"""

  imapServer = None
  __commands__ = None

  def __init__(self):
    """TODO"""

    if not CLI.__commands__:
      CLI.commands["logout"] = handlers.logout)
      CLI.commands["quit"] = handlers.logout)
      CLI.commands["createshared"] = handlers.createShared)
      CLI.commands["cs"] = handlers.createShared)
      CLI.commands["deleteshared"] = handlers.deleteShared)
      CLI.commands["ds"] = handlers.deleteShared)
      CLI.commands["setacl"] = handlers.setACL)
      CLI.commands["sa"] = handlers.setACL)
      CLI.commands["getacl"] = handlers.getACL)
      CLI.commands["ga"] = handlers.getACL)
      CLI.commands["getperm"] = handlers.getPerm)
      CLI.commands["gp"] = handlers.getPerm)
      CLI.commands["setperm"] = handlers.setPerm)
      CLI.commands["sp"] = handlers.setPerm)
      #CLI.commands("createuser", "cu", handlers.createUser)
      #CLI.commands("cu", handlers.createUser)

  def __getHandler(self, command):
    """TODO"""

    cmd = filter(lambda c: (c['name'] == command) or (c['alias'] == command), self.__commands)
    if len(cmd) == 1 :
      return cmd[0]['handler']
    else:
      return None
    
  def run(self):
    """TODO"""

    if Config().exists():
      Config().setPassword(self.askPassword())
      Config().load()

      if Config()['default_server'] and not Options()['maintain']:
        CLI.imapServer = handlers.connectIMAPServer(Config()['default_server'])
    else:
      if yes("Config file %s not exists.\nCreate one?"):
        Config().setPassword(self.newPassword())
        Config().save()
      else:
        raise pyradm.Abort()

    self.setPrompt()

    try:
      while True:
        
        line = self.read
        args = split(s = line, maxsplit = 1)
        
        if len(args) > 0:
          if len(args) < 2: args.append("")
          handler = self.__getHandler(args[0])
          if handler:
            try:
              handler(self.__imapAdmin, strip(args[1]))
            except IMAPError, e:
              print "ERROR: " + str(e)
          else:
            print "ERROR: unknown command '" + args[0] + "'"
    except handlers.Logout:
      pass

# vim:ts=2:sw=2:et
