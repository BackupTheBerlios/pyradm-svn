__all__ = ["CLI"]

from string import split, strip
from pyIMAP import IMAPError
from pyradm.Config import Config
import readline
import handlers

class CLI:
  """TODO"""

  def __init__(self, imapAdmin = None, config = None):
    """TODO"""

    self.__config = Config()
    self.__imapAdmin = imapAdmin
#    self.__prompt = Config()['credentials']['user'] + "@" + config['server']['host'] + ": "
    self.__commands = []

    self.command("logout", "quit", handlers.logout)
    self.command("createshared", "cs", handlers.createShared)
    self.command("deleteshared", "ds", handlers.deleteShared)
    self.command("setacl", "sa", handlers.setACL)
    self.command("getacl", "ga", handlers.getACL)
    self.command("getperm", "gp", handlers.getPerm)
    self.command("setperm", "sp", handlers.setPerm)
    #self.command("createuser", "cu", handlers.createUser)

  def command(self, command, alias = None, handler = None):
    """TODO"""

    self.__commands.append({'name': command, 'alias': alias, 'handler': handler})

  def __getHandler(self, command):
    """TODO"""

    cmd = filter(lambda c: (c['name'] == command) or (c['alias'] == command), self.__commands)
    if len(cmd) == 1 :
      return cmd[0]['handler']
    else:
      return None
    
  def run(self):
    """TODO"""

    try:
      while True:
        
        line = raw_input(self.__prompt)
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
