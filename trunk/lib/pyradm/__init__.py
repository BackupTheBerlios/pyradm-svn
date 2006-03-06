__all__ = ["Help", "Config", "Options", "QuitException"]

import sys, os
import pickle
from getopt import getopt

masterPassword = "blabla"

Help = {}

class Options:
    """TODO"""

    __options__ = None

    def __init__(self):
        """TODO"""

        if not Options.__options__:
            Options.__options__ = {
                'help': False,
                'config': os.getenv('HOME') + "/.pyradmrc",
                'maintain': False,
            }
            self.__getopt()

    def __setitem__(self, option, value):
        """TODO"""

        if not Options.__options__: raise NotImplementedError("FIXME set option %s before initialization" % (option))
        Options.__options__[option] = value

    def __getitem__(self, option):
        """TODO"""

        if not Options.__options__: raise NotImplementedError("FIXME get option %s before initialization" %(option))
        return Options.__options__[option]

    def __getopt(self, args = sys.argv[1:]):
        """TODO"""

        options = getopt(args, "c:mh", ["config=", "maintain", "help"])

        for option in options[0]:
            if option[0] in ["-c", "--config"]:
                self['config'] = option[1]
            elif option[0] in ["-h", "--help"]:
                self['help'] = True
            elif option[0] in ["-m", "--maintain"]:
                self['maintain'] = True

class Config:
    """TODO"""

    __config__ = None
    __masterPassword__ = None

    def __init__(self):
        """TODO"""

        if not Config.__config__ and Config.__masterPassword__:
            self.load()

    def __setitem__(self, parameter, value):
        """TODO"""

        if not Config.__config__: raise NotImplementedError("FIXME set config parameter %s before initialization" % (parameter))
        Config.__config__[parameter] = value

    def __getitem__(self, parameter, value):
        """TODO"""

        if not Config.__config__: raise NotImplementedError("FIXME get config parameter %s before initialization" % (parameter))
        return Config.__config__[parameter]

    def setMasterPassword(self, password):
        """TODO"""

        Config.__masterPassword__ = password

    def load(self):
        """TODO"""

        if not Config.__masterPassword__: raise NotImplementedError("FIXME load config before setting password")
        Config.__config__ = pickle.load(file(Options["config"]))
    
    def save(self):
        """TODO"""
        
        if not Config.__masterPassword__: raise NotImplementedError("FIXME save config before setting password")
        pickle.dump(Config.__config__, file(Options["config"], "w"))

class QuitException(Exception): pass
