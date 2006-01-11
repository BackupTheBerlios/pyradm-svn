#!/usr/bin/python

class Config:
  """TODO"""

  def __init__(self):
    """TODO"""

    self.__config = {}
    self.__config['server'] = {}
    self.__config['credentials'] = {}
    self.__config['connection'] = {}
    self.__config['sharedMB'] = {}

    self['server']['host'] = "imap.ric.cad.ru"
    self['server']['port'] = 993
    self['credentials']['user'] = "admin"
    self['credentials']['passwd'] = "K3iAhcDz"
    self['connection']['ssl'] = True

    self['sharedMB']['defaultACL'] = [("anyone", "p"), ("admin", "lrswipcda")]
    self['sharedMB']['defaultChildrens'] = ["spam"]

  def __getitem__(self, idx):
    
    return self.__config[idx]
