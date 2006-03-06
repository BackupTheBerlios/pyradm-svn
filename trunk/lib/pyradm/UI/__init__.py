__all__ = ["CLI", "Command"]

import readline
from getpass import getpass

from pyIMAP import IMAPError
from pyradm import Config, Options
from pyradm.utils import yes
import handlers

class Command:
    """TODO"""

    def __init__(self, aliases, handler, helpText = "No help available"):
        """TODO"""

        self.__handler = handler
        self.__helpText = helpText
        
        for alias in aliases:
            CLI.__commands__[alias] = self

    def __call__(self, args):
        """TODO"""

        self.__handler(args)

class CLI:
    """TODO"""

    __commands__ = {}

    def __init__(self):
        """TODO"""

        self.imapServer = None
        self.initPrompt()

    def message(self, msg):
        """TODO"""

        print msg

    def askPassword(self):
        """TODO"""

        return getpass("Password: ")

    def askConfirmedPassword(self):
        """TODO"""

        password = getpass("Password: ")
        password2 = getpass("Password again: ")

        if (password != password2): raise CLI.PasswordsDoNotMatch()

        return password

    def readCommand(self):
        """TODO"""

        line = raw_input(self.__prompt)
        # FIXME parser should recognize quoting
        words = line.split()
        return (words[0], words[1:])

    def initPrompt(self):
        """TODO"""

        # FIXME handle empty default server

        try:
            config = Config()
            serverConfig = config['imapServers'][config['defaultServer']]
            self.__prompt = "[%s@%s]: " % (serverConfig['username'], serverConfig['host'])
        except:
            self.__prompt = "[Maintenance mode]: "
        
    def run(self):
        """TODO"""

        config = Config()
        options = Options()

        if config.exists():

            password = None
            tries = 0

            while not password and tries < 3:
                try:
                    password = self.askPassword()
                    config.load()
                except Config.BadPassword:
                    self.message("Bad password")
                    tries += 1
                if tries >= 3: raise Abort()

            config.load()

            if config['defaultServer'] and not options['maintain']:
                self.imapServer = handlers.connectIMAPServer(config['defaultServer'])
            else:
                options['maintain'] = True

        else:

            if yes("Config file %s not exists.\nCreate one?" % options["config"]):
                password = self.askConfirmedPassword()
                config.setMasterPassword(password)
                config.save()
            else:
                raise Abort()

        self.initPrompt()

        while True:
            try:
                (command, args) = self.readCommand()
                CLI.commands[command](args)
            except CLI.SyntaxError, e:
                self.message(str(e))

Command(
    ["logout", "quit"],
    handlers.logout,
)
